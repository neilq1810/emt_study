# Chapter 23 — The Inverse Problem

> **Status:** DEEPENED (awaiting review) · **Part VIII — Position Solvers**
> Opens Part VIII. Consumes the coupling matrix $\hat{\mathbf M}$ from Ch. 11/20;
> conditioning & uncertainty follow in Ch. 24. Citation keys resolve to
> [`../../citations/bibliography.json`](../../citations/bibliography.json).

The forward model (Ch. 5–7) predicts the coupling matrix $\mathbf M$ from a known
pose. Tracking requires the **inverse**: given a measured $\hat{\mathbf M}$, find
the pose $(\mathbf r,\mathbf R)$ that produced it. Because the dipole coupling is
nonlinear in position (the $1/r^3$ and angular factors of Ch. 5) and orientation
lives on the manifold $SO(3)$, this is a nonlinear least-squares / maximum-
likelihood problem. This chapter derives the solvers from first principles —
Gauss–Newton, **Levenberg–Marquardt**, and an **explicit closed-form
initializer** from the coupling-matrix eigenstructure — then maximum likelihood /
MAP, $SO(3)$ parameterization and constraints, and **robust** outlier rejection.
Conditioning, observability, and uncertainty are deferred to Ch. 24. The
Phase-6 *position-solver visualizer* and Phase-5 Monte-Carlo back this chapter
with runnable code.

---

## 23.1 The measurement equation

Stack the calibrated measurements into a vector
$\mathbf z = \operatorname{vec}(\hat{\mathbf M})$ (nine entries for a single
triad–triad pair; $C$ entries per sensor axis for a $C$-coil generator, Ch. 19
§19.7) and the pose into $\mathbf x$ (3 position + 2 or 3 orientation, depending
on 5/6-DOF, Ch. 13). The forward model $h(\mathbf x)$ (Ch. 5 eq. 5.6) gives the
predicted measurement, so

$$
\mathbf z = h(\mathbf x) + \mathbf v,\qquad \mathbf v\sim\mathcal N(0,\mathbf R),
\tag{23.1}
$$

with $\mathbf v$ the measurement noise (Parts IV–VII) of covariance $\mathbf R$.
The solver inverts (23.1). Note $h$ is nonlinear and, for the bare dipole, has
**known ambiguities** — sign/mirror solutions and the 5-DOF roll null (Ch. 13) —
that the solver must resolve via initialization, constraints, or fusion (Ch. 21).

## 23.2 Least squares and maximum likelihood

The natural estimator minimizes the whitened residual:

$$
\hat{\mathbf x} = \arg\min_{\mathbf x}\ \tfrac12\,\mathbf e(\mathbf x)^\top\mathbf R^{-1}\mathbf e(\mathbf x),
\qquad \mathbf e(\mathbf x)=\mathbf z-h(\mathbf x).
\tag{23.2}
$$

Two readings of one objective: it is **weighted nonlinear least squares** (weight
by reliability $\mathbf R^{-1}$), and — under Gaussian $\mathbf v$ — it *is* the
**maximum-likelihood estimate**, maximizing $p(\mathbf z\mid\mathbf x)$
[@kay1993]. This matters because the MLE is asymptotically efficient (attains the
Cramér–Rao bound, Ch. 24), giving the estimator a principled optimality, not just
a convenient cost. Using the *correct* $\mathbf R$ — including per-channel and
frequency-dependent weighting (Ch. 19–20) — is what makes the estimate efficient;
an identity weight discards the known noise structure and inflates variance where
some channels are noisier than others.

## 23.3 Gauss–Newton, derived

Linearize the residual about the current estimate $\mathbf x_k$ using the
**Jacobian** $\mathbf J = \partial h/\partial\mathbf x$:
$\mathbf e(\mathbf x_k+\Delta) \approx \mathbf e_k - \mathbf J\Delta$. Substituting
into (23.2) and setting the gradient to zero gives the **normal equations**

$$
(\mathbf J^\top\mathbf R^{-1}\mathbf J)\,\Delta\mathbf x = \mathbf J^\top\mathbf R^{-1}\mathbf e_k,
\qquad \mathbf x_{k+1}=\mathbf x_k+\Delta\mathbf x.
\tag{23.3}
$$

