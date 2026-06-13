# Chapter 21 — State Estimation & Sensor Fusion

> **Status:** DEEPENED (awaiting review) · **Part VII — Digital Signal Processing**
> Builds on Ch. 11 (pipeline), Ch. 20 (amplitudes), Ch. 23–24 (the per-frame
> solver and its Jacobian/covariance). Citation keys resolve to
> [`../../citations/bibliography.json`](../../citations/bibliography.json).

The position solver (Part VIII) returns a pose per measurement frame. But poses
arrive as a time series from a physically continuous, inertia-bearing object, and
they are noisy and occasionally corrupted (distortion, outliers). **Recursive
state estimation** exploits the temporal structure — a motion model plus a
measurement model — to produce smoother, lower-latency, more robust pose, to
report calibrated **uncertainty**, and to **fuse** EM with complementary sensors
(IMU, optical). This chapter develops the Kalman filter and its nonlinear
extensions *as they must actually be built for 6-DOF EMT* — including the
**error-state formulation** that is mandatory for orientation — then particle
filtering, the fusion architectures, and the consistency tests without which a
reported covariance cannot be trusted.

---

## 21.1 The state-space view and the EMT state vector

Model the tracked object with a state $\mathbf x_k$ evolving by a **process
model** and observed by a **measurement model**:

$$
\mathbf x_k = f(\mathbf x_{k-1}) + \mathbf w_k,\qquad
\mathbf z_k = h(\mathbf x_k) + \mathbf v_k,
\tag{21.1}
$$

with process noise $\mathbf w_k\sim\mathcal N(0,\mathbf Q)$ and measurement noise
$\mathbf v_k\sim\mathcal N(0,\mathbf R)$. For 6-DOF EMT a representative state is

$$
\mathbf x = \big[\,\underbrace{\mathbf p}_{3},\ \underbrace{\mathbf v}_{3},\ \underbrace{\mathbf q}_{\text{orientation}},\ \underbrace{\boldsymbol\omega}_{3}\ (,\ \mathbf b_a,\mathbf b_g\ \text{if IMU})\big],
$$

i.e. position, linear velocity, orientation, angular velocity, and (when fused
with an IMU) accelerometer/gyro biases. The measurement $\mathbf z_k$ is either
the calibrated coupling matrix $\hat{\mathbf M}$ (the *tight* coupling, where
$h(\cdot)$ is the forward model of Ch. 5–7) or the per-frame solved pose (the
*loose* coupling). The recursive estimator maintains a **belief**
(mean + covariance) and updates it each frame — the modern descendant of the
predictor/corrector structure Raab et al. used in 1979 [@raab1979].

**Process models.** Common choices: constant-velocity (CV, white-noise
acceleration), constant-acceleration (CA), and for orientation a
constant-angular-velocity model; the unmodeled dynamics are absorbed into
$\mathbf Q$. The CV model's discrete process noise for a position/velocity block is
$\mathbf Q = q\left[\begin{smallmatrix}\Delta t^3/3 & \Delta t^2/2\\ \Delta t^2/2 & \Delta t\end{smallmatrix}\right]$
with $q$ the acceleration PSD — the same form used in the Phase-6 Kalman
explorer. The choice of $q$ is the agility knob (§21.8).

## 21.2 The Kalman filter (linear-Gaussian core)

For linear $f,h$ and Gaussian noise, the **Kalman filter** is the optimal
(minimum-mean-square-error) estimator [@kalman1960; @barshalom2001]:

**Predict:** $\hat{\mathbf x}_k^- = \mathbf F\hat{\mathbf x}_{k-1}$,
$\ \mathbf P_k^- = \mathbf F\mathbf P_{k-1}\mathbf F^\top + \mathbf Q$.

**Update:**
$$
\mathbf S_k = \mathbf H\mathbf P_k^-\mathbf H^\top + \mathbf R,\quad
\mathbf K_k = \mathbf P_k^-\mathbf H^\top\mathbf S_k^{-1},
$$
$$
\hat{\mathbf x}_k = \hat{\mathbf x}_k^- + \mathbf K_k\,\boldsymbol\nu_k,\quad
\boldsymbol\nu_k = \mathbf z_k - \mathbf H\hat{\mathbf x}_k^-,\quad
\mathbf P_k = (\mathbf I - \mathbf K_k\mathbf H)\mathbf P_k^- .
$$

