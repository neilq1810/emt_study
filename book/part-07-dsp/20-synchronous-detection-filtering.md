# Chapter 20 — Synchronous Detection & Filtering

> **Status:** DRAFT · **Part VII — Digital Signal Processing**
> Builds on Ch. 19 (channel separation) and Ch. 10 (coherence). Produces the
> channel amplitudes $\hat a_{ij}$ for Ch. 11/23. Citation keys resolve to
> [`../../citations/bibliography.json`](../../citations/bibliography.json).

Having separated the transmit axes (Ch. 19), the receiver must estimate each
channel's **amplitude** (and, for coherent systems, phase) from samples buried in
noise far larger than the signal (Ch. 4 §4.7). The dominant technique is
**synchronous (lock-in) detection** — multiply by a reference at the excitation
frequency and low-pass filter — which is the matched filter for a known-frequency
tone and achieves an extraordinarily narrow effective noise bandwidth. This
chapter derives the lock-in, relates it to FFT/matched-filter amplitude
estimation, and covers adaptive filtering for interference rejection.

---

## 20.1 The lock-in amplifier: derivation

Let the signal be $v(t) = A\cos(\omega_0 t + \phi) + n(t)$. Multiply by two
references in quadrature, $\cos\omega_0 t$ and $\sin\omega_0 t$ [@scofield1994]:

$$
v(t)\cos\omega_0 t = \tfrac{A}{2}\cos\phi + \tfrac{A}{2}\cos(2\omega_0 t+\phi) + n\cos\omega_0 t .
$$

A **low-pass filter** removes the $2\omega_0$ term and most of the noise, leaving
the **in-phase** component $X=\tfrac{A}{2}\cos\phi$; the sine reference gives the
**quadrature** component $Y=\tfrac{A}{2}\sin\phi$. Then

$$
\boxed{\,A = 2\sqrt{X^2+Y^2},\qquad \phi=\operatorname{atan2}(Y,X).\,}
\tag{20.1}
$$

The amplitude $A$ is proportional to the channel coupling $M_{ij}$ (Ch. 5), and
the sign/phase carries orientation information. Computing both $X$ and $Y$ makes
the magnitude estimate **independent of the signal phase** — essential when the
exact phase is unknown or drifts.

### Why it works: the noise bandwidth
The low-pass filter of time constant $\tau$ (or integration time $T$) has an
**equivalent noise bandwidth** $\sim 1/(2\tau)$ (or $\sim 1/T$). Only noise within
this tiny band *around $\omega_0$* survives; everything else — including the
geomagnetic DC offset, mains lines, and broadband noise — is rejected
[@scofield1994]. A Phase-5 simulation (`simulations/run_all.py`,
`figures/ch20_lockin_snr_vs_T.png`) confirms the amplitude-error scaling:
recovering a tone buried under noise 5× its amplitude, the lock-in estimate error
falls as $T^{-0.49}$ (≈ the predicted $1/\sqrt{T}$). For $T=10\,\text{ms}$ the
noise bandwidth is ~100 Hz, an
enormous rejection of out-of-band interference, and longer $T$ narrows it further
(at the cost of update rate/latency — the trilemma of Ch. 12). This is the
quantitative reason EMT can recover sub-µT signals beneath a 50 µT geomagnetic
field (Ch. 4 §4.7).

## 20.2 Equivalence to single-bin DFT and the matched filter

For coherent sampling (Ch. 18 §18.3) over an integer number of cycles, the
lock-in's $X,Y$ are *exactly* the real and imaginary parts of the **DFT bin** at
$\omega_0$:

$$
X+jY \;\propto\; \sum_{k} v[k]\,e^{-j\omega_0 k/f_s}.
$$

Three consequences:

1. **FDM falls out for free.** One FFT evaluates all FDM channels (Ch. 19 §19.2)
   simultaneously — each transmit frequency is a separate bin. This is why FDM
   systems often use an FFT rather than parallel analog lock-ins.
