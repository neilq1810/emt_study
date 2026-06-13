# Chapter 20 — Synchronous Detection & Filtering

> **Status:** DEEPENED (awaiting review) · **Part VII — Digital Signal Processing**
> Builds on Ch. 19 (channel separation) and Ch. 10 (coherence). Produces the
> channel amplitudes $\hat a_{ij}$ for Ch. 11/23. Citation keys resolve to
> [`../../citations/bibliography.json`](../../citations/bibliography.json).

Having separated the transmit channels (Ch. 19), the receiver must estimate each
channel's **amplitude** (and, for coherent systems, phase) from samples buried in
noise far larger than the signal (Ch. 4 §4.7). The dominant technique is
**synchronous (lock-in) detection** — multiply by a reference at the excitation
frequency and low-pass filter — which is the matched filter for a known-frequency
tone and achieves an extraordinarily narrow effective noise bandwidth. This
chapter derives the lock-in and its **equivalent noise bandwidth** rigorously,
proves its optimality via the single-bin DFT, then treats the *implementation*
realities that decide whether a lock-in performs to theory — **synchronous vs.
asynchronous detection** (the shared-clock coherence that makes both leakage *and*
phase behave), reference phase and harmonic content, dynamic reserve, analog vs.
digital realization, and the **significance of the phase channel** (orientation sign
and a quadrature distortion signature) — and finishes with pulsed-DC matched filtering
and adaptive interference cancellation. The open-source Anser platform is a concrete
digital-lock-in EMT realization [@jaeger2017].

---

## 20.1 The lock-in amplifier: dual-phase derivation

Let the signal on a sensor channel be
$v(t) = A\cos(\omega_0 t + \phi) + n(t)$, with $\omega_0$ the (known) excitation
frequency, $A\propto M_{ij}$ the coupling we want (Ch. 5), $\phi$ a fixed
channel/propagation phase, and $n(t)$ broadband noise. Multiply by two reference
waveforms in quadrature [@scofield1994]:

$$
v(t)\cos\omega_0 t = \tfrac{A}{2}\cos\phi + \underbrace{\tfrac{A}{2}\cos(2\omega_0 t + \phi)}_{\text{rejected by LPF}} + n(t)\cos\omega_0 t,
$$
$$
v(t)\sin\omega_0 t = -\tfrac{A}{2}\sin\phi + \tfrac{A}{2}\sin(2\omega_0 t + \phi) + n(t)\sin\omega_0 t .
$$

A **low-pass filter** removes the $2\omega_0$ terms and the out-of-band noise,
leaving the **in-phase** and **quadrature** outputs

$$
X = \tfrac{A}{2}\cos\phi,\qquad Y = \tfrac{A}{2}\sin\phi,
$$
$$
\boxed{\,A = 2\sqrt{X^2+Y^2},\qquad \phi=\operatorname{atan2}(Y,X).\,}
\tag{20.1}
$$

The amplitude $A$ is proportional to the channel coupling $M_{ij}$, and the
*sign/phase* carries orientation information (the coupling can be negative,
Ch. 5 §5.4). Computing both $X$ and $Y$ makes the **magnitude estimate
independent of the unknown signal phase** — essential when $\phi$ drifts with
temperature or cable length, or when the transmitter–receiver phase reference is
only approximately known (§20.4).

## 20.2 Equivalent noise bandwidth and output SNR

The lock-in's power comes from the low-pass filter: it admits only noise within a
narrow band *centered on $\omega_0$*. Quantitatively, the filter's **equivalent
noise bandwidth (ENBW)** sets the output noise.

- **Integrate-and-dump** (boxcar of length $T$), $h(t)=1/T$ for $0\le t<T$: the
  one-sided ENBW is
  $$
  \mathrm{ENBW}_\text{boxcar} = \frac{1}{2T}\ \text{[Hz]} .
  \tag{20.2}
  $$
- **First-order RC** of time constant $\tau$: $\mathrm{ENBW}_\text{RC} = 1/(4\tau)$.

