# Chapter 24 — Conditioning, Observability & Uncertainty

> **Status:** DRAFT · **Part VIII — Position Solvers**
> Closes Part VIII. Builds on Ch. 23 (solver) and feeds the error budget (Ch. 25)
> and fusion (Ch. 21). Citation keys resolve to
> [`../../citations/bibliography.json`](../../citations/bibliography.json).

A pose solver can converge to the right answer in one part of the working volume
and be hopelessly uncertain in another — using the *same* hardware and the *same*
algorithm. The difference is **geometry**: how informative the measurement is
about each pose parameter. This chapter develops the tools that quantify and
predict that — **observability/identifiability** (can the pose be determined at
all?), **conditioning** (how sensitively does pose error amplify measurement
error?), **convergence** (will the solver get there?), and **uncertainty
quantification** (the covariance and the Cramér–Rao bound). Together they explain
*why* accuracy varies across the volume and turn a point estimate into a
trustworthy measurement.

---

## 24.1 Observability and identifiability

A pose parameter is **observable** if the measurement changes when it changes —
formally, if it appears in the Jacobian $\mathbf J=\partial h/\partial\mathbf x$
(Ch. 23) with nonzero sensitivity. Failures of observability in EMT are concrete,
not abstract:

- **The 5-DOF roll null (Ch. 13 §13.1).** For a single-element sensor, rotation
  about its own axis leaves every measurement unchanged: that DOF is structurally
  **unobservable**, so $\mathbf J$ is rank-deficient in that direction. No solver
  recovers it — only a second element or fusion does (Ch. 21).
- **Dipole sign/mirror ambiguities.** The bare dipole forward model maps distinct
  poses to identical measurements (e.g. $\mathbf m\to-\mathbf m$ symmetries),
  making them **unidentifiable** without priors/continuity (Ch. 23 §23.4).
- **Weak-gradient regions.** Where the field is locally near-uniform (Ch. 5 §5.7),
  position changes barely move the measurement — *technically* observable but
  *practically* nearly singular.

The diagnostic is the **rank and singular values of $\mathbf J$** (or of the
Fisher information $\mathbf J^\top\mathbf R^{-1}\mathbf J$, §24.4): a zero singular
value = unobservable direction; a small one = weakly observable. Mapping these
across the volume produces an **observability map** that should drive generator/
sensor design (Ch. 9) and working-volume specification.

## 24.2 Conditioning and numerical stability

Even when fully observable, the inverse can be **ill-conditioned**. The condition
number of the Fisher/normal-equations matrix,

$$
\kappa = \frac{\sigma_{\max}(\mathbf J)}{\sigma_{\min}(\mathbf J)},
$$

bounds how measurement error amplifies into pose error: a measurement error of
relative size $\epsilon$ can produce pose error up to $\sim\kappa\,\epsilon$
[@nocedal2006]. EMT consequences:

- **The $1/r^3$ law hurts conditioning at range.** Sensitivity to position falls
  as the field weakens and flattens, so $\sigma_{\min}$ shrinks toward the volume
  edge — $\kappa$ grows, and the same amplitude noise yields much larger pose
  error far out. This is the quantitative form of "accuracy degrades with
  distance."
- **Mixed units.** Position (metres) and orientation (radians) live in one state
  vector; naive scaling inflates $\kappa$ artificially. **Preconditioning**
  (non-dimensionalizing, scaling columns of $\mathbf J$) is necessary for honest
  conditioning and stable solves.
- **Numerical practice.** Solve the linearized step via **QR or SVD of $\mathbf J$**
  rather than forming $\mathbf J^\top\mathbf J$ (which squares the condition
  number); LM's damping $\lambda\mathbf D$ also regularizes near-singular steps
  (Ch. 23) [@nocedal2006].

This is exactly the "1% amplitude error ≠ 1% pose error" amplification flagged in
Ch. 11 §11.5: the amplification factor *is* (loosely) $\kappa$, and it is
pose-dependent.

## 24.3 Convergence and initialization

A nonlinear solver converges only from within a **basin of attraction**:

- **Initialization** (Ch. 23 §23.4): the closed-form seed or the previous pose
  must lie in the correct basin, or LM converges to a mirror/local solution.
  Continuity (tracking) is the strongest defense; re-acquisition is the riskiest
  moment.