2. **Optimality.** For a known-frequency sinusoid in additive white Gaussian
   noise, the single-bin DFT *is* the matched filter — the minimum-variance
   unbiased amplitude estimator. The lock-in is therefore not just convenient but
   (near-)optimal [@scofield1994].
3. **Leakage discipline.** If sampling is *not* coherent, spectral leakage biases
   the estimate; windowing or coherent sampling (Ch. 18) mitigates it. This is
   the DSP reason coherent clocking (Ch. 10) matters.

## 20.3 Matched filtering for pulsed-DC

Pulsed-DC systems do not have a steady tone; the "signal" is the **settled level**
(or the full transient) after a current step (Ch. 6 §6.4). The optimal estimator
is again a matched filter — here matched to the *expected settling waveform*:
weight and integrate the post-step samples to estimate the static field amplitude
while rejecting noise and any residual eddy transient. Choosing the integration
window (start after eddy settling, end before drift) is the pulsed-DC analogue of
choosing $\tau$ in the lock-in, with the same rate/accuracy trade.

## 20.4 Adaptive filtering for interference

Some interference is neither DC nor at a fixed out-of-band frequency — e.g. a
nearby motor, switching supply, or another EM device whose spectrum overlaps or
drifts. **Adaptive filters** (LMS/RLS) and **adaptive notch** filters can track
and subtract such interferers, especially when a **reference** of the interference
is available (a "witness" pickup). Related ideas:

- **Reference/witness cancellation.** A sensor that sees *only* the interference
  (not the tracking signal) provides a reference an adaptive filter subtracts from
  the channel — directly analogous to the witness-sensor distortion approaches of
  Ch. 27.
- **Notch at known offenders.** Adaptive notch at mains and its harmonics for the
  residual that band-selection (Ch. 17) and the lock-in do not fully remove.

Adaptive methods must be used cautiously: an over-aggressive adaptive filter can
attenuate the *signal* if the interference reference is contaminated by it, and it
adds latency and nonstationary behavior the error budget (Ch. 25) must account
for.

## 20.5 From amplitudes to the pipeline
The output of this chapter is the set of channel amplitudes/phases $\hat a_{ij}$
— Stage 1 of the pipeline (Ch. 11 §11.1). Their noise is set by the integration
time (∝ 1/√T) and the upstream sensor/AFE/ADC floor (Parts IV–VI); their *bias*
is set by leakage, crosstalk (Ch. 19), and uncorrected distortion (Ch. 6). These
amplitudes, after calibration (Stage 2, Ch. 11/26), become the coupling matrix
$\hat{\mathbf M}$ handed to the position solver (Part VIII).

> **Takeaway.** Synchronous detection is the linchpin that makes EMT possible: by
> collapsing the measurement to a known-frequency, phase-referenced, narrow-band
> estimate, it converts an impossible-looking SNR problem (signal far below
> background) into a routine one. Everything upstream exists to deliver a clean
> tone to this stage; everything downstream trusts the amplitudes it produces.

---

## Open questions / to verify
- Add the explicit equivalent-noise-bandwidth formula for the specific
  low-pass/decimation filter used, and reconcile with the Σ-Δ decimation of
  Ch. 18 to avoid double-counting bandwidth.
- ✅ **Resolved (Phase 5):** SNR-vs-integration-time curve computed
  (`figures/ch20_lockin_snr_vs_T.png`; error $\propto T^{-0.49}$, i.e. $1/\sqrt T$).
  Remaining: tie absolute amplitude SNR to the Ch. 15/16/18 noise floor.
- Source a primary description of pulsed-DC matched-filter detection (vendor or
  peer-reviewed) to firm up §20.3 (currently general principle).

## Sources cited
- [@scofield1994] lock-in derivation, noise bandwidth, optimality. Channel
  separation context from Ch. 19; coherent sampling from Ch. 18; witness/adaptive
  cancellation links to Ch. 27.