If the input (after band-select, Ch. 17) has one-sided noise PSD $S_n$
[V$^2$/Hz], the demodulated noise variance on each of $X,Y$ is
$\sigma^2 \approx \tfrac14 S_n\,\mathrm{ENBW}$, so the **amplitude noise scales as**

$$
\sigma_A \;\propto\; \sqrt{S_n\,\mathrm{ENBW}} \;\propto\; \frac{1}{\sqrt{T}},
\tag{20.3}
$$

the $1/\sqrt{T}$ law confirmed by the Phase-5 simulation (amplitude error
$\propto T^{-0.49}$ even with the signal buried 5× under noise;
`figures/ch20_lockin_snr_vs_T.png`). Relative to a wideband front end of
bandwidth $B$, the lock-in's **processing gain** is
$B/\mathrm{ENBW} = 2BT$: for $B=10\,\text{kHz}$ and $T=10\,\text{ms}$, that is a
factor of 200 (23 dB) of out-of-band noise rejected — the quantitative reason EMT
recovers sub-µT signals beneath a 50 µT geomagnetic background (Ch. 4 §4.7). The
amplitude SNR delivered to the solver is then
$\mathrm{SNR}_\text{out} = A/\sigma_A$, with $\sigma_A$ traceable through (20.3) to
the sensor/AFE/ADC floor of Parts IV–VI. **The cost of the gain is time:** longer
$T$ narrows ENBW (better SNR) but lowers update rate and raises latency and
intra-frame motion error — the trilemma of Ch. 12 and Ch. 19 §19.6.

## 20.3 Equivalence to the single-bin DFT and the matched filter

For coherent sampling (Ch. 18 §18.3) over an integer number of cycles, the
lock-in's $X,Y$ are *exactly* the real and imaginary parts of the **DFT bin** at
$\omega_0$:

$$
X + jY \;\propto\; \sum_{k} v[k]\,e^{-j\omega_0 k/f_s}.
\tag{20.4}
$$

Three consequences:

1. **FDM falls out for free.** One FFT evaluates all FDM channels (Ch. 19 §19.2)
   simultaneously — each transmit frequency is a separate bin — which is why
   multi-coil FDM systems use an FFT or a parallel lock-in bank [@jaeger2017].
2. **Optimality.** For a sinusoid of *known* frequency in additive white Gaussian
   noise, the single-bin DFT (equivalently the dual-phase lock-in) is the
   **matched filter** and the minimum-variance unbiased estimator of the complex
   amplitude; its variance attains the Cramér–Rao bound for that estimation
   problem [@kay1993; @scofield1994]. The lock-in is therefore not merely
   convenient but *optimal* — no linear or nonlinear estimator does better at
   recovering a known-frequency tone's amplitude.
3. **Synchronous vs. asynchronous detection (leakage *and* phase).** Whether
   detection is *synchronous* turns on one clock decision: if the **excitation
   (DAC) and acquisition (ADC) share a timebase** so the reference is phase-locked
   to the actual drive — as the open-source Anser does with a common DAQ sample
   clock [@jaeger2017] — then sampling is coherent (integer cycles per window), the
   lock-in's $X,Y$ are *exactly* the DFT bin (20.4), there is **no leakage**, and
   the **absolute phase $\phi$ is meaningful** (§20.10). If the clocks **free-run
   (asynchronous)**, the tone falls between bins → **spectral leakage** biases every
   channel *and* the absolute phase drifts arbitrarily; you must then either
   **window** (§20.8) or **estimate** each tone's frequency/phase before
   demodulating. Synchronous (shared-clock) detection is therefore the cleanest path
   and the reason coherence is a first-class system requirement (Ch. 10) — it buys
   both leakage-free amplitude *and* a usable phase channel.

## 20.4 Reference quality: phase, harmonics, jitter, dynamic reserve

The lock-in is only as good as its reference. Four practical effects:

- **Reference phase error.** A single-phase detector outputs
  $\tfrac{A}{2}\cos(\phi - \phi_\text{ref})$; a reference-phase error $\delta$
  attenuates by $\cos\delta \approx 1 - \delta^2/2$ — second-order, so small
  phase errors barely bias the *magnitude* but rotate energy between $X$ and $Y$.
  The dual-phase magnitude (20.1) is first-order phase-insensitive, which is its
  main advantage.