The **innovation** $\boldsymbol\nu_k$ and its covariance $\mathbf S_k$ are the
quantities that drive both gating (§21.8) and distortion detection (§21.7). The
Kalman gain optimally blends prediction and measurement by their relative
uncertainties. For numerical robustness, production filters use the **Joseph
form** of the covariance update or a square-root/UD factorization to keep
$\mathbf P_k$ symmetric positive-definite [@barshalom2001].

## 21.3 The Extended Kalman Filter (EKF)

EMT's measurement model is strongly nonlinear (the $1/r^3$ dipole coupling,
Ch. 5), so the linear KF does not apply directly. The EKF linearizes about the
current estimate using the **measurement Jacobian**
$\mathbf H_k = \left.\partial h/\partial\mathbf x\right|_{\hat{\mathbf x}_k^-}$ —
*the same Jacobian* that defines conditioning and the CRLB in Ch. 24 — and applies
the KF equations with $\boldsymbol\nu_k = \mathbf z_k - h(\hat{\mathbf x}_k^-)$.
Cheap and ubiquitous, but the linearization can **bias or diverge** when (i) the
nonlinearity is strong over the covariance's spread (near the generator, where the
field gradient is steep), or (ii) the estimate is poor (after re-acquisition, or
in the weakly observable far field, Ch. 24). Divergence manifests as an
over-confident $\mathbf P$ with growing innovations — caught by the consistency
tests of §21.8.

## 21.4 The Unscented Kalman Filter (UKF)

Rather than linearize, the UKF propagates a deterministic set of **sigma points**
through the *true* nonlinear $f,h$ and reconstructs the mean/covariance — the
**unscented transform** [@julier2004]. For an $n$-dimensional state with mean
$\hat{\mathbf x}$ and covariance $\mathbf P$, form $2n+1$ points with scaling
$\lambda = \alpha^2(n+\kappa) - n$:

$$
\boldsymbol\chi_0 = \hat{\mathbf x},\quad
\boldsymbol\chi_i = \hat{\mathbf x} \pm \big(\sqrt{(n+\lambda)\mathbf P}\big)_i,\ i=1\dots n,
$$
$$
W^m_0 = \frac{\lambda}{n+\lambda},\quad
W^c_0 = W^m_0 + (1-\alpha^2+\beta),\quad
W^m_i = W^c_i = \frac{1}{2(n+\lambda)} .
$$

