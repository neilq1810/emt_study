# Chapter 10 — Timing, Clocking & Synchronization

> **Status:** DEEPENED (awaiting review) · **Part III — Tracker Architecture**
> Builds on Ch. 5 (coupling matrix), Ch. 8 (chain). Detailed estimation math is
> in Part VII (Ch. 19–20). Citation keys resolve to
> [`../../citations/bibliography.json`](../../citations/bibliography.json).

The forward model (Ch. 5) gives nine numbers — the coupling-matrix entries
$M_{ij}$ between three transmit axes and three sense axes. But a single sensor
coil produces *one* voltage at a time; the system must **separate** the
contributions of the three (or more) transmit axes, and it must know the
**phase reference** of the excitation to recover signed amplitudes. Both jobs
are problems of *timing*. This chapter covers channel separation
(time/frequency/code division), coherent vs. non-coherent detection, and the
clock-jitter budget — the architectural decisions that determine update rate and
set a noise floor the rest of the system cannot beat.

---

## 10.1 The channel-separation problem

A sensor axis measures $\varepsilon_j(t)=-\sum_i M_{ij}\,\dot I_i(t)$ — a
superposition of all transmit axes (Ch. 5 §5.6). To recover the individual
$M_{ij}$ we must make the transmit axes *distinguishable*. Three classic
multiplexing schemes, exactly analogous to communications:

| Scheme | Transmit axes are separated by… | Pros | Cons |
|---|---|---|---|
| **TDM** (time division) | activating one axis at a time | simple decode; no crosstalk if settled; cheap RF | update rate divided by #axes; motion between slots |
| **FDM** (frequency division) | a distinct frequency per axis | all axes simultaneous → higher rate; easy multi-axis | needs guard bands/bandwidth; crosstalk if filters imperfect; per-frequency calibration |
| **CDM** (code division) | orthogonal codes per axis | simultaneous; processing gain; interference-robust | most complex DSP; code/sync design |

The trade is developed quantitatively in Ch. 19. At the architecture level: TDM
is the simplest and most distortion-clean (each axis can be sampled after its
own settling) but pays an update-rate penalty and is sensitive to target motion
*between* time slots; FDM maximizes simultaneity and update rate but spends
bandwidth and demands careful crosstalk control; CDM trades DSP complexity for
robustness. In practice, "TDM is simpler to keep clean; FDM is faster but
needs care with crosstalk and bandwidth" is the rule of thumb borne out across
implementations (conf: med — consistent with the multiplexing literature and
engineering practice; FDM's easier synchronization but larger-bandwidth/crosstalk
trade is widely reported).

## 10.2 Coherent (synchronous) vs. non-coherent detection

The recovered quantity is a small AC (or transient) amplitude buried under the
geomagnetic field and broadband interference (Ch. 4 §4.7). The dominant
technique is **synchronous (coherent) detection** — multiply the sensor signal
by a reference at the excitation frequency/phase and low-pass filter, i.e. a
**lock-in amplifier** (full math in Ch. 20). Coherent detection requires the
receiver to know the **phase** of the transmitter excitation, which is the core
synchronization requirement of this chapter.

- **Coherent** systems share a phase reference between transmitter and receiver
  (a wired clock, or a recovered reference). They achieve the narrowest
  effective noise bandwidth and recover *signed* amplitudes (sign carries
  orientation information, Ch. 5). This is the high-performance default.
- **Non-coherent** systems estimate amplitude without absolute phase (e.g.
  magnitude from quadrature, or envelope detection). Simpler and tolerant of an
  unsynchronized wireless link, but they lose sign information and pay an SNR
  penalty.

The synchronization can be delivered by a **wired reference**, by an **RF/BLE
clock-sync** between transmitter and receiver, or by an **EM-pulse handshake**
that lets the receiver measure and track its clock offset to the transmitter.
Wireless and detachable-sensor architectures live or die on the quality of this
sync.

