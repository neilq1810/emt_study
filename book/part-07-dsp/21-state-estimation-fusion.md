# Chapter 21 — State Estimation & Sensor Fusion

> **Status:** DRAFT · **Part VII — Digital Signal Processing**
> Builds on Ch. 11 (pipeline), Ch. 20 (amplitudes). Complements the per-frame
> solver of Part VIII with across-time estimation. Citation keys resolve to
> [`../../citations/bibliography.json`](../../citations/bibliography.json).

The position solver (Part VIII) returns a pose per measurement frame. But poses
arrive in a time series from a physically continuous, inertia-bearing object, and
they are noisy and occasionally corrupted (distortion, outliers). **Recursive
state estimation** exploits the temporal structure — a motion model plus a
measurement model — to produce smoother, lower-latency, more robust pose, and to
**fuse** EM with complementary sensors (IMU, optical). This chapter develops the
Kalman filter and its nonlinear extensions for EMT, then the fusion architectures
that define much of the modern and future field.

---

## 21.1 Why recurse: the state-space view

Model the tracked object with a state $\mathbf x_k$ (pose, and usually velocity)
evolving by a **process model** and observed by a **measurement model**:

$$
\mathbf x_k = f(\mathbf x_{k-1}) + \mathbf w_k,\qquad
\mathbf z_k = h(\mathbf x_k) + \mathbf v_k,
$$

with process noise $\mathbf w_k\sim\mathcal N(0,\mathbf Q)$ and measurement noise
$\mathbf v_k\sim\mathcal N(0,\mathbf R)$. For EMT, $\mathbf z_k$ may be the
coupling matrix $\hat{\mathbf M}$ (or the per-frame solved pose), and $h(\cdot)$
the forward model of Ch. 5–7. The recursive estimator maintains a **belief**
(mean + covariance) and updates it each frame — the modern descendant of the
predictor/corrector structure Raab et al. used in 1979 [@raab1979].

## 21.2 The Kalman filter (linear-Gaussian core)

For linear $f,h$ and Gaussian noise, the **Kalman filter** is the optimal
(minimum-mean-square-error) estimator [@kalman1960]. Its two steps:

**Predict:**
$$
\hat{\mathbf x}_k^- = \mathbf F\hat{\mathbf x}_{k-1},\qquad
\mathbf P_k^- = \mathbf F\mathbf P_{k-1}\mathbf F^\top + \mathbf Q.
$$
**Update:**
$$
\mathbf K_k = \mathbf P_k^-\mathbf H^\top(\mathbf H\mathbf P_k^-\mathbf H^\top + \mathbf R)^{-1},
$$
$$
\hat{\mathbf x}_k = \hat{\mathbf x}_k^- + \mathbf K_k(\mathbf z_k - \mathbf H\hat{\mathbf x}_k^-),\qquad
\mathbf P_k = (\mathbf I - \mathbf K_k\mathbf H)\mathbf P_k^- .
$$

The **Kalman gain** $\mathbf K_k$ optimally blends prediction and measurement by
their relative uncertainties: trust the measurement when $\mathbf R$ is small,
trust the model when $\mathbf P_k^-$ is small. The covariance $\mathbf P_k$ is a
*reported uncertainty* — exactly what clinical trust and fusion require (Ch. 24)
[@barshalom2001].

## 21.3 Nonlinear extensions: EKF and UKF

EMT's measurement model is **strongly nonlinear** (the $1/r^3$ dipole coupling,
Ch. 5), so the linear KF does not apply directly. Two standard remedies
[@barshalom2001; @julier2004]:

- **Extended Kalman Filter (EKF).** Linearize $f,h$ about the current estimate
  via Jacobians ($\mathbf F=\partial f/\partial x$, $\mathbf H=\partial h/\partial x$)
  and apply the KF equations. Cheap and ubiquitous, but the linearization can
  bias or diverge when nonlinearity is strong or the estimate is poor — a real
  risk near poorly observable poses (Ch. 24).