Propagate $\mathbf{\mathcal Y}_i = h(\boldsymbol\chi_i)$, then
$\hat{\mathbf z} = \sum_i W^m_i\mathbf{\mathcal Y}_i$,
$\mathbf S = \sum_i W^c_i(\mathbf{\mathcal Y}_i-\hat{\mathbf z})(\cdot)^\top + \mathbf R$,
$\mathbf P_{xz} = \sum_i W^c_i(\boldsymbol\chi_i-\hat{\mathbf x})(\mathbf{\mathcal Y}_i-\hat{\mathbf z})^\top$,
and gain $\mathbf K = \mathbf P_{xz}\mathbf S^{-1}$. The parameters
$\alpha$ (spread, $\sim10^{-3}$), $\kappa$ ($0$ or $3-n$), $\beta$ ($=2$ for
Gaussians) tune the point set. The UKF captures mean/covariance to second order
(vs. the EKF's first), needs **no Jacobians**, and at similar cost is often more
robust for the dipole nonlinearity — frequently the better default for EMT pose
tracking. (conf: med — general estimation result; an EMT-specific EKF-vs-UKF
benchmark is the planned Phase-5 study, §Open questions.)

## 21.5 Orientation done right: the error-state (multiplicative) filter

A subtle but **essential** point for 6-DOF EMT: orientation cannot be a naïve KF
state. A unit quaternion has four components with a norm constraint, so its
$4\times4$ covariance is singular (rank 3), and adding a Gaussian correction
breaks unit norm. The correct construction is the **error-state / multiplicative
Kalman filter (ESKF/MEKF)** [@sola2017]:

- Keep a **nominal** orientation $\mathbf q$ outside the filter state.
- Let the filter estimate a small **error rotation** $\delta\boldsymbol\theta\in\mathbb R^3$
  in the tangent space, with true orientation
  $\mathbf q_\text{true} = \mathbf q \otimes \delta\mathbf q$,
  $\delta\mathbf q \approx [\,1,\ \tfrac12\delta\boldsymbol\theta\,]$.
- The covariance is a proper $3\times3$ block on $\delta\boldsymbol\theta$ — no
  constraint, no singularity.
- After each update, **inject** the estimated $\delta\boldsymbol\theta$ into the
  nominal quaternion ($\mathbf q \leftarrow \mathbf q\otimes\delta\mathbf q$) and
  **reset** $\delta\boldsymbol\theta\to 0$.

This is how the solver's $SO(3)$ increment (Ch. 23 §23.3) and the recursive filter
share one consistent rotation representation. Skipping it — e.g. Euler angles in
the state — invites gimbal lock and inconsistent covariance, a common silent bug
in homegrown 6-DOF trackers. (conf: high — standard in attitude estimation
[@sola2017].)

## 21.6 Particle filtering

When the posterior is **multimodal** — the sign/mirror ambiguities of the dipole
inverse, the roll null of a 5-DOF sensor (Ch. 13), or heavy-tailed outliers from
distortion — a single Gaussian belief is inadequate. A **particle filter** (SIR)
represents the posterior by $N_p$ weighted samples
$\{\mathbf x^{(i)}, w^{(i)}\}$ propagated through the nonlinear models, with
weights updated by the likelihood $w^{(i)}\!\propto w^{(i)} p(\mathbf z_k\mid\mathbf x^{(i)})$
[@arulampalam2002]. Two practical realities:

- **Degeneracy & resampling.** Weights concentrate on a few particles over time;
  monitor the **effective sample size** $N_\text{eff} = 1/\sum_i (w^{(i)})^2$ and
  **resample** when it falls below a threshold (e.g. $N_p/2$) [@arulampalam2002].
- **Cost & impoverishment.** $N_p$ must grow with state dimension; resampling can
  collapse diversity. Particle filters are therefore used in EMT mainly for
  **initialization, ambiguity resolution, and research systems**, not high-rate
  production loops, where an ESKF/UKF with good initialization (Ch. 23 §23.4) is
  preferred. (conf: med.)

## 21.7 Sensor fusion: EM + IMU + optical

Fusion covers EMT's weaknesses with complementary modalities, combined in one
estimator (typically an ESKF whose state includes the shared pose and per-sensor
biases) [@barshalom2001; @sola2017]:

| Modality | Strengths | Weaknesses | Fusion role |
|---|---|---|---|
| **EM** | absolute, drift-free, no line-of-sight, small sensor | slower, distortion-prone | absolute reference / drift correction |
| **IMU** | high rate, low latency, distortion-immune | drifts (bias, integration) | propagate between EM frames; supply roll |
| **Optical** | very accurate, drift-free | occludable | bound error when visible |

**Architecture.** The standard pattern is an **error-state EKF with IMU
propagation**: the high-rate IMU drives the *predict* step (integrating
acceleration/angular rate, estimating biases $\mathbf b_a,\mathbf b_g$), and the
lower-rate EM (and optical, when available) provide *absolute updates* that arrest
IMU drift. This **complementary frequency split** — IMU for high-frequency motion
(low latency), EM for low-frequency/absolute truth (drift-free) — directly attacks
the latency trilemma (Ch. 12) and lets a 5-DOF EM coil + IMU gyro deliver 6-DOF
(the IMU supplies the missing roll, Ch. 13 §13.4).

**Time alignment is first-order.** Fusing a fresh IMU sample with a *stale* EM
sample injects error $\propto$ time-skew × velocity (Ch. 12 §12.5); accurate
acquisition timestamping and a common time base are prerequisites, not
refinements — a mis-aligned fusion is worse than EM alone.

**Distortion detection via the innovation.** The single most powerful practical
use of fusion: when EM disagrees with IMU/optical beyond their combined
covariance, the **normalized innovation squared**
$\text{NIS} = \boldsymbol\nu_k^\top\mathbf S_k^{-1}\boldsymbol\nu_k$ exceeds its
$\chi^2_m$ bound (e.g. the 95% point for $m$ measurement DOF), flagging **field
distortion** in real time. The estimator then **down-weights EM** (inflates
$\mathbf R$, or gates the update out) until the distortion passes — converting a
silent, dangerous error into a detected, managed one (Ch. 27 §27.4).

## 21.8 Consistency, tuning, smoothing, and failure modes

- **Consistency tests.** A filter is *consistent* if its actual errors match its
  claimed covariance. Test with the **NIS** (per-frame, $\chi^2_m$) and the
  **NEES** $=(\mathbf x-\hat{\mathbf x})^\top\mathbf P^{-1}(\mathbf x-\hat{\mathbf x})$
  ($\chi^2_n$, when truth is available, e.g. on a phantom) [@barshalom2001].
  A consistently-too-large NIS means $\mathbf P/\mathbf R$ are under-estimated
  (over-confident — dangerous); too-small means over-conservative.
- **$\mathbf Q/\mathbf R$ tuning** sets the smoothing/latency trade: large
  $\mathbf R$ (or small $\mathbf Q$) → smoother but laggier (Ch. 12 §12.3); these
  must reflect the *real* noise from the budget (Ch. 25), not be fudge factors.
- **Smoothing.** When some latency is tolerable (e.g. post-procedure review, or a
  fixed-lag buffer), a Rauch–Tung–Striebel smoother or fixed-lag smoother
  markedly reduces error by using future measurements — the offline counterpart
  to real-time filtering.

**Failure modes:** EKF divergence under strong nonlinearity/poor init (use UKF or
better seeding); naïve-quaternion inconsistency/gimbal lock (use the ESKF, §21.5);
over-smoothing hiding real motion; mis-tuned covariance producing overconfident
(dangerous) or useless (too-loose) estimates; particle impoverishment; and
time-skew in fusion. The reported covariance must be *consistent* (§21.8) to be
trustworthy for clinical use.

## 21.9 Multi-modal fusion in depth: complementarity and the integrated navigator

§21.7 introduced EM+IMU+optical; the deeper point is *why* it works: the modalities have
**complementary failure modes**, so fusion buys **robustness and observability**, not merely
noise averaging.

| Modality | Strength | Blind spot |
|---|---|---|
| **EM** | no line-of-sight — sees hidden tips | distortion (Ch. 6/27); degrades as $z^4$ (Ch. 24) |
| **Optical** | distortion-immune, high accuracy | needs line-of-sight; only external rigid bodies |
| **IMU** | high-rate, self-contained, no LoS | integration drift (bias) |
| **Robot kinematics** | strong motion prior, known tool base | flex/backlash |
| **Imaging (US/fluoro/CT)** | anatomical, near-truth registration | intermittent; dose/LoS-limited |

The fusion argument is that **each covers another's blind spot**: optical **anchors EM and
bounds its distortion** where LoS exists (giving the NIS distortion test of §21.8 an
independent reference), while EM **provides continuity when the optical marker is occluded**;
the IMU **bridges EM dropouts and supplies the roll** a 5-DOF sensor lacks (resolving the
roll null of §24.1 via the error-state filter, §21.5), while EM **bounds IMU drift**; the
robot's kinematics **tighten** the EM estimate and EM **corrects kinematic flex**.

**The observability payoff (tie to Ch. 24).** Each added modality appends rows to the
measurement Jacobian, which **lowers PDOP (§24.3)** and can resolve *both* layers of the
observability problem: the **local** 5-DOF roll null (§24.1) **and** the **global**
hemisphere/parity ambiguity (§24.7) — fusion is the general resolver named there. This makes
the fusion chapter and the observability chapter one story: more independent measurements →
fuller rank → a uniquely and well-conditioned pose.

**Architecture.** The **error-state filter** (§21.5) is the natural *integrated navigator*
(the multisensor-navigation framing of [@groves2013]): each modality enters as a measurement
with its **own $\mathbf R$ and its own timestamp** — so the **cross-modality sync of Ch. 10
§10.6 is a precondition**, and the filter must handle **asynchronous, out-of-sequence**
updates. The dividend is honest uncertainty: the **fused covariance** (Ch. 24/46) reflects
*which* modalities are currently contributing — tight when optical and EM agree, widening to
EM-only when the marker is occluded — which is exactly the reliability-tracking signal the
confidence display of Ch. 46 §46.6 renders to the clinician.

---

## Open questions / to verify
- Benchmark EKF vs. UKF vs. ESKF vs. particle filter on the EMT dipole model
  (Phase 5), reporting accuracy/robustness/cost and the EKF divergence boundary;
  cite results here.
- Add a worked EM+IMU error-state fusion example with explicit state,
  $\mathbf Q/\mathbf R$, IMU bias states, and a NIS-based distortion-detection
  demonstration (tie to the Phase-6 Kalman explorer).
- Source peer-reviewed EM+IMU and EM+optical *clinical* fusion studies for Ch. 29
  and cross-reference.

## Sources cited
- [@kalman1960] Kalman filter. [@julier2004] UKF/unscented transform.
  [@sola2017] error-state (multiplicative) orientation filter.
  [@arulampalam2002] particle filtering (SIR, degeneracy, resampling).
  [@barshalom2001] EKF, fusion, consistency (NIS/NEES), smoothing.
  [@groves2013] multisensor integrated navigation — the §21.9 integrated-navigator framing.
  [@raab1979] historical predictor/corrector precedent. Cross-modality timebase: Ch. 10 §10.6;
  observability payoff: Ch. 24 §24.1/§24.7; confidence display: Ch. 46 §46.6.
