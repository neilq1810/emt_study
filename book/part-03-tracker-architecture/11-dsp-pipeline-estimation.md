# Chapter 11 — DSP Pipeline & Estimation (Architecture View)

> **Status:** DEEPENED (awaiting review) · **Part III — Tracker Architecture**
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

**Quantifying the Stage-3 amplification.** The mapping is the inverse Jacobian
(Ch. 24). Two concrete anchors from the deepened solver chapters: near mid-volume
a fractional measurement error $\varepsilon$ produces a *range* error of only
$\sim(r/3)\varepsilon$ — the cube-root forgiveness of Ch. 25's worked example (a
0.2% gain error → 0.2 mm at $z=0.3$ m). But the amplification is **pose-dependent
and grows steeply toward the edge**: the CRLB scales as $z^4$ (Ch. 24 §24.5), so
the *same* $\varepsilon$ yields several-fold larger pose error at the volume
boundary, and near an observability null (a 5-DOF roll direction, Ch. 13) it
diverges. The Phase-6 *error-propagation* tool plots this amplification
($\kappa(\mathbf J)$ vs. range) directly. The lesson for the pipeline: Stage 3 is
not a fixed "gain" — it is a geometry-dependent amplifier, which is why pose
error must be reported *with* its pose-dependent covariance (§11.6), not as a
single accuracy number.

This is why the error budget (Ch. 25) is assembled *through the pipeline*, not
per-component in isolation, and why uncertainty quantification (Ch. 24) belongs
to the solver, not bolted on afterward.

## 11.6 The data contract: propagate covariances, not just values

The single most important architectural discipline in the pipeline is that **each
stage outputs a value *and* its covariance**, and the next stage consumes both.
The pipeline is therefore a covariance-propagation chain that exactly mirrors the
value chain:

$$
\underbrace{\mathbf R_a}_{\text{amplitude cov (Stage 1)}}
\ \xrightarrow{\text{calibrate}}\
\underbrace{\mathbf R_M}_{\text{coupling cov (Stage 2)}}
\ \xrightarrow{\text{invert}}\
\underbrace{\mathbf P = (\mathbf J^\top\mathbf R_M^{-1}\mathbf J)^{-1}}_{\text{pose cov (Stage 3) = CRLB}}.
$$

- **Stage 1** produces $\mathbf R_a$ — the amplitude noise covariance, set by the
  effective noise bandwidth ($\propto1/\tau$, Ch. 20) and the upstream sensor/AFE/
  ADC floor (Parts IV–VI). It is (nearly) diagonal and channel-dependent.
- **Stage 2** transforms it: per-channel gains scale $\mathbf R_a$, and *every*
  calibration constant carries its own uncertainty that adds to $\mathbf R_M$
  (Ch. 26). Crucially, calibration can introduce **correlations** (a shared
  field-map residual couples channels), so $\mathbf R_M$ is *not* diagonal — and
  treating it as diagonal under-weights the better channels and biases the solve.
- **Stage 3** maps $\mathbf R_M$ to the pose covariance $\mathbf P$ via the
  inverse Fisher information — which is exactly the **CRLB** (Ch. 24, eq. 24.1).
  Feeding the *correct* $\mathbf R_M$ (not an identity weight) is what makes the
  estimate efficient (Ch. 23 §23.2).

This is why the solver weights by $\mathbf R_M^{-1}$ (Ch. 23) and why the Kalman
filter consumes $\mathbf P$ as its measurement covariance (Ch. 21): the whole
chain is one consistent uncertainty calculation. A pipeline that passes bare
numbers between stages — amplitudes without $\mathbf R_a$, a pose without
$\mathbf P$ — throws away the information needed to weight, fuse, and flag
correctly, and is the most common architectural mistake in homegrown trackers.

### Failure modes (per stage)
- **Stage 1:** residual crosstalk/leakage (Ch. 19) appears as a *correlated*
  amplitude bias, not white noise — mis-modeled if $\mathbf R_a$ is assumed
  diagonal.
- **Stage 2:** uncorrected distortion or stale calibration injects a
  pose-dependent bias the solver cannot detect from one frame (needs fusion/
  consistency, Ch. 21).
- **Stage 3:** divergence/local-minimum at a poorly conditioned pose (Ch. 23/24);
  guarded by the closed-form seed, bounded iterations, and the eigenvalue-ratio
  consistency check (Ch. 23 §23.5).

---

## Open questions / to verify
- ✅ **Resolved:** Stage-3 amplification is now quantified (§11.5, cube-root
  near-field, $z^4$ edge growth, Phase-6 tool); the closed-form $\mathbf M^\top\mathbf M$
  initializer is **derived and machine-verified** in Ch. 23 §23.5
  (`sim_closed_form_init`). Remaining: a Phase-5 notebook propagating
  $\mathbf R_a\!\to\!\mathbf R_M\!\to\!\mathbf P$ end-to-end for a concrete frame.

## Sources cited
- [@raab1979] predictor/corrector recursive estimation and linearization.
  Covariance propagation / CRLB from Ch. 24; calibration from Ch. 26; detailed
  algorithms cross-referenced to Parts VII–VIII.
