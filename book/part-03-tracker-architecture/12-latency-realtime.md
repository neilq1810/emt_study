# Chapter 12 — Latency & Real-Time Constraints

> **Status:** DRAFT · **Part III — Tracker Architecture**
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

## 12.3 Latency vs. lag: a subtle distinction

- **Pure latency** (a fixed delay) shifts the pose in time; for constant
  velocity it produces a position error $\approx v\cdot t_\text{total}$.
- **Filter lag** (from smoothing) is velocity-dependent and *frequency-shaped*:
  it attenuates and delays fast motion more than slow motion, which can feel
  like "sluggishness" distinct from a constant delay.

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
- Populate §12.1 with representative measured per-term latencies for at least one
  AC and one pulsed-DC architecture, from sourced material (Ch. 28), with
  conditions.
- Add a worked trilemma example: given a clinical accuracy + rate requirement,
  derive the required AFE/ADC noise spec (ties Ch. 16/18/25 together).
- Verify typical clinical latency requirements per application (EP, bronchoscopy,
  robotics) for Ch. 29 and cross-reference here.

## Sources cited
- [@hummel2005] static-accuracy reference for the §12.3 dynamic-error comparison.
  Per-architecture latency figures flagged for primary-source attachment above.
