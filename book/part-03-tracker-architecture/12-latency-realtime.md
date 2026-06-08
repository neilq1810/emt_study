# Chapter 12 — Latency & Real-Time Constraints

> **Status:** DEEPENED (awaiting review) · **Part III — Tracker Architecture**
> Closes Part III. Builds on Ch. 8–11. Citation keys resolve to
> [`../../citations/bibliography.json`](../../citations/bibliography.json).

For a tracker used to guide a moving instrument inside a patient, **latency is a
safety and usability spec, not just a performance number**. A pose that is
accurate but 100 ms stale points to where the catheter *was*, not where it *is*.
This chapter assembles the end-to-end latency budget, exposes the fundamental
**accuracy–rate–latency trilemma**, and states the real-time determinism
requirements that the implementation (Ch. 22) must meet. Together with the error
budget (Ch. 25), the latency budget is one of the two scorecards by which a
design is judged.

---

## 12.1 The end-to-end latency budget

Total motion-to-pose latency is the sum of contributions along the chain of
Ch. 8:

$$
t_\text{total} = t_\text{excite/settle} + t_\text{integrate} + t_\text{ADC+decim}
+ t_\text{demod} + t_\text{solve} + t_\text{filter} + t_\text{transport}.
\tag{12.1}
$$

| Term | What it is | Dominant in | Set by |
|---|---|---|---|
| $t_\text{excite/settle}$ | per-axis settling (esp. pulsed-DC eddy decay) | pulsed-DC | Ch. 6 §6.4, Ch. 10 |
| $t_\text{integrate}$ | coherent integration / averaging window | AC | Ch. 10 §10.5, Ch. 11 §11.1 |
| $t_\text{ADC+decim}$ | conversion + decimation filter group delay | Σ-Δ ADCs | Ch. 18 |
| $t_\text{demod}$ | lock-in / FFT low-pass group delay | all | Ch. 20 |
| $t_\text{solve}$ | iterative pose solve | poorly conditioned poses | Ch. 23–24 |
| $t_\text{filter}$ | Kalman/smoothing lag | smoothed systems | Ch. 21 |
| $t_\text{transport}$ | bus/USB/network to host | wireless/USB | Ch. 8, host API |

The **architecture-fixed** dominant terms are usually $t_\text{integrate}$ (AC)
or $t_\text{excite/settle}$ (pulsed-DC) — exactly the terms that also set update
rate (Ch. 10) and noise (Ch. 11). This is not a coincidence; it is the trilemma.

**Two worked budgets** (engineering estimates from the deepened subsystem
chapters; conf: med pending per-product sourcing):

| Term | AC FDM (τ = 5 ms) | Pulsed-DC (TDM, clean room) | Pulsed-DC (5 cm conductor) |
|---|---:|---:|---:|
| $t_\text{excite/settle}$ | ~0 (continuous) | $5\tau_e\approx4$ ms (1 cm Cu) | $5\tau_e\approx90$ ms (Ch. 6 §6.4) |
| $t_\text{integrate}$ + decim/demod group delay | ~5–7 ms (≈τ + τ/2 of the lock-in/CIC, Ch. 20/22) | ~2 ms ×3 axes | ~2 ms ×3 axes |
| $t_\text{solve}$ | ~0.3 ms (LM, Ch. 22) | ~0.3 ms | ~0.3 ms |
| $t_\text{filter}$ (light Kalman) | ~1 ms | ~1 ms | ~1 ms |
| $t_\text{transport}$ (USB) | ~1 ms | ~1 ms | ~1 ms |
| **Total** | **≈ 8 ms** | **≈ 12 ms** | **≈ 100 ms** |

The lesson is stark: an **AC system is integration-dominated** (~8 ms, fixed by
the SNR window), while a **pulsed-DC system is settling-dominated and
*environment-dependent*** — a few milliseconds in a clean room but, per the
eddy-decay law (Ch. 6 eq. 6.3), an order of magnitude worse when a fist-sized
conductor enters the volume. This is a decisive, often-overlooked architectural
difference: pulsed-DC's distortion immunity is bought partly with a *variable*
latency.

## 12.2 The accuracy–rate–latency trilemma

The three headline specs are coupled through **integration time** $\tau$:

- **Accuracy** improves with longer $\tau$ (noise bandwidth $\propto 1/\tau$, so
  amplitude SNR improves ∝ √τ for white noise — Ch. 11 §11.1).
- **Update rate** falls with longer $\tau$ (and with more TDM slots — Ch. 10).
- **Latency** rises with longer $\tau$ (and with filter group delay — §12.1).

You cannot independently maximize all three with a fixed sensor/AFE; improving
one by brute force degrades another. The escape routes are *engineering*, not
free lunches:

1. **Better SNR per unit time** — larger generator moment (Ch. 9), lower-noise
   AFE (Ch. 16), higher ENOB (Ch. 18) — buys accuracy at fixed $\tau$.
2. **Smarter estimation** — a recursive estimator (Ch. 21) with a motion model
   extracts more accuracy per sample, but adds its own lag if over-smoothed.
3. **Prediction** — a forward-predicting filter can *hide* latency for smooth
   motion by extrapolating, at the risk of overshoot during fast/irregular
   motion. Common in head-tracking; used cautiously in medical contexts.

> **Design discipline.** Fix two of {accuracy, rate, latency} from the clinical
> requirement (Ch. 29) and let the third be the dependent variable; then use
> routes 1–3 to move the frontier. Trying to specify all three independently is
> the most common way an EMT requirement becomes infeasible.

