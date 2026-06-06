# Chapter 23 — The Inverse Problem

> **Status:** DRAFT · **Part VIII — Position Solvers**
> Opens Part VIII. Consumes the coupling matrix $\hat{\mathbf M}$ from Ch. 11/20;
> conditioning & uncertainty follow in Ch. 24. Citation keys resolve to
> [`../../citations/bibliography.json`](../../citations/bibliography.json).

The forward model (Ch. 5–7) predicts the coupling matrix $\mathbf M$ from a known
pose. Tracking requires the **inverse**: given a measured $\hat{\mathbf M}$, find
the pose $(\mathbf r,\mathbf R)$ that produced it. Because the dipole coupling is
**nonlinear** in position (the $1/r^3$ and angular factors of Ch. 5) and
orientation lives on the manifold $SO(3)$, this is a nonlinear least-squares /
maximum-likelihood problem. This chapter develops the solvers — closed-form
initialization, Gauss–Newton, **Levenberg–Marquardt**, maximum likelihood, and
Bayesian/MAP — plus constraint handling and robust outlier rejection. Conditioning,
observability, and uncertainty are deferred to Ch. 24.

---

## 23.1 The measurement equation

Stack the calibrated measurements into a vector $\mathbf z = \operatorname{vec}(\hat{\mathbf M})$
and the pose parameters into $\mathbf x$ (3 for position + 2 or 3 for
orientation, depending on 5/6-DOF, Ch. 13). The forward model $h(\mathbf x)$
(Ch. 5 eq. 5.6) gives the predicted measurement, so

$$
\mathbf z = h(\mathbf x) + \mathbf v,\qquad \mathbf v\sim\mathcal N(0,\mathbf R),
\tag{23.1}
$$

with $\mathbf v$ the measurement noise (Parts IV–VII) of covariance $\mathbf R$.
The solver inverts (23.1). Note $h$ is nonlinear and, for the bare dipole, has
**known ambiguities** (sign/mirror solutions; the 5-DOF roll null of Ch. 13) that
the solver must resolve via initialization, constraints, or fusion (Ch. 21).

## 23.2 Least squares and maximum likelihood

The natural estimator minimizes the weighted residual:

$$
\hat{\mathbf x} = \arg\min_{\mathbf x}\ \tfrac12\,\big\|\mathbf z - h(\mathbf x)\big\|^2_{\mathbf R^{-1}}
= \arg\min_{\mathbf x}\ \tfrac12\,\mathbf e(\mathbf x)^\top\mathbf R^{-1}\mathbf e(\mathbf x),
\tag{23.2}
$$

with residual $\mathbf e(\mathbf x)=\mathbf z-h(\mathbf x)$. Two readings of the
same objective:

- **Weighted nonlinear least squares (WNLS).** Minimize squared error weighted by
  measurement reliability ($\mathbf R^{-1}$).
- **Maximum likelihood (MLE).** Under Gaussian $\mathbf v$, (23.2) *is* the
  maximum-likelihood estimate — it maximizes $p(\mathbf z\mid\mathbf x)$
  [@kay1993]. This matters because MLE is asymptotically efficient (attains the
  Cramér–Rao bound, Ch. 24), giving the estimator a principled optimality, not
  just a convenient cost.

Using the *correct* $\mathbf R$ (from the noise budget, Ch. 25) — including any
per-channel and pose-dependent weighting — is what makes the estimate efficient;
an identity weight throws away the known noise structure.

## 23.3 Gauss–Newton and Levenberg–Marquardt

Linearize $h$ about the current estimate via the **Jacobian**
$\mathbf J = \partial h/\partial\mathbf x$ [@nocedal2006]:

- **Gauss–Newton (GN)** step solves the normal equations
  $$
  (\mathbf J^\top\mathbf R^{-1}\mathbf J)\,\Delta\mathbf x = \mathbf J^\top\mathbf R^{-1}\mathbf e,
  $$
  then updates $\mathbf x\leftarrow\mathbf x+\Delta\mathbf x$. Fast (quadratic-ish)
  near the solution, but can diverge far from it or when
  $\mathbf J^\top\mathbf R^{-1}\mathbf J$ is ill-conditioned (Ch. 24).
- **Levenberg–Marquardt (LM)** damps the GN step [@marquardt1963]:
  $$
  (\mathbf J^\top\mathbf R^{-1}\mathbf J + \lambda\,\mathbf D)\,\Delta\mathbf x = \mathbf J^\top\mathbf R^{-1}\mathbf e,
  $$
  interpolating between Gauss–Newton ($\lambda\to0$, fast) and gradient descent
  ($\lambda\to\infty$, robust). $\lambda$ is adapted each iteration (increase on a
  failed step, decrease on success). LM's robustness to poor initialization and
  ill-conditioning makes it **the workhorse pose solver in EMT** — the practical
  realization of the increment-update idea Raab et al. introduced in 1979
  [@raab1979; @marquardt1963].