Gauss–Newton drops the second-derivative (residual-curvature) term of the true
Hessian, which is negligible near a good fit (small residuals) — hence GN's
**local quadratic-ish convergence** there [@nocedal2006]. But far from the
solution, or when $\mathbf J^\top\mathbf R^{-1}\mathbf J$ is ill-conditioned
(Ch. 24), the GN step can overshoot or diverge. Two fixes are standard: damping
(LM, §23.4) and solving (23.3) by **QR/SVD of $\mathbf J$** rather than forming
$\mathbf J^\top\mathbf J$ (which squares the condition number, Ch. 24 §24.2).

## 23.4 Levenberg–Marquardt

LM damps the GN step [@marquardt1963]:

$$
(\mathbf J^\top\mathbf R^{-1}\mathbf J + \lambda\,\mathbf D)\,\Delta\mathbf x
= \mathbf J^\top\mathbf R^{-1}\mathbf e_k,
\tag{23.4}
$$

with $\mathbf D$ a positive-definite scaling (Marquardt's choice
$\mathbf D=\operatorname{diag}(\mathbf J^\top\mathbf J)$ makes the step
scale-invariant). The damping interpolates between regimes:

- $\lambda\to 0$: pure Gauss–Newton — fast near the solution.
- $\lambda\to\infty$: $\Delta\mathbf x \to \tfrac1\lambda\mathbf D^{-1}\mathbf J^\top\mathbf R^{-1}\mathbf e_k$,
  a short **steepest-descent** step — robust far away.

LM has a **trust-region** interpretation: each $\lambda$ corresponds to a step
bounded to a region where the linearization is trusted [@nocedal2006]. The
adaptation rule (Marquardt): attempt a step; if the cost decreased, accept and
*decrease* $\lambda$ (e.g. $\div3$); if it increased, reject and *increase*
$\lambda$ (×3) and retry. This robustness to poor initialization and
ill-conditioning makes LM **the workhorse pose solver in EMT** — the practical
realization of the increment-update idea Raab et al. introduced in 1979
[@raab1979; @marquardt1963], and exactly the algorithm in the Phase-6
position-solver tool.

## 23.5 Closed-form initialization from the coupling eigenstructure

LM needs a starting point that lies in the correct basin and avoids the dipole's
mirror solutions. EMT admits an **explicit closed-form initializer** from the
structure of $\mathbf M$ (Ch. 5 §5.4) — here derived in full, resolving the open
question flagged in earlier drafts.

Write the (calibrated) coupling as $\mathbf M = g\,\mathbf R^\top\mathbf K$, where
$g = N_sA_s$ is the sensor gain, $\mathbf R\in SO(3)$ the orientation, and
$\mathbf K = \dfrac{c}{r^3}\big(3\hat{\mathbf r}\hat{\mathbf r}^\top - \mathbf I\big)$
the dipole tensor with $c=\mu_0 m/4\pi$ (Ch. 5 eq. 5.5). Form the
**rotation-invariant** Gram matrix (using $\mathbf R\mathbf R^\top=\mathbf I$ and
$\mathbf K^\top=\mathbf K$):

$$
\mathbf M^\top\mathbf M = g^2\,\mathbf K^2
= g^2\Big(\tfrac{c}{r^3}\Big)^2\big(3\hat{\mathbf r}\hat{\mathbf r}^\top - \mathbf I\big)^2
= g^2\Big(\tfrac{c}{r^3}\Big)^2\big(3\hat{\mathbf r}\hat{\mathbf r}^\top + \mathbf I\big),
$$

since $(3\mathbf P-\mathbf I)^2 = 9\mathbf P -6\mathbf P+\mathbf I = 3\mathbf P+\mathbf I$
for the projector $\mathbf P=\hat{\mathbf r}\hat{\mathbf r}^\top$. Hence
$\mathbf M^\top\mathbf M$ is symmetric with eigenvalues

$$
\lambda_\parallel = 4\,g^2\Big(\tfrac{c}{r^3}\Big)^2\ (\text{eigenvector }\hat{\mathbf r}),
\qquad
\lambda_\perp = g^2\Big(\tfrac{c}{r^3}\Big)^2\ (\times 2).
\tag{23.5}
$$

**The algorithm:**