- **Damping/trust region** (LM) enlarges the reliable step region versus raw
  Gauss–Newton, trading speed for robustness [@marquardt1963; @nocedal2006].
- **Bounded iterations** (Ch. 22 §22.5): in real time, cap iterations and, on
  non-convergence (often a symptom of poor conditioning or distortion), emit the
  predicted pose with inflated covariance and a quality flag rather than a wrong
  confident answer.

Convergence behavior is itself pose-dependent: ill-conditioned regions have
flatter, more elongated cost valleys that slow convergence and widen the
ambiguity risk — so §24.1–24.3 are one coupled story.

## 24.4 Uncertainty quantification: covariance and the CRLB

The estimate is incomplete without its uncertainty. Two linked tools [@kay1993]:

- **Fisher information & the Cramér–Rao lower bound (CRLB).** For the Gaussian
  model (23.1), the Fisher information is
  $\mathbf F_{\!I} = \mathbf J^\top\mathbf R^{-1}\mathbf J$, and **no unbiased
  estimator can do better than**
  $$
  \operatorname{Cov}(\hat{\mathbf x}) \succeq \mathbf F_{\!I}^{-1} = (\mathbf J^\top\mathbf R^{-1}\mathbf J)^{-1}.
  \tag{24.1}
  $$
  The CRLB (24.1) is the **theoretical accuracy limit** for a given geometry and
  noise — a design tool: evaluate it across the volume to predict achievable
  accuracy *before building anything*, and to compare generator/sensor designs
  (Ch. 9, Ch. 13) on equal footing. Its diagonal gives per-axis position/
  orientation variance; its eigenvectors give the error ellipsoid's axes.
- **Estimator covariance.** The MLE asymptotically attains the CRLB
  [@kay1993], so the solver's output covariance
  $\approx(\mathbf J^\top\mathbf R^{-1}\mathbf J)^{-1}$ at the solution is both the
  reported uncertainty *and* (near) the best possible. This is the covariance
  handed to the Kalman filter as $\mathbf R$/innovation weighting (Ch. 21) and to
  the error budget (Ch. 25).

**Consistency caveat.** The linearized covariance (24.1) is a *local* (Gaussian)
approximation; near ambiguities, weak observability, or strong nonlinearity it
**understates** true uncertainty (the posterior is non-Gaussian/multimodal —
hence particle filters, Ch. 21 §21.4). A covariance that claims high confidence in
a poorly observable region is dangerous; consistency checks (NIS, Ch. 21 §21.6)
and the observability map (§24.1) guard against believing it.

## 24.5 Synthesis: why accuracy varies across the volume
Sections 24.1–24.4 are one causal chain:

$$
\underbrace{\text{geometry} \to \mathbf J}_{\S24.1}\ \to\ \underbrace{\sigma_{\min}(\mathbf J),\ \kappa}_{\S24.1\text{–}24.2}\ \to\ \underbrace{(\mathbf J^\top\mathbf R^{-1}\mathbf J)^{-1}}_{\S24.4\ \text{CRLB}}\ =\ \text{pose uncertainty}.
$$

Combined with the noise→pose relation of Ch. 15 §15.4, this is the complete
recipe for predicting EMT accuracy at any pose: **measurement noise (Parts IV–VII)
× integration (Ch. 11/20) ÷ signal ($m_t/r^3$, Ch. 9) × geometric conditioning
(this chapter) = uncertainty.** It tells the designer where the system is good,
where it is marginal, and how to fix it (more moment, better-conditioned coil
geometry, longer integration, fusion). Part IX assembles these into a full error
budget.

---

## Open questions / to verify
- Produce CRLB maps over a working volume for a concrete generator/sensor design
  (Phase 5), and validate against Monte Carlo solver runs (Ch. 25) — the planned
  "error propagation / uncertainty" interactive modules.
- Quantify the conditioning improvement from a second (askew) sensor element vs.
  EM+IMU fusion for the 5→6 DOF case (ties Ch. 13, 21).
- Add a worked preconditioning/SVD example showing the $\kappa$ reduction.

## Sources cited
- [@kay1993] Fisher information, CRLB, MLE efficiency. [@nocedal2006]
  conditioning, SVD/QR, trust region. [@marquardt1963] LM regularization.
  Observability links to Ch. 13; error budget to Ch. 25.