**How tight must sync be?** A timing offset $\delta t$ between transmitter and
receiver is a phase error $\delta\phi=\omega\,\delta t$ in the coherent detector,
which attenuates the in-phase amplitude by $\cos\delta\phi$ (Ch. 20 §20.4). To
hold the amplitude error below 1% requires $\delta\phi\lesssim 8^\circ=0.14$ rad,
i.e. at $f=10\,\text{kHz}$:
$$
\delta t \lesssim \frac{0.14}{2\pi f} \approx 2.2\,\mu\text{s}.
$$
This is the quantitative synchronization budget: a *wired* reference meets it
trivially; a *wireless* link must discipline its clock to the
**microsecond** level. That this is achievable is shown by wireless EMT
demonstrations — e.g. transmitting the sensor signal over an FM radio link on the
open-source Anser system reached $1.61\pm0.68$ mm, comparable to the $1.14$ mm
wired baseline [@crowley2023; @jaeger2017]. (conf: high — the phase-error budget
is direct from Ch. 20 §20.4; the wireless accuracy is the reported result.)

## 10.3 Clock architecture and the reference chain

A coherent system is built around one **master clock** (often the DDS reference
that generates the excitation, Ch. 9 §9.4). The reference is distributed to:
the generator drive (defines excitation frequency/phase), the ADC sample clock
(defines when the receiver looks), and the digital demodulator (defines the
lock-in reference). Any *relative* timing error between these corrupts the
amplitude estimate. The key architectural decision is **how the reference reaches
the receiver** — physically shared (best), recovered from the received signal,
or independently disciplined and offset-tracked (wireless).

**Coherent sampling.** Deriving the excitation frequency $f_0$ and the ADC sample
rate $f_s$ from the *same* master clock with an integer ratio
$f_s/f_0 = $ integer (and an integer number of cycles in the analysis window)
makes the single-bin DFT / lock-in estimate *exact* — no spectral leakage
(Ch. 18 §18.3, Ch. 20 §20.3). This is essentially free when one clock fans out to
both, and is the cleanest reason to build the system around a single reference
rather than independent transmit and receive clocks. It also dovetails with the
per-coil resonant tuning of Ch. 9 §9.4: each FDM coil's frequency is a known
integer division of the master clock, so its tank and its demodulator stay
locked together.

## 10.4 Clock jitter as a noise floor

Even with perfect *average* synchronization, **jitter** — random
sample-instant timing error — injects amplitude/phase noise that no downstream
processing can remove. For a sinusoidal signal of frequency $f$, RMS timing
jitter $\sigma_t$ produces an aperture-jitter SNR ceiling

$$
\mathrm{SNR}_{\text{jitter}} = -20\log_{10}\!\big(2\pi f\,\sigma_t\big)\ \text{[dB]},
\tag{10.1}
$$

the standard ADC aperture-jitter relation (derived and applied to ENOB in
Ch. 18). Two consequences for EMT:

1. The same higher excitation frequency that buys coil sensitivity (Ch. 5 §5.2)
   *tightens* the jitter requirement via (10.1) — another facet of the
   frequency trade.
2. The jitter floor must sit **below** the thermal/quantization noise floor of
   the AFE/ADC (Ch. 16, 18), or it dominates the error budget (Ch. 25). This
   makes the reference oscillator's phase noise a first-class system spec, not
   an afterthought.

*Worked sanity check:* at $f=10\,\text{kHz}$, achieving an 80 dB jitter ceiling
needs $2\pi f\sigma_t \le 10^{-4}$, i.e. $\sigma_t \lesssim 1.6\,\text{ns}$ —
readily met by ordinary crystal references, confirming that at EMT's low
frequencies **jitter is usually not the limiting term** (unlike RF systems).
The dominant timing concern in EMT is therefore *settling/sequencing* (TDM) and
*phase-reference integrity* (coherence), not raw jitter. (conf: high — direct
application of (10.1) at EMT frequencies.)

**Three timing errors, not one.** It helps to keep them distinct: (i) **aperture
jitter** (random sample-instant error, eq. 10.1) — a per-sample noise floor,
negligible here; (ii) **static phase offset / sync error** (§10.2) — a coherent
amplitude bias $\propto\cos\delta\phi$, the binding constraint for wireless
links; and (iii) **output/frame jitter** (variation in *when each pose is
produced*, Ch. 22 §22.7) — irrelevant to amplitude SNR but important for control
loops and fusion (Ch. 21). A reference's **phase noise** — the frequency-domain
view of jitter — integrates to (i); its slow drift contributes to (ii). EMT is
forgiving of (i), demanding on (ii), and (iii) is a real-time-scheduling problem.

