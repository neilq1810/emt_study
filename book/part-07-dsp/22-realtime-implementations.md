# Chapter 22 — Real-Time Implementations

> **Status:** DRAFT · **Part VII — Digital Signal Processing**
> Closes Part VII. Maps the DSP of Ch. 19–21 and the pipeline of Ch. 11 onto
> hardware, under the latency/determinism constraints of Ch. 12. Citation keys
> resolve to [`../../citations/bibliography.json`](../../citations/bibliography.json).

The algorithms of Ch. 19–21 must run within a hard latency budget (Ch. 12),
deterministically, on hardware that is often small, power-limited, and
medical-grade. This chapter maps the pipeline onto **FPGA, DSP/embedded CPU, and
GPU** targets, explains the data-rate funnel that makes real-time EMT tractable,
and covers the fixed-point/numerical and verification concerns specific to a
safety-relevant real-time system.

---

## 22.1 The data-rate funnel (recap and why it dictates partitioning)

The pipeline (Ch. 11) is a funnel: the ADC produces the **highest** data rate
(oversampled Σ-Δ streams, Ch. 18); synchronous detection (Ch. 20) collapses each
channel to a few amplitudes per frame; the solver and estimator (Parts VIII,
Ch. 21) operate on that tiny reduced dataset at the pose rate. Partitioning
follows the funnel:

| Stage | Data rate | Compute character | Natural target |
|---|---|---|---|
| Demod / lock-in / FFT (Ch. 20) | highest | fixed, parallel, streaming | **FPGA** (or DSP) |
| Decimation / filtering (Ch. 18/20) | high→medium | streaming FIR/CIC | **FPGA/DSP** |
| Calibration / coupling matrix (Ch. 11 §11.2) | low | table lookup + linear algebra | FPGA or **CPU** |
| Solver (LM/Gauss-Newton, Ch. 23) | low | iterative, branching | **CPU / GPU** |
| State estimator / fusion (Ch. 21) | low | matrix algebra, sequential | **CPU** |

This is why a high-channel-count tracker is feasible on modest hardware: the
expensive, branchy nonlinear work happens only on the heavily decimated data.

## 22.2 FPGA implementations

FPGAs are the natural home for **Stage 1** (demodulation):

- **Deterministic, parallel, streaming.** A lock-in or FFT per channel runs at
  the sample rate with fixed, data-independent latency — exactly the determinism
  Ch. 12 §12.4 demands. Many channels run in parallel (one datapath each).
- **Tight ADC coupling.** Direct interface to Σ-Δ modulators, on-fabric
  decimation (CIC + FIR), and generation of the coherent reference (Ch. 10)
  keep the high-rate path off the CPU bus.
- **Cost:** development effort, fixed-point design (§22.4), and limited
  flexibility versus software.

## 22.3 Embedded CPU/DSP and GPU

- **Embedded CPU / DSP core** runs the **solver and estimator** (Stages 2–3):
  iterative nonlinear least squares (Ch. 23), the EKF/UKF (Ch. 21), and the host
  API. A real-time OS (or bare-metal with bounded loops) provides predictable
  scheduling. For most clinical trackers (one or a few sensors), a modern
  embedded CPU is ample for the per-frame solve.
- **GPU** becomes relevant for **massive parallelism**: many simultaneous sensors
  (catheter baskets, electrode arrays), large transmitter arrays
  ([@plotkin2003]), particle filters with many particles (Ch. 21 §21.4), or
  field-map / ML distortion-correction inference (Ch. 27). GPUs add latency and
  power, so they suit high-throughput or research configurations more than
  single-sensor low-latency loops.

The partition is not fixed: a small system may do everything on one SoC
(FPGA fabric + hard CPU cores), which is increasingly the norm.

## 22.4 Numerical precision: fixed vs. floating point

- **Fixed-point** on the FPGA front end: efficient and deterministic, but the
  designer must manage word growth and rounding through the lock-in/decimation so
  quantization in the *processing* does not spoil the ADC's hard-won ENOB
  (Ch. 18). The wide dynamic range (Ch. 9 §9.6) makes scaling/headroom analysis
  essential.
- **Floating-point** for the solver/estimator: the dipole forward model and its
  Jacobian span many orders of magnitude (the $1/r^3$ and $r^{-4}$ derivatives),
  so single/double precision avoids conditioning problems in the matrix solves
  (Ch. 24). A common, robust split is **fixed-point streaming front end →
  floating-point nonlinear back end**.

## 22.5 Meeting the latency and determinism budget

Implementing Ch. 12's requirements concretely:

- **Bounded work per frame.** Cap solver iterations; on non-convergence at a
  poorly conditioned pose (Ch. 24), output the predicted pose with an inflated
  covariance and a quality flag rather than overrunning the time budget.
- **Pipelining vs. latency.** Front-end pipelining raises throughput but adds
  fixed latency; the decimation-filter group delay (Ch. 18) is usually the
  largest front-end latency term and must be counted in eq. (12.1).
- **Acquisition timestamping** at the ADC (Ch. 12 §12.4) so fusion (Ch. 21) and
  the host can compensate fixed transport delays and align modalities.
- **Jitter of the *output* stream** (frame-to-frame timing) matters for control
  loops and fusion as much as average latency; FPGA scheduling of the front end
  keeps it low.

## 22.6 Verification of the real-time system

A safety-relevant tracker requires more than "it runs":

- **Bit-exact / model-in-the-loop testing.** Validate the FPGA/fixed-point
  datapath against a floating-point reference model on recorded/synthetic data,
  so the implementation provably matches the designed algorithm.
- **Worst-case timing analysis.** Demonstrate the bounded worst-case latency
  (not just average) required by Ch. 12 §12.4 and the regulatory posture of
  Ch. 29.
- **Fault behavior.** Verify graceful degradation (flagging, covariance
  inflation) under saturation, distortion spikes, and dropped frames — these are
  the conditions where naive implementations fail silently.

> **Takeaway.** Real-time EMT is an exercise in putting each computation where the
> data rate and determinism demand it: streaming, fixed-latency demodulation in
> hardware; flexible, floating-point, bounded-iteration estimation in software.
> The funnel (§22.1) is what makes the whole thing fit a clinical latency budget.

---

## Open questions / to verify
- Add a concrete resource/latency estimate (FPGA DSP-slice count, cycles) for a
  representative multi-channel lock-in, with assumptions.
- Source which commercial systems use FPGA vs. SoC vs. GPU back ends (Ch. 28)
  with citations rather than assertion.
- Provide a fixed-point word-growth analysis for the lock-in/decimation chain as
  a worked example (Phase 5).

## Sources cited
- [@plotkin2003] large transmitter arrays motivating parallelism. Real-time/
  numerical practice cross-referenced to Ch. 11, 12, 18, 23, 24; estimator from
  Ch. 21.
