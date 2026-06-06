# Chapter 11 — DSP Pipeline & Estimation (Architecture View)

> **Status:** DRAFT · **Part III — Tracker Architecture**
> Architecture-level overview; the algorithms live in Part VII (Ch. 19–22) and
> Part VIII (Ch. 23–24). Citation keys resolve to
> [`../../citations/bibliography.json`](../../citations/bibliography.json).

This chapter traces the data path from ADC samples to a pose estimate at the
*block* level, so the reader has a map before the detailed algorithm chapters.
The pipeline has three conceptual stages, each a well-defined estimation
problem: **(1) samples → channel amplitudes**, **(2) amplitudes → coupling
matrix**, **(3) coupling matrix → pose**. Keeping these stages distinct is the
single most useful organizing idea in EMT signal processing, because each stage
has its own noise model, its own failure modes, and its own place in the error
budget (Ch. 25).

---

## 11.1 Stage 1 — samples to channel amplitudes

**Input:** a stream of ADC samples from each sensor axis (Ch. 18).
**Output:** for each (transmit axis $i$, sense axis $j$) pair, an estimated
amplitude $\hat{a}_{ij}$ (and phase, if coherent).

This is the **demodulation / amplitude-estimation** stage and it is where the
multiplexing scheme of Ch. 10 is undone:

- **Coherent / lock-in (Ch. 20):** multiply by the reference, low-pass filter,
  read the in-phase (and quadrature) DC value. Equivalent to a single-bin DFT at
  the excitation frequency; gives the optimal (matched-filter) amplitude
  estimate for a known-frequency tone in white noise.
- **FFT / multi-bin:** for FDM, an FFT separates the per-axis frequencies in one
  transform; bin amplitudes are the channel amplitudes.
- **TDM gating:** select the settled portion of each time slot, then integrate.

The dominant performance metric here is the **effective noise bandwidth**:
longer integration → lower noise but lower update rate (the rate-vs-accuracy
trade of Ch. 10 §10.5). The output amplitudes inherit the sensor/AFE/ADC noise
(Parts IV–VI) plus any residual crosstalk from imperfect channel separation.

## 11.2 Stage 2 — amplitudes to the coupling matrix

**Input:** the $\hat{a}_{ij}$.
**Output:** the calibrated $3\times3$ (or larger) coupling matrix $\hat{\mathbf{M}}$
of Ch. 5 (eq. 5.6).

This stage applies the **calibration** (Part X): per-channel gain/phase, sensor
effective-area constants, frequency-dependent corrections (for FDM), and any
distortion/field-map correction (Ch. 26–27). The forward model of Ch. 5–7 is
what these amplitudes will be compared against in Stage 3, so the calibration
here must make the measured $\hat{\mathbf{M}}$ commensurate with the model's
predicted $\mathbf{M}(\mathbf{r},\mathbf{R})$. Errors that are *multiplicative
and stable* (gains) are handled here cleanly; errors that are *spatially
structured* (distortion) require the field-map machinery and are the hard part.

## 11.3 Stage 3 — coupling matrix to pose

**Input:** $\hat{\mathbf{M}}$.
**Output:** pose $(\mathbf{r},\mathbf{R})$ — 5 or 6 DOF — with a covariance.

This is the **inverse problem** (Part VIII). At the architecture level, the key
choices are:

- **Initialization vs. tracking.** A *closed-form* initializer exploits the
  eigenstructure of $\mathbf{M}$ (Ch. 5 §5.4: the rotation-invariant
  $\mathbf{M}^{\top}\mathbf{M}$ exposes $\hat{\mathbf{r}}$ and $r$) to seed a
  *nonlinear iterative* refiner (Levenberg–Marquardt, Ch. 23). The
  predictor/corrector structure pioneered by Raab et al. — linearizing about the
  previous estimate — is the recursive form used during continuous tracking
  [@raab1979].
- **Per-sample solve vs. recursive estimate.** A pure per-sample solver treats
  each frame independently; a **recursive state estimator** (Kalman/EKF/UKF,
  Ch. 21) fuses a motion model across frames to reduce noise and reject
  outliers, at the cost of dynamic lag.

The output must carry an **uncertainty** (covariance), both to be clinically
trustworthy and to drive fusion (Ch. 21) and observability monitoring (Ch. 24).

## 11.4 Where each subsystem lives (mapping to hardware)

The three stages map onto the real-time implementation choices of Ch. 22:

| Stage | Typical home | Why |
|---|---|---|
| 1 (demod) | **FPGA / DSP** near the ADC | high sample-rate, deterministic, parallel per-channel |
| 2 (calibration) | FPGA or embedded CPU | table lookups + linear algebra |
| 3 (solver/estimator) | **embedded CPU / GPU** | iterative nonlinear solve, branching |

The split is driven by the data-rate funnel: Stage 1 ingests the highest sample
rate and reduces it to a handful of amplitudes per frame; Stages 2–3 operate on
that reduced data at the pose update rate. This funnel is what makes real-time
EMT tractable on modest hardware (Ch. 12).

## 11.5 The pipeline as an error-propagation chain

Each stage adds and transforms error, and the stages are *not* independent:

1. **Stage 1** sets the stochastic noise on $\hat{a}_{ij}$ (→ amplitude SNR).
2. **Stage 2** can inject *bias* (calibration residual, uncorrected distortion).
3. **Stage 3** maps amplitude errors into pose errors through the **Jacobian of
   the forward model** — which can *amplify* error where the field gradient is
   weak (poor observability/conditioning, Ch. 24). A 1% amplitude error does
   *not* map to a 1% pose error; the gain depends on geometry.

This is why the error budget (Ch. 25) is assembled *through the pipeline*, not
per-component in isolation, and why uncertainty quantification (Ch. 24) belongs
to the solver, not bolted on afterward.

---

## Open questions / to verify
- Add a quantitative example of Stage-3 error amplification (Jacobian
  conditioning) at a poorly observable pose, backed by the Phase-5 solver
  simulation.
- Confirm the closed-form-initializer claim (eigenstructure of
  $\mathbf{M}^{\top}\mathbf{M}$) against a primary source and add to Ch. 23.

## Sources cited
- [@raab1979] predictor/corrector recursive estimation and linearization;
  detailed algorithms cross-referenced to Parts VII–VIII.