### Worked trilemma — when a catheter sensor cannot meet the spec
Suppose the requirement is **σ ≤ 1 mm at the volume edge ($z=0.5$ m), update rate
≥ 100 Hz**, with a small catheter sensor ($N_sA_s = 10^{-4}\,\text{m}^2{\cdot}$turn).
Trace the trilemma:

1. **Rate pins $\tau$.** $\ge100$ Hz with overhead → $\tau\lesssim5$ ms →
   $\mathrm{ENBW}\approx1/(2\tau)=100$ Hz (Ch. 20). $\tau$ is now *fixed*; it
   cannot be the free variable.
2. **$\tau$ and the noise floor fix $\sigma_B$.** Demodulated voltage noise
   $\sigma_\varepsilon = e_n\sqrt{\mathrm{ENBW}} = 1.3\,\tfrac{\text{nV}}{\sqrt{\text{Hz}}}\times\sqrt{100}=13$ nV
   (Ch. 20). Field-referred:
   $\sigma_B=\sigma_\varepsilon/(N_sA_s\,\omega)=13\,\text{nV}/(10^{-4}\times6.28\times10^4)=2.1$ nT.
3. **$\sigma_B$ and geometry fix accuracy.** At $z=0.5$ m the CRLB gain is
   $0.66\,\text{mm/nT}$ (Ch. 24, Phase-5), so
   $\sigma_\text{pos}=2.1\times0.66\approx\mathbf{1.4\ mm} > 1\ \text{mm}$ — the
   spec **fails**.

The trilemma is now explicit: with $\tau$ pinned by the rate, accuracy is
*determined*, not free. The only escapes are route 1 (SNR-per-time): **double the
generator moment** $m_t$ (halves $\sigma_B$ → 0.7 mm ✓), **halve the AFE noise**
$e_n$ (same effect), or **shrink the working volume** (at $z=0.45$ m the CRLB gain
drops as $z^4$, to ~0.43 mm/nT → 0.9 mm ✓). What you *cannot* do is simply
"integrate longer" — that would violate the rate requirement. This is exactly the
master link budget (Ch. 8 eq. 8.1) read as a constraint, and it resolves how a
requirement is made feasible (or shown infeasible) *before* building. (conf: high
— assembled from eqs. 5.2, 20.3, 24.1 and the Phase-5 CRLB gain.)

## 12.3 Latency vs. lag: a subtle distinction

- **Pure latency** (a fixed delay) shifts the pose in time; for constant
  velocity it produces a position error $\approx v\cdot t_\text{total}$.
- **Filter lag** (from smoothing) is velocity-dependent and *frequency-shaped*:
  it attenuates and delays fast motion more than slow motion, which can feel
  like "sluggishness" distinct from a constant delay. Quantitatively, a
  linear-phase FIR of length $L$ contributes a *constant* group delay
  $(L-1)/(2f_s)$ (the decimation/lock-in low-pass, Ch. 18/20/22); a Kalman filter
  contributes a velocity-lag set by its effective bandwidth (the $\mathbf Q/\mathbf R$
  tuning, Ch. 21 §21.8) — tighter smoothing (small $\mathbf Q$) means more lag.
  The FIR part is a pure delay (compensable by timestamping); the Kalman part is a
  dynamic distortion that prediction (route 3) partly offsets.

A 10 ms total latency at a catheter tip speed of $0.1\,\text{m/s}$ yields a
1 mm dynamic position error — comparable to the *static* accuracy of good
systems (Ch. 1 §1.7, [@hummel2005]). So for moving targets, **latency can
dominate the error budget even when static accuracy is excellent** — a point
easy to miss when reading datasheet accuracy numbers measured statically.
(conf: high — direct kinematics; the static-accuracy reference is [@hummel2005].)

## 12.4 Real-time determinism

Average latency is not enough; medical and robotic integration require **bounded
worst-case** latency and **low jitter** in the *output* timing (distinct from
clock jitter, Ch. 10 §10.4). Requirements:

- **Deterministic Stage-1 processing** (Ch. 11) — hence the FPGA/DSP home
  (Ch. 22): fixed-cost per frame, no data-dependent branching at the sample
  rate.
- **Bounded solver iterations** (Ch. 23) — cap iterations and fall back to the
  predicted/previous pose with a flagged covariance rather than blow the time
  budget at a poorly conditioned pose (Ch. 24).
- **Timestamping at acquisition** — so fusion (Ch. 21) and host applications can
  compensate known, fixed transport delays; this is essential for combining EM
  pose with imaging or robot kinematics.

## 12.5 Latency in fusion and multi-modal systems

When EM pose is fused with IMU (high-rate, low-latency, drifting) or optical
(accurate, occludable) data (Ch. 21), **relative latency/time-alignment between
modalities** becomes a first-order error source: fusing a fresh IMU sample with a
stale EM sample injects error proportional to the time skew × velocity. Accurate
**timestamping and time-base alignment** across modalities is therefore part of
the latency design, not an afterthought — and is a recurring theme in the
hybrid-system frontier of Part XIII.

---

## Open questions / to verify
- ✅ **Resolved (engineering estimate):** §12.1 now has worked AC/pulsed-DC latency
  budgets (~8 ms vs 12–100 ms, settling-dependent) and §12.2 a worked trilemma
  deriving the SNR/noise spec from a rate+accuracy requirement. Remaining: replace
  the per-term estimates with *measured* per-product figures (Ch. 28).
- Verify typical clinical latency requirements per application (EP, bronchoscopy,
  robotics) for Ch. 29 and cross-reference here.

## Sources cited
- [@hummel2005] static-accuracy reference for the §12.3 dynamic-error comparison.
  Latency budget assembled from Ch. 6 (settling), 20 (integration/group delay),
  22 (decimation), 8 (link budget); per-product figures flagged above.