## 10.5 Timing and update rate

Timing choices set the **update rate**, a clinically critical spec:

- **TDM:** $f_\text{update} \approx 1/(N_\text{axes}\times t_\text{slot})$, where
  $t_\text{slot}$ includes settling + integration. More axes (or more
  transmitters in an array) → slower updates unless slots shorten (less
  integration → more noise). A direct rate-vs-accuracy trade.
- **FDM:** all axes simultaneous, so update rate is set by the integration time
  needed for the desired per-frequency SNR and bin separation, not by axis
  count — generally faster, at the bandwidth/crosstalk cost of §10.1. Note the
  channel spacing is bounded *below* by two things: the bin resolution $1/\tau$
  (Ch. 19) **and** the per-coil resonant bandwidth $f_0/Q$ (Ch. 9 §9.4) — a
  high-$Q$ resonant generator coil only passes a narrow band around its own
  frequency, which both enforces channel separation and demands frequency
  stability.
- **Pulsed-DC:** rate limited by per-axis eddy-current settling wait (Ch. 6
  §6.4) plus magnetometer integration.

These feed directly into the end-to-end latency budget of Ch. 12.

## 10.6 Cross-modality time synchronization & clock domains

§§10.3–10.5 synchronize *within* the tracker. But a clinical system **fuses several
devices** — the EM tracker, an IMU, an optical tracker, imaging (US/fluoro/CT), robot
encoders — and **each has its own clock and its own latency**. Fusion (Ch. 21) and
registration (Ch. 40/43) assume the measurements they combine share a **common timebase**;
when they do not, the error is direct and often dominant.

**The skew error is a first-class accuracy term.** A time offset $\Delta t$ between two
modalities observing a target moving at velocity $v$ injects a position error
$\approx v\,\Delta t$. At catheter/respiratory speeds (≈50–200 mm/s), a **10 ms** skew gives
**0.5–2 mm** — comparable to the entire accuracy budget. This is the quantified form of the
"time-skew in fusion" failure mode flagged in Ch. 21 §21.8: cross-modality sync is not a
detail, it is a millimetre-class error source.

**Mechanisms.**
- **Timestamp at the source** — each modality stamps its sample at the instant of
  *acquisition*, not arrival, so downstream buffering/jitter cannot corrupt the time.
- **Align the clock domains** — a shared **hardware trigger / sync line**, **IEEE 1588 PTP**,
  or a **PPS** reference ties the domains to a common epoch.
- **Calibrate fixed latency** — measure each modality's pipeline delay (Ch. 12) and
  compensate it; for **periodic** motion, additionally phase-align via the gating signal
  (Ch. 41).
- **Cross the domains in software** — the integrated filter (Ch. 21) ingests **asynchronous,
  out-of-sequence** measurements by interpolating/extrapolating each to a common time using
  its timestamp; the determinism this needs is the reproducibility requirement of Ch. 35
  §35.5.

The throughline: a trustworthy **timestamp travels with every measurement**, and the fusion
estimator is built to consume measurements on one timeline — without which the most accurate
per-modality pose still fuses into a millimetre error.

---

## Open questions / to verify
- ✅ **Resolved:** wireless synchronization now has a peer-reviewed anchor
  [@crowley2023] and a quantified sync budget (§10.2, ~2 µs at 10 kHz). Remaining:
  source a primary description of the *EM-pulse handshake* scheme specifically.
- Provide representative $t_\text{slot}$, integration-time, and update-rate
  figures per architecture from sourced material (Ch. 28) rather than asserting.

## Sources cited
- [@raab1979], [@franz2014] coherent-detection EMT context. [@crowley2023]
  wireless (FM) sensor link & sync accuracy. [@jaeger2017] coherent FDM master-clock
  realization (Anser). Multiplexing/lock-in detail cross-referenced to Ch. 19–20;
  jitter to Ch. 18.