1. **Eigendecompose** the symmetric $\mathbf M^\top\mathbf M$. The eigenvalues
   should be in ratio $\mathbf{4:1:1}$ — a built-in **self-consistency / quality
   check**; departure flags noise, distortion, or model error (a cheap distortion
   detector, cf. Ch. 21 §21.7).
2. **Bearing:** $\hat{\mathbf r}$ = eigenvector of the largest eigenvalue
   $\lambda_\parallel$ (with a *sign/mirror ambiguity* $\pm\hat{\mathbf r}$,
   resolved by continuity or a workspace prior, §23.7).
3. **Range:** from (23.5), $r = \big(2gc/\sqrt{\lambda_\parallel}\big)^{1/3}$.
4. **Position:** $\mathbf r = r\,\hat{\mathbf r}$.
5. **Orientation:** with $\mathbf K$ now known, $\mathbf R^\top = \tfrac1g\mathbf M\mathbf K^{-1}$
   ($\mathbf K$ is invertible — eigenvalues $\propto\{2,-1,-1\}$); project the
   result to $SO(3)$ via SVD ($\mathbf R = \mathbf U\mathbf V^\top$) to remove
   noise.

This seed is then refined by LM (§23.4). During *continuous tracking*, the
**previous pose** is the initializer (predictor/corrector, Ch. 21), which is
faster and resolves the mirror ambiguity by continuity; the closed form is used at
acquisition and for re-acquisition after track loss. (conf: high — algebra shown
**and numerically verified**: the Phase-5 simulation `sim_closed_form_init`
recovers random poses to machine precision and confirms the exact $1{:}1{:}4$
eigenvalue ratio, `data/closed_form_init.json`. This is the dipole-tensor form of
the classical magnetic-pose closed solution [@raab1979].)

## 23.6 Bayesian / MAP estimation

With prior information — a motion model, a known workspace, or the previous
estimate's covariance — the **maximum a posteriori** estimate adds a prior term
[@kay1993]:

$$
\hat{\mathbf x}_\text{MAP} = \arg\min_{\mathbf x}\ \tfrac12\|\mathbf z-h(\mathbf x)\|^2_{\mathbf R^{-1}} + \tfrac12\|\mathbf x-\mathbf x_0\|^2_{\mathbf P_0^{-1}},
$$

which is **exactly the Kalman update** (Ch. 21) when $\mathbf x_0,\mathbf P_0$ are
the prediction. So the per-frame MAP solver and the recursive estimator are two
views of one Bayesian framework: the solver is a MAP step; the filter chains MAP
steps with a motion model. This tells you *when* to add a prior (fast/continuous
tracking) and *when* to stay maximum-likelihood (independent re-acquisition, where
a stale prior would bias the seed).

## 23.7 $SO(3)$ parameterization & constraints

**Orientation on the manifold.** Rotations must be parameterized to avoid gimbal
lock and keep the update on $SO(3)$: use a **local** increment — a rotation vector
$\delta\boldsymbol\theta$ (exponential map) or quaternion — taken with respect to
the *current* orientation, composed multiplicatively. The Jacobian is taken w.r.t.
$\delta\boldsymbol\theta$, exactly the **error-state** representation the filter
uses (Ch. 21 §21.5), so solver and filter share one rotation convention.

**Constraints** improve conditioning and remove ambiguity [@nocedal2006]:
workspace bounds; $\mathbf R\in SO(3)$ (by manifold parameterization);
known mechanical constraints (a sensor on a rigid shaft → fixed sensor-to-tip
transform, Ch. 14.2); and dual-sensor rigidity (two sensors at known separation →
shared body frame). They are imposed by manifold parameterization,
bound-constrained optimization, or penalty terms, and turn an ill-posed solve into
a well-posed one (Ch. 24).

## 23.8 Robust estimation & outlier rejection

Distortion spikes (Ch. 6), crosstalk (Ch. 19), and dropped channels produce
**gross errors** that a pure least-squares fit over-weights — because the
quadratic loss has an *unbounded influence function*, so a single outlier can
dominate the solution. **M-estimators** replace the quadratic with a robust loss
$\rho(\cdot)$ [@huber1964]:

$$
\hat{\mathbf x} = \arg\min_{\mathbf x}\sum_i \rho\!\big(e_i(\mathbf x)/\sigma_i\big),
$$