- **Unscented Kalman Filter (UKF).** Propagate a deterministic set of **sigma
  points** through the *true* nonlinear $f,h$ and reconstruct mean/covariance via
  the **unscented transform** [@julier2004]. No Jacobians, accuracy to higher
  order, similar cost — often more robust than EKF for the dipole nonlinearity.
  The UKF is frequently the better default for EMT pose tracking. (conf: med —
  general estimation result; EMT-specific superiority should be benchmarked, see
  *Open questions*.)

## 21.4 Particle filtering

When the posterior is **multimodal** — e.g. ambiguities (the roll/sign
ambiguities of 5-DOF sensors, Ch. 13; mirror solutions of the dipole inverse) or
heavy-tailed outliers from distortion — a Gaussian belief is inadequate. A
**particle filter** represents the posterior by weighted samples propagated
through the nonlinear models, handling arbitrary distributions and multimodality
[@barshalom2001]. The cost is computational (many particles) and the risk is
sample impoverishment; particle filters are used in EMT mainly for
initialization, ambiguity resolution, or research systems rather than
high-rate production loops (conf: med).

## 21.5 Sensor fusion: EM + IMU + optical

Fusion is where EMT's weaknesses are covered by complementary modalities, all
combined in one estimator (typically an EKF/UKF whose state includes the shared
pose and per-sensor biases) [@barshalom2001]:

| Modality | Strengths | Weaknesses | Fusion role |
|---|---|---|---|
| **EM** | absolute, drift-free, no line-of-sight, small sensor | slower, distortion-prone | absolute reference / drift correction |
| **IMU** | high rate, low latency, distortion-immune | drifts (integration) | smooths & predicts between EM frames |
| **Optical** | very accurate, drift-free | occludable (line-of-sight) | bounds error when visible |

Key fusion ideas specific to EMT:

- **Complementary frequency split.** Let the IMU carry high-frequency motion
  (low latency) and EM carry low-frequency/absolute truth (drift-free); the
  filter fuses them so the result is simultaneously fast *and* drift-free —
  directly attacking the latency trilemma of Ch. 12.
- **Distortion detection.** A disagreement between EM and IMU/optical that
  exceeds their combined covariance flags **field distortion** (Ch. 6) in real
  time — the estimator can then down-weight EM (inflate $\mathbf R$) until the
  distortion passes. This is one of the most powerful practical uses of fusion.
- **5-DOF → 6-DOF.** An IMU's gyro can supply the roll a single-coil EM sensor
  cannot (Ch. 13 §13.4), yielding 6-DOF from a 5-DOF EM sensor + IMU.
- **Time alignment is critical.** Fusing a fresh IMU sample with a stale EM
  sample injects error ∝ skew × velocity (Ch. 12 §12.5); accurate timestamping
  and time-base alignment are prerequisites, not refinements.

## 21.6 Tuning, consistency, and failure modes
- **$\mathbf Q,\mathbf R$ tuning** sets the smoothing/latency trade: large
  $\mathbf R$ (or small $\mathbf Q$) → smoother but laggier (Ch. 12 §12.3). These
  must reflect the *real* measurement noise from the budget (Ch. 25), not be
  fudge factors.
- **Consistency checks** (normalized innovation squared, NIS) detect filter
  divergence and outliers [@barshalom2001]; gating rejects measurements whose
  innovation is implausibly large (distortion spikes).
- **Failure modes:** EKF divergence under strong nonlinearity/poor init;
  over-smoothing hiding real motion; mis-tuned covariance producing
  overconfident (dangerous) or useless (too loose) estimates. The reported
  covariance must be *consistent* to be trustworthy for clinical use.

---

## Open questions / to verify
- Benchmark EKF vs. UKF vs. particle filter on the EMT dipole model (Phase 5
  simulation) and report accuracy/robustness/cost; cite results here.
- Add a worked EM+IMU fusion example with explicit state, $\mathbf Q/\mathbf R$,
  and a distortion-detection demonstration.
- Source peer-reviewed EM+IMU and EM+optical clinical fusion studies for Ch. 29
  and cross-reference.

## Sources cited
- [@kalman1960] Kalman filter. [@julier2004] UKF/unscented transform.
  [@barshalom2001] EKF, particle filtering, fusion, consistency, CRLB.
  [@raab1979] historical predictor/corrector precedent.