- **Low-SNR magnitude bias (Rician).** The magnitude $\sqrt{X^2+Y^2}$ of two
  Gaussian-noise-corrupted components is **Rician-distributed**, biased *upward*
  by $\sim\sigma$ when $\mathrm{SNR}\lesssim 1$. At the far edge of the working
  volume (weakest coupling, Ch. 24's $z^4$ region) this bias is real; if the phase
  $\phi$ is known/stable, use the unbiased in-phase component $X$ rather than the
  magnitude. (conf: high — standard result for the envelope of a tone in noise.)
- **Reference harmonics.** A *digital* lock-in often multiplies by a $\pm1$
  **square-wave** reference, which is $\tfrac{4}{\pi}(\sin\omega_0 t + \tfrac13\sin 3\omega_0 t + \tfrac15\sin 5\omega_0 t + \cdots)$.
  It therefore also detects signal **and noise at the odd harmonics**
  $3\omega_0, 5\omega_0,\dots$ weighted $1/n$ — folding harmonic interference and
  extra noise into the output unless the input is band-limited around $\omega_0$
  first (Ch. 17). A true *sine* reference (or a band-limited input) avoids this.
  This interacts with FDM frequency planning (Ch. 19 §19.2): a channel on an odd
  harmonic of another is doubly dangerous with square-wave detection. **The flip
  side:** in a system whose sensor signal is *deliberately* a square wave — a
  **triangular excitation** read by the differentiating coil (Ch. 9 §9.9) — those odd
  harmonics *are* the signal, so a **square-wave reference becomes the matched filter**
  and the "penalty" turns into the optimal detector.
- **Reference jitter.** Timing jitter on the reference/sample clock injects
  amplitude/phase noise (Ch. 10 §10.4, eq. 10.1); at EMT frequencies this is
  usually below the thermal floor, but it sets the ultimate coherence limit.

**Dynamic reserve.** Because the ENBW is tiny, a lock-in can recover a small
signal in the presence of a large *out-of-band* interferer — the **dynamic
reserve** (largest tolerable interferer / full-scale signal) can be 60–100 dB.
But the interferer must not overload the *analog* chain *before* demodulation:
dynamic reserve is ultimately bounded by the AFE/ADC dynamic range (Ch. 16 §16.4,
Ch. 18). This is why band-select filtering (Ch. 17 §17.1) precedes the
ADC — to spend the converter's range on signal, not on an interferer the lock-in
would otherwise have removed.

## 20.5 Analog vs. digital realization

- **Analog lock-in:** analog mixer + analog LPF, then a slow ADC on the
  near-DC output. Historically dominant; excellent dynamic reserve if the mixer is
  linear, but gain/offset drift and mixer nonlinearity limit accuracy.
- **Digital lock-in (the modern EMT norm):** band-select + anti-alias → ADC →
  *digital* multiply by reference → digital decimation/LPF. The decimation filter
  of a Σ-Δ ADC (Ch. 18) *is* the lock-in low-pass. Advantages: exact, drift-free
  multiplication; trivial dual-phase; many channels in parallel on an FPGA
  (Ch. 22). Anser implements a digital lock-in across its eight FDM channels
  [@jaeger2017]. The trade is that the ADC must digitize the *full* pre-demod
  signal (including any residual interferer), bounding dynamic reserve by ENOB.

## 20.6 Matched filtering for pulsed-DC

Pulsed-DC systems (Ch. 6 §6.4) have no steady tone; the observable is the
**settled static field** after a current step, once eddy transients decay. The
optimal estimator is again a matched filter — here matched not to a sinusoid but
to the *expected post-step waveform*. Given a model
$s(t) = B_\infty\,[\,1 - \sum_k c_k e^{-t/\tau_k}\,]$ (static field minus decaying
eddy modes, Ch. 6), the minimum-variance estimate of $B_\infty$ weights and
integrates the post-step samples by the matched template. In practice this reduces
to **choosing the integration window**: start after the dominant eddy time
constant $\tau_e$ has decayed (the Phase-5 settling figure,
`figures/ch06_pulsed_dc_settling.png`, shows residual eddy error vs. delay), and
end before slow thermal drift matters. The window choice is the pulsed-DC analogue
of choosing $T$ in the lock-in, with the same SNR-vs-rate trade — *plus* a
distortion term: sampling too early leaves an eddy bias (a *deterministic* error,
Ch. 25 §25.3), sampling too late wastes SNR. (conf: high for the principle; exact
templates are device-specific, flagged below.)

## 20.7 Adaptive filtering for interference

Some interference is neither DC nor at a fixed out-of-band frequency — a nearby
motor, switching supply, or another EM device whose spectrum overlaps or drifts.
**Adaptive filters** track and subtract it [@widrow1975]:

- **Reference/witness cancellation (LMS).** A sensor that observes *only* the
  interference (not the tracking signal) provides a reference; an adaptive FIR
  filter $\mathbf w$ updated by least-mean-squares,
  $\mathbf w_{k+1} = \mathbf w_k + 2\mu\,e_k\,\mathbf x_k$, learns the transfer
  from reference to the corrupting component and subtracts it — the classic
  adaptive noise canceller [@widrow1975]. This is the direct analogue of the
  **witness-sensor distortion** methods of Ch. 27 (a witness coil as the
  interference reference), making §20.7 and §27.3 two views of one idea.
- **Adaptive notch** at mains and its harmonics removes the residual that
  band-select (Ch. 17) and the lock-in do not fully suppress.

**Cautions** (conf: high — standard adaptive-filter pitfalls): if the interference
reference is contaminated by the *signal* (signal leakage into the witness), the
adaptive filter will cancel signal too; step-size $\mu$ trades convergence speed
against misadjustment noise; and the filter is non-stationary, so its contribution
must enter the error budget (Ch. 25) as a time-varying term, not a constant.

## 20.8 FFT methods, windowing, and leakage

When channels are separated by FFT (Ch. 19 FDM), the same coherence discipline
applies: with non-integer-cycle capture, apply a window (Hann, flat-top) to
suppress leakage at the cost of a wider main lobe (slightly larger ENBW). A
**flat-top** window trades frequency resolution for *amplitude* accuracy (flat
passband over a bin), which is what an amplitude-estimating tracker wants when
exact coherence cannot be guaranteed. Coherent sampling (Ch. 18) remains the
cleanest path and avoids windowing entirely.

## 20.9 Worked example — ENBW, processing gain, and the floor

Take $B = 10\,\text{kHz}$ band-select, integrate-and-dump $T = 5\,\text{ms}$
(→ 200 Hz update before TDM/overhead). Then $\mathrm{ENBW} = 1/(2T) = 100\,\text{Hz}$
(eq. 20.2), and processing gain $= B/\mathrm{ENBW} = 100$ (20 dB). If the coil +
AFE deliver an input-referred noise density of $\sim 1.3\,\text{nV}/\sqrt{\text{Hz}}$
(Ch. 15 worked example), the demodulated amplitude noise is
$\sim 1.3\,\text{nV}/\sqrt{\text{Hz}} \times \sqrt{100\,\text{Hz}} \approx 13\,\text{nV RMS}$.
Against the Ch. 4 §4.7 worst-case signal EMF (sub-µV at the volume edge, before
amplification), this gives an amplitude SNR of order $10^1$–$10^2$ at the edge and
much higher near the generator — consistent with the CRLB sub-mm prediction
(Ch. 24) and the ≤1 mm target of Ch. 31. Halving the error requires **4×** the
integration time (eq. 20.3) — the steep price of the $1/\sqrt T$ law. (conf:
high — direct application of (20.2)–(20.3) with the Ch. 15 floor.)

## 20.10 The phase channel: orientation sign and the quadrature distortion signature

The dual-phase lock-in computes the phase $\phi=\operatorname{atan2}(Y,X)$ (20.1) **for
free**, and discarding it (magnitude-only detection) throws away two genuinely useful
things — so for an AC system the phase should *not* be disregarded.

**1 — The sign of the coupling (orientation).** A quasistatic dipole coupling $M_{ij}$ is
*real* and can be **negative** (Ch. 5 §5.4); against a stable system phase reference,
$\phi$ collapses to $0$ or $\pi$, i.e. it carries the **sign** of $M_{ij}$. That sign is
orientation information the magnitude alone discards — it is what lets the closed-form
initializer resolve coupling-matrix signs (Ch. 23 §23.5), so a magnitude-only detector
forfeits observability the dual-phase detector keeps.

**2 — The quadrature component as a distortion sentinel.** A *pristine* quasistatic
coupling sits entirely in one phase (the calibrated system phase). A **conductive/eddy
distorter does not**: the eddy secondary field is driven by $dB/dt$ and, through the
conductor's resistance, **lags the primary**, injecting a **quadrature** component (Ch. 6).
So a growing quadrature signal — a departure of $\phi$ from its calibrated value — is a
**direct, near-free indicator of conductive distortion** that the same lock-in already
measures. It is even *selective*: a **ferromagnetic** distorter perturbs the field largely
**in phase** (a reactive, near-lossless flux concentration, Ch. 6 §6.3) and contributes
little to quadrature, so the phase signature helps **distinguish conductive from
ferromagnetic distortion** — information no amplitude-only (or pulsed-DC) detector gets for
free. This makes the phase channel a built-in **detect-and-flag** input (Ch. 27 §27.4) and
another residual for the reconciled twin (Ch. 56), carrying exactly what a witness sensor
would.

**The catch (back to §20.3).** Absolute phase is interpretable **only if detection is
synchronous** — the reference phase-locked to the drive (§20.3); under asynchronous
detection $\phi$ drifts and the quadrature sentinel is unusable. So the value of the phase
channel is itself an argument for shared-clock coherent detection. (conf: high for the
principle — the eddy quadrature signature is standard; the exact phase-vs-frequency
behaviour is regime-dependent, Ch. 6.)

---

## Failure modes
- **Incoherent sampling → leakage bias** on every channel (§20.3); fix with
  coherent clocking (Ch. 10) or windowing.
- **Square-wave-reference harmonic folding** (§20.4): odd-harmonic noise/interferer
  pulled into the output; band-limit the input or use a sine reference.
- **Rician magnitude bias at low SNR** (§20.4): the far-volume amplitude reads
  high; use the in-phase component if phase is known.
- **Dynamic-reserve overload** (§20.4): a large interferer clips the AFE/ADC
  *before* demodulation, so the lock-in cannot remove it; band-select first.
- **Adaptive-filter signal cancellation** (§20.7): signal leakage into the
  reference makes the canceller erode the signal.

## Open questions / to verify
- Add the explicit one-sided ENBW derivation (boxcar and RC) to Appendix C and
  reconcile with the Σ-Δ decimation-filter ENBW (Ch. 18) to avoid double-counting.
- Source a primary description of a *specific* pulsed-DC matched-filter / window
  (vendor or peer-reviewed) to ground §20.6 (currently general principle).
- Build a Phase-5 notebook for the Rician low-SNR magnitude bias and the
  square-wave harmonic-folding penalty, with curves.
- Confirm representative dynamic-reserve figures against a primary source.
- Simulate the **quadrature distortion signature** (§20.10): the in-phase/quadrature
  split of an eddy distorter vs a ferromagnetic distorter across frequency, as a
  phase-sensitive detect-and-flag input (ties Ch. 6/27, the §56 reconciled twin).
- Source Anser's primary description of the **synchronous (shared-clock) acquisition**
  (§20.3) to ground the async-vs-sync detail beyond the general principle.

## Sources cited
- [@scofield1994] lock-in derivation, ENBW, optimality. [@kay1993] matched-filter/
  CRLB optimality and the Rician magnitude result. [@jaeger2017] digital-lock-in
  FDM realization (Anser). [@widrow1975] adaptive noise cancelling / witness
  reference. Channel separation from Ch. 19; coherent sampling from Ch. 18;
  witness/adaptive links to Ch. 27.