- **Huber loss:** quadratic for $|e|\le k$, linear beyond — bounded influence, so
  outliers contribute a constant (not growing) gradient [@huber1964].
- **Tukey biweight:** *redescending* (influence $\to 0$ for large $|e|$) — fully
  rejects gross outliers, at the cost of needing a good initial fit.

In practice these are solved by **iteratively reweighted least squares (IRLS)**:
compute residuals, set weights $w_i = \psi(e_i)/e_i$ (with $\psi=\rho'$), solve the
weighted GN/LM step, repeat. **RANSAC**-style consensus (fit minimal subsets, keep
the largest inlier set) is an alternative when a large fraction of channels may be
corrupt. The innovation-gating of Ch. 21 §21.8 is the recursive analogue. A single
uncorrected outlier can corrupt *all* DOF (the solver couples channels), so
robustness is **not optional** in clinical use.

## 23.9 Convergence, basins & rank-deficiency

- **Basins of attraction.** A nonlinear solver converges only from within a basin;
  the closed-form seed (§23.5) or previous pose (§23.6) must land in the correct
  one, or LM converges to a mirror/local solution. Continuity (tracking) is the
  strongest defense; re-acquisition is the riskiest moment.
- **Rank-deficient Jacobian.** For a 5-DOF sensor the roll direction is
  unobservable, so $\mathbf J$ is rank-deficient (Ch. 24 §24.1); the bare normal
  equations are singular. Handle by **parameterizing out** the unobservable DOF
  (solve only the 5 observable parameters), by **regularization** (the $\lambda$
  in LM acts as a Tikhonov regularizer on the weak direction), or by **fusion**
  (an IMU supplies roll, Ch. 21).
- **Line search / trust region.** LM's $\lambda$ is the trust-region radius;
  alternatively a line search along the GN direction guarantees descent
  [@nocedal2006].

## 23.10 Output

The solver returns $\hat{\mathbf x}$ **and** a local uncertainty
($\approx(\mathbf J^\top\mathbf R^{-1}\mathbf J)^{-1}$, Ch. 24), plus a
quality/convergence flag (including the §23.5 eigenvalue-ratio check). These feed
the state estimator (Ch. 21), the error budget (Ch. 25), and the host/clinical
layer (Ch. 12 §12.4, Ch. 29). A pose without an uncertainty is clinically
incomplete. The Phase-5 Monte-Carlo confirms the LM output's covariance matches
the CRLB to ~3% in the well-conditioned regime (Ch. 24).

---

## Failure modes
- **Mirror/local minimum** (§23.5/23.9): bad seed → wrong basin; use the
  closed-form + continuity, and check the eigenvalue-ratio consistency.
- **Singular normal equations** (5-DOF, §23.9): rank-deficient $\mathbf J$; remove
  the unobservable DOF or regularize.
- **Outlier domination** (§23.8): one corrupted channel skews all DOF under LS;
  use Huber/Tukey IRLS or RANSAC.
- **Ill-conditioning amplification** (Ch. 24): solve via QR/SVD, precondition;
  never form $\mathbf J^\top\mathbf J$ explicitly when $\kappa$ is large.
- **Stale-prior bias** (§23.6): a MAP prior from a lost track biases re-acquisition;
  fall back to pure ML on track loss.

## Open questions / to verify
- ✅ **Resolved:** the closed-form $\mathbf M^\top\mathbf M$ eigenstructure
  initializer is derived (§23.5) **and validated** (`sim_closed_form_init`,
  machine-precision recovery, `data/closed_form_init.json`). Remaining: extend the
  sim to measure seed accuracy / basin capture **vs. measurement noise** and
  mirror-ambiguity rate.
- Benchmark LM vs. trust-region vs. the UKF (Ch. 21) on the dipole model
  (Phase 5), reporting convergence basin and robustness to ambiguity.
- Quantify how often robust losses are needed under realistic distortion (tie to
  Ch. 6 datasets, Ch. 25 Monte Carlo); choose default $k$ for Huber.

## Sources cited
- [@marquardt1963] LM algorithm. [@nocedal2006] GN/trust-region/constraints/line
  search. [@kay1993] MLE/MAP, efficiency. [@huber1964] robust M-estimation.
  [@raab1979] incremental-update precedent and closed-form lineage. Conditioning &
  CRLB in Ch. 24.