**Orientation on $SO(3)$.** Rotations must be parameterized carefully — unit
quaternions or a local exponential-map (rotation-vector) increment avoid gimbal
lock and keep the update on the manifold. The Jacobian is taken with respect to
the *local* orientation increment, and the rotation is composed multiplicatively.
(conf: high — standard practice in pose estimation.)

## 23.4 Closed-form initialization

LM needs a starting point, and a good one avoids local minima and the dipole's
mirror ambiguities. EMT admits a **closed-form initializer** from the structure
of $\mathbf M$ (Ch. 5 §5.4): the rotation-invariant product
$\mathbf M^\top\mathbf M$ removes the unknown orientation $\mathbf R$, and the
eigenstructure of the dipole tensor $\mathbf K(\mathbf r)$ (eigenvalues
$\propto\{2,-1,-1\}/r^3$ with the "+2" eigenvector along $\hat{\mathbf r}$) yields
estimates of range $r$ and bearing $\hat{\mathbf r}$; orientation then follows by
aligning measured to predicted columns. This seed is refined by LM. During
continuous tracking, the **previous pose** is the initializer (predictor/corrector,
Ch. 21), which is both faster and resolves ambiguities by continuity. (conf: med —
the eigenstructure initializer is standard in principle; the precise algorithm and
a primary citation are flagged in *Open questions*.)

## 23.5 Bayesian / MAP estimation

When prior information is available — a motion model, a known workspace, or the
previous estimate's covariance — the **maximum a posteriori (MAP)** estimate adds
a prior term [@kay1993]:

$$
\hat{\mathbf x}_{\text{MAP}} = \arg\min_{\mathbf x}\ \tfrac12\|\mathbf z-h(\mathbf x)\|^2_{\mathbf R^{-1}} + \tfrac12\|\mathbf x-\mathbf x_0\|^2_{\mathbf P_0^{-1}},
$$

which is exactly the **measurement update of the Kalman filter** (Ch. 21) when
$\mathbf x_0,\mathbf P_0$ are the prediction. So the per-frame MAP solver and the
recursive estimator are two views of one Bayesian framework: the solver is a MAP
step; the filter chains MAP steps with a motion model. This unification is worth
internalizing — it tells you when to add a prior (fast/continuous tracking) and
when to stay maximum-likelihood (independent re-acquisition).

## 23.6 Constraints and outlier rejection

Real solves must respect physics and survive bad data:

- **Constraints.** Workspace bounds, $\|\hat{\mathbf n}_s\|=1$, $\mathbf R\in SO(3)$,
  and known mechanical constraints (e.g. a sensor on a rigid shaft) can be imposed
  by manifold parameterization (rotations), bound-constrained optimization, or
  penalty terms [@nocedal2006]. Constraints both improve conditioning (Ch. 24) and
  remove ambiguous solutions.
- **Outlier rejection / robust estimation.** Distortion spikes (Ch. 6),
  crosstalk (Ch. 19), and dropped channels produce gross errors that a pure
  least-squares fit (quadratic loss) over-weights. **Robust losses** (Huber,
  Tukey) or **RANSAC**-style consensus down-weight or discard outliers; the
  innovation-gating of Ch. 21 §21.6 is the recursive analogue. A single
  uncorrected outlier can corrupt all DOF because the solver couples channels —
  so robustness is not optional in clinical use.

## 23.7 Output
The solver returns $\hat{\mathbf x}$ **and** a local uncertainty (from
$(\mathbf J^\top\mathbf R^{-1}\mathbf J)^{-1}$, Ch. 24), plus a quality/convergence
flag. These feed the state estimator (Ch. 21), the error budget (Ch. 25), and the
host/clinical layer (Ch. 12 §12.4, Ch. 29). A pose without an uncertainty is
clinically incomplete.

---

## Open questions / to verify
- Attach a primary citation for the closed-form $\mathbf M^\top\mathbf M$
  eigenstructure initializer and write the explicit algorithm in Appendix C.
- Benchmark LM vs. trust-region and vs. the UKF (Ch. 21) on the dipole model
  (Phase 5), reporting convergence basin and robustness to ambiguity.
- Quantify how often robust losses are needed under realistic distortion (ties
  Ch. 6 datasets, Ch. 25 Monte Carlo).

## Sources cited
- [@marquardt1963] LM algorithm. [@nocedal2006] GN/trust-region/constraints.
  [@kay1993] MLE/MAP. [@raab1979] incremental-update precedent. Conditioning &
  CRLB in Ch. 24.
