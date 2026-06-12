# Chapter 24 — Conditioning, Observability & Uncertainty

> **Status:** DEEPENED (awaiting review) · **Part VIII — Position Solvers**
> Closes Part VIII. Builds on Ch. 23 (solver) and feeds the error budget (Ch. 25)
> and fusion (Ch. 21). Backed by the Phase-5 CRLB/Monte-Carlo simulations.
> Citation keys resolve to [`../../citations/bibliography.json`](../../citations/bibliography.json).

A pose solver can converge to the right answer in one part of the working volume
and be hopelessly uncertain in another — using the *same* hardware and the *same*
algorithm. The difference is **geometry**: how informative the measurement is
about each pose parameter. This chapter develops the tools that quantify and
predict that — **observability/identifiability** (can the pose be determined at
all?), **conditioning** (how sensitively does pose error amplify measurement
error?), **dilution of precision** (the navigation field's name for the same
thing), **convergence**, and **uncertainty quantification** (the covariance and
the Cramér–Rao bound). EMT here is a sibling of GNSS: both invert a nonlinear
range/geometry model, and both live or die by the conditioning of a measurement
Jacobian [@groves2013]. Together these explain *why* accuracy varies across the
volume and turn a point estimate into a trustworthy measurement.

---

## 24.1 Observability and identifiability

These two are distinct and both matter:

- **Local observability** — does the measurement change *infinitesimally* when a
  parameter changes? Formally, parameter direction $\mathbf d$ is locally
  observable at $\mathbf x$ iff $\mathbf J\mathbf d\neq 0$, i.e. $\mathbf d$ is not
  in the null space of the Jacobian $\mathbf J=\partial h/\partial\mathbf x$
  (Ch. 23). Equivalently, the **Fisher information**
  $\mathbf F=\mathbf J^\top\mathbf R^{-1}\mathbf J$ (§24.5) must be full rank.
- **Global identifiability** — do *distinct* poses ever produce *identical*
  measurements? Even with full-rank $\mathbf J$ everywhere, the map $h$ can be
  many-to-one.

EMT's failures of each are concrete:

- **The 5-DOF roll null (local).** For a single-element sensor, rotation about its
  own axis leaves every measurement unchanged: $\mathbf J$ is **exactly
  rank-deficient** in that direction (a structural zero singular value). No solver
  recovers it; only a second element or fusion does (Ch. 13, Ch. 21).
- **Dipole sign/mirror ambiguities (global).** The forward model maps
  $\hat{\mathbf r}\to-\hat{\mathbf r}$ (and related $\mathbf m\to-\mathbf m$
  symmetries) to indistinguishable measurements — the very mirror solutions the
  closed-form initializer inherits (Ch. 23 §23.5). These are **un-identifiable**
  without a prior or continuity, no matter how good the conditioning.
- **Weak-gradient regions (near-singular).** Where the field is locally
  near-uniform (Ch. 5 §5.7), position barely moves the measurement — technically
  observable but practically near-null.

**A useful link to the closed form.** The $\mathbf M^\top\mathbf M$ eigenstructure
of Ch. 23 §23.5 (eigenvalues $4{:}1{:}1$) is an observability statement: the
**bearing direction $\hat{\mathbf r}$ (the "4" eigenvector) is the best-observed**
combination, the two transverse directions less so. The diagnostic everywhere is
the **singular-value spectrum of $\mathbf J$** (or eigenvalues of $\mathbf F$): a
zero = unobservable, a small one = weakly observable. Mapping the smallest
singular value across the volume yields an **observability map** that should drive
generator/sensor placement (Ch. 9) and the working-volume spec.

## 24.2 Conditioning and numerical stability

Even when fully observable, the inverse can be **ill-conditioned**. Take the SVD
$\mathbf J=\mathbf U\boldsymbol\Sigma\mathbf V^\top$ with singular values
$\sigma_1\ge\dots\ge\sigma_n$. A measurement perturbation $\delta\mathbf z$
maps to a pose perturbation whose worst-case size is

$$
\|\delta\mathbf x\| \le \frac{\|\delta\mathbf z\|}{\sigma_{\min}},
\qquad
\frac{\|\delta\mathbf x\|/\|\mathbf x\|}{\|\delta\mathbf z\|/\|\mathbf z\|}\le \kappa(\mathbf J)=\frac{\sigma_{\max}}{\sigma_{\min}}.
\tag{24.2}
$$

So error along the **weakest-observed direction** ($\mathbf v_n$, the right
singular vector of $\sigma_{\min}$) is amplified by $1/\sigma_{\min}$, and the
*relative* amplification is bounded by the condition number $\kappa$
[@nocedal2006]. EMT consequences:

- **The $1/r^3$ law hurts conditioning at range.** As the field weakens and
  flattens, $\sigma_{\min}(\mathbf J)$ shrinks toward the volume edge, so $\kappa$
  grows and the same amplitude noise yields far larger pose error — the
  quantitative form of "accuracy degrades with distance" (made exact as the $z^4$
  law in §24.5). The Phase-6 *error-propagation* tool plots $\kappa(\mathbf J)$ vs.
  range directly.
- **Mixed units / preconditioning.** Position (metres) and orientation (radians)
  share one state vector; their raw columns of $\mathbf J$ differ by many orders
  of magnitude, inflating $\kappa$ *artificially*. **Non-dimensionalize** —
  scale the position columns by a characteristic length (e.g. the working-volume
  radius) and keep orientation in radians, or apply column scaling
  $\mathbf J\to\mathbf J\mathbf S$ — before assessing conditioning or solving. This
  separates *geometric* ill-conditioning (real) from *unit* ill-conditioning
  (spurious).
- **Never form $\mathbf J^\top\mathbf J$.** The normal-equations matrix has
  $\kappa(\mathbf J^\top\mathbf J)=\kappa(\mathbf J)^2$ — forming it *squares* the
  conditioning and halves the available precision. Solve the linearized step via a
  **QR or SVD of $\mathbf J$** (backward-stable) [@nocedal2006]; LM's damping
  $\lambda\mathbf D$ additionally **regularizes** near-singular steps (Ch. 23
  §23.4), bounding the amplification at the cost of a small bias.

This is exactly the "1% amplitude error ≠ 1% pose error" amplification flagged in
Ch. 11 §11.5: the amplification factor *is* (loosely) $\kappa$, and it is
pose-dependent.

## 24.3 Dilution of precision — the navigation bridge

Navigation engineers have a name for pose-independent geometric conditioning:
**dilution of precision (DOP)** [@groves2013]. For unit, isotropic measurement
noise ($\mathbf R=\sigma^2\mathbf I$), the estimate covariance is
$\operatorname{Cov}=\sigma^2(\mathbf J^\top\mathbf J)^{-1}$, and one defines

$$
\text{PDOP} = \sqrt{\operatorname{tr}\big[(\mathbf J^\top\mathbf J)^{-1}\big]_\text{pos}},
\qquad
\sigma_\text{pos} = \sigma\cdot\text{PDOP},
\tag{24.3}
$$

(position DOP; analogous GDOP/HDOP/VDOP for the full/horizontal/vertical blocks).
DOP cleanly separates the **geometry** (PDOP, a pure number) from the
**measurement noise** ($\sigma$): a system has good *geometry* where PDOP is small,
independent of how noisy the sensors are. For EMT this is illuminating:

- The **CRLB map is a DOP map** scaled by $\sigma_B$ — the $z^4$ growth of §24.5
  *is* the PDOP of a single triad/array growing toward the volume edge.
- Adding transmitter coils (Ch. 9, Ch. 19 §19.7) or a second sensor element
  **lowers PDOP** the same way adding satellites lowers GNSS DOP — better geometry,
  before any noise improvement.
- It gives a design vocabulary shared with the fusion side (Ch. 21): EM+IMU+optical
  is "multisensor integrated navigation" [@groves2013], and its conditioning is the
  combined Fisher information of all modalities.

(conf: high — DOP is the standard navigation framing; the EMT-PDOP identification
is exact given (24.3).)

## 24.4 Convergence and initialization

A nonlinear solver converges only from within a **basin of attraction**:

- **Initialization** (Ch. 23 §23.5): the closed-form seed or previous pose must lie
  in the correct basin, or LM converges to a mirror/local solution. Continuity
  (tracking) is the strongest defense; re-acquisition is the riskiest moment.
- **Damping/trust region** (LM) enlarges the reliable step region versus raw
  Gauss–Newton, trading speed for robustness [@marquardt1963; @nocedal2006].
- **Bounded iterations** (Ch. 22 §22.5): in real time, cap iterations and, on
  non-convergence (often a symptom of poor conditioning or distortion), emit the
  predicted pose with inflated covariance and a quality flag rather than a wrong,
  confident answer.

Convergence behaviour is itself **pose-dependent**: ill-conditioned regions have
flatter, more elongated cost valleys (the small-$\sigma$ direction of §24.2) that
slow convergence and widen the ambiguity risk — so §§24.1–24.4 are one coupled
story, visualized directly in the Phase-6 *position-solver* tool (the cost surface
is elongated where conditioning is poor).

## 24.5 Uncertainty quantification: covariance and the CRLB

The estimate is incomplete without its uncertainty. Two linked tools [@kay1993]:

- **Fisher information & the Cramér–Rao lower bound (CRLB).** For the Gaussian
  model (23.1) the Fisher information is
  $\mathbf F = \mathbf J^\top\mathbf R^{-1}\mathbf J$, and **no unbiased estimator
  can do better than**
  $$
  \operatorname{Cov}(\hat{\mathbf x}) \succeq \mathbf F^{-1} = (\mathbf J^\top\mathbf R^{-1}\mathbf J)^{-1}.
  \tag{24.1}
  $$
  The CRLB is the **theoretical accuracy limit** for a given geometry and noise — a
  design tool: evaluate it across the volume to predict achievable accuracy
  *before building anything*, and to compare generator/sensor designs (Ch. 9, 13)
  on equal footing. Its diagonal gives per-DOF variance; its **eigenvectors give
  the error ellipsoid's axes** (the principal directions and magnitudes of pose
  uncertainty). The position and orientation blocks (and their cross-covariance)
  separate the two error types — orientation can be well-determined where position
  is not, and vice versa.
- **Estimator covariance.** The MLE asymptotically attains the CRLB [@kay1993], so
  the solver's output covariance $\approx\mathbf F^{-1}$ at the solution is both the
  reported uncertainty *and* (near) the best possible — the covariance handed to
  the Kalman filter as innovation weighting (Ch. 21) and to the error budget
  (Ch. 25).

**Computed CRLB (Phase-5 simulation).** Evaluating (24.1) for a co-located
transmitter triad and a sensor triad ($m_t=1$, field-referred measurement noise
$\sigma_B=1\,\text{nT}$, `simulations/run_all.py`) gives on-axis position bounds
of **0.017 / 0.086 / 0.66 mm at 0.2 / 0.3 / 0.5 m** — sub-millimetre across a
0.5 m volume, consistent with the Ch. 31 target. Critically, the on-axis CRLB grows
as $\sigma_{\text{pos}}\propto z^{4.0}$ (fitted exponent $4.00$;
`data/crlb_vs_range.csv`, `figures/ch24_crlb_vs_range.png`): the $1/r^3$ field
weakening contributes three powers of range and the flattening position-sensitivity
a fourth, so **accuracy degrades as the fourth power of range** — the sharpest
quantitative statement of the conditioning penalty of §24.2, and (per §24.3) the
PDOP of the geometry. The CRLB map (`figures/ch24_crlb_map.png`) shows the
best-conditioned region near the generator and rapid edge degradation. (conf:
high — computed; absolute values scale with the assumed $\sigma_B$.)

**Consistency caveat.** The linearized covariance (24.1) is a *local* (Gaussian)
approximation; near ambiguities, weak observability, or strong nonlinearity it
**understates** true uncertainty (the posterior is non-Gaussian/multimodal — hence
particle filters, Ch. 21 §21.6). A covariance claiming high confidence in a poorly
observable region is dangerous; consistency checks (NIS/NEES, Ch. 21 §21.8) and the
observability map (§24.1) guard against believing it. The Phase-5 Monte-Carlo
(`data/monte_carlo_vs_crlb.json`) confirms the LM solver's empirical error
**matches the CRLB to within ~3%** at near/mid/far poses — the estimator is
efficient and the bound is a usable predictor in the well-conditioned regime. The
Phase-6 *Monte-Carlo uncertainty* tool overlays the live scatter on this CRLB
ellipse.

## 24.6 The full 6-DOF Fisher information and the position–orientation coupling

The CRLB of §24.5 is often *presented* as if position-only, but EMT estimates a
**6-DOF pose** $\mathbf x=(\mathbf p,\boldsymbol\varphi)$ — position plus a 3-vector
orientation (a rotation vector). A 3-axis sensor reading three transmit axes yields a
**9-vector** of coupling-matrix entries, so the Jacobian $\mathbf J=\partial h/\partial
\mathbf x$ is $9\times6$ and the Fisher information is a **$6\times6$** matrix, blocked
into position, orientation, and their **coupling**:
$$
\mathbf F=\begin{bmatrix}\mathbf F_{pp}&\mathbf F_{p\varphi}\\ \mathbf F_{\varphi p}&\mathbf F_{\varphi\varphi}\end{bmatrix}.
$$
The **honest position CRLB** is the position block of the *full* inverse, which by the
Schur complement is
$$
\operatorname{Cov}_{pp}=[\mathbf F^{-1}]_{pp}=\big(\mathbf F_{pp}-\mathbf F_{p\varphi}\mathbf F_{\varphi\varphi}^{-1}\mathbf F_{\varphi p}\big)^{-1}\ \succeq\ \mathbf F_{pp}^{-1}.
\tag{24.4}
$$
The subtracted term is the **information lost to estimating an unknown orientation**:
the naive bound $\mathbf F_{pp}^{-1}$ (which pretends orientation is known) is
*optimistic*; the true 6-DOF bound (24.4) is larger.

**Computed — the coupling penalty is a constant (Phase-5, `data/crlb_6dof.json`).**
Evaluating (24.4) for the co-located triad/triad geometry, treating orientation as
**unknown inflates the position CRLB by a pose-invariant factor $\approx2.95$**
(variance $\approx8.7\times$) — identical at near, mid, and far on-axis poses *and* at
off-axis tilted poses, to four significant figures. The invariance is structural: the
dipole tensor $(3\hat{\mathbf r}\hat{\mathbf r}^\top-\mathbf I)$ and the rotation-vector
parameterization give position- and orientation-Jacobian blocks whose relative
geometry is **scale- and rotation-invariant**, so the Schur-complement ratio is a fixed
property of the configuration, not of where you are in the volume. The practical upshot:
the position bounds reported in §24.5 (0.017 / 0.086 / 0.66 mm) **are already the
marginalized 6-DOF values** — the book quoted the honest number — and an
orientation-known analysis would be **~3× too optimistic**. *You cannot state a
position accuracy without saying whether orientation is known or jointly estimated;* a
real 6-DOF tracker estimates both, so the ~3× penalty is real and belongs in the budget
(Ch. 25). (conf: high — computed, robust across diverse poses.)

**The orientation CRLB scales more gently — as $z^3$.** The same inversion gives the
orientation bound (the $\boldsymbol\varphi$ block of $\mathbf F^{-1}$):
**0.0097° / 0.033° / 0.15° at 0.2 / 0.3 / 0.5 m**, fitting
$\sigma_\varphi\propto z^{3.0}$ — **one power of range less than position's $z^4$**. The
reason is physical: **orientation is read from the field's direction/magnitude at the
sensor** ($\propto1/r^3$, so noise/signal $\propto r^3$), whereas **position is read
from the field's *gradient*** — one more spatial derivative, hence one more power of
range. Orientation therefore degrades more gracefully with distance than position, and
the off-diagonal $\mathbf F_{p\varphi}$ means a position error and an orientation error
are **correlated** — the true uncertainty is a single ellipsoid in the full 6-D pose
space, not separable per-DOF.

## 24.7 Nonlinear observability and the hemisphere ambiguity

The local observability test of §24.1 (rank of $\mathbf J$) is a **linearization**, and
for a *nonlinear* measurement a full-rank Jacobian everywhere does **not** guarantee a
unique global solution. The rigorous tool is the **nonlinear observability rank
condition** of Hermann & Krener [@hermann1977]: form the observability codistribution
from the differentials of the output and its **Lie derivatives** along the system's
dynamics; the pose is **locally weakly observable** where those differentials span the
full state space. For a *static* single measurement (no dynamics) this collapses back to
"full-rank $\mathbf J$" (§24.1) — but the nonlinear machinery earns its keep **with
motion**: along a trajectory the time-derivatives of the measurement add independent
rows (the observability Gramian of the moving sensor), so a pose that is *instantaneously*
weakly observable can become observable over a **short arc**. This is the formal basis
for why **motion and fusion** (Ch. 21) recover the 5-DOF roll null and stabilize weak
directions that a single static frame cannot.

**The hemisphere (parity) ambiguity — the decisive global case.** The dipole coupling
to a sensor at $\mathbf r$ enters through $\hat{\mathbf r}\hat{\mathbf r}^\top$, which is
**invariant under $\hat{\mathbf r}\to-\hat{\mathbf r}$**. So a sensor at $+\mathbf r$ and
its mirror image at $-\mathbf r$ through the generator origin produce coupling tensors
related by a sign flip that a matching **sensor-orientation flip makes identical**:
two distinct 6-DOF poses, **the same 9-vector measurement**. A single-generator dipole
system therefore **cannot tell which side of the generator the sensor is on** — a
*global* un-identifiability (the Jacobian can be full-rank at *both* poses, so no amount
of conditioning, §24.2, resolves it). This is the rigorous form of the "sign/mirror
ambiguity" flagged in §24.1 and the mirror basins the closed-form initializer inherits
(Ch. 23 §23.5). Every fielded system breaks the symmetry, and the ways it does are worth
naming:
- **Asymmetric generator geometry** — a *planar, multi-coil* generator (Ch. 9; T2.1)
  whose coils are not co-located has spatial extent that distinguishes the two
  hemispheres; the symmetry is broken by construction.
- **A half-space prior** — the sensor is physically on one known side (the patient
  *above* an under-table generator); constrain the solver to that half-space.
- **Continuity / tracking** — start in the known hemisphere and track; continuity keeps
  the estimate in the correct basin, and **re-acquisition is the dangerous moment**
  (§24.4).
- **Fusion** — an independent modality (IMU/optical, Ch. 21) disambiguates directly.

The lesson is that EMT observability has **two layers**: local (linear, the $\mathbf J$/
Fisher rank of §§24.1–24.6, which motion and a second element fix) and **global** (the
parity symmetry of the dipole, which only an asymmetric generator, a prior, continuity,
or fusion fixes). A system can be perfectly conditioned and still globally ambiguous —
which is why "well-conditioned" (§24.2) and "uniquely solvable" are *different*
guarantees. (conf: high — the parity symmetry is exact for the ideal dipole; Hermann–
Krener is the standard nonlinear-observability framework.)

## 24.8 Synthesis: why accuracy varies across the volume
Sections 24.1–24.5 are one causal chain:

$$
\underbrace{\text{geometry} \to \mathbf J}_{\S24.1}\ \to\ \underbrace{\sigma_{\min}(\mathbf J),\ \kappa,\ \text{PDOP}}_{\S24.2\text{–}24.3}\ \to\ \underbrace{(\mathbf J^\top\mathbf R^{-1}\mathbf J)^{-1}}_{\S24.5\ \text{CRLB}}\ =\ \text{pose uncertainty}.
$$

Combined with the noise→pose relation of Ch. 15 §15.4, this is the complete recipe
for predicting EMT accuracy at any pose: **measurement noise (Parts IV–VII) ×
integration (Ch. 11/20) ÷ signal ($m_t/r^3$, Ch. 9) × geometric conditioning /
PDOP (this chapter) = uncertainty.** It tells the designer where the system is
good, where it is marginal, and how to fix it (more moment, more coils for lower
PDOP, better-conditioned geometry, longer integration, fusion). Part IX assembles
these into a full error budget.

---

## Open questions / to verify
- ✅ **Resolved (Phase 5):** CRLB maps + range curve produced and validated against
  Monte-Carlo (`data/monte_carlo_vs_crlb.json`, ~3%); on-axis
  $\sigma_{\text{pos}}\propto z^{4}$; wrapped as the Phase-6 CRLB / Monte-Carlo /
  error-propagation tools.
- ✅ **Resolved (Phase 5, §24.6):** full **6-DOF** Fisher information computed
  (`data/crlb_6dof.json`): the position-only-vs-marginalized **coupling penalty is a
  pose-invariant $\approx2.95\times$** (variance $\approx8.7\times$), the reported
  position CRLB is the honest marginalized value, and the **orientation CRLB
  $\propto z^3$** (0.0097–0.15° over the volume). Remaining: render the 6-DOF error
  ellipsoid and the orientation-CRLB map in the Phase-6 tools; explain the exact
  numeric value 2.95 analytically from the dipole tensor.
- ✅ **Resolved (§24.7):** the dipole **hemisphere/parity ambiguity** stated rigorously
  (global un-identifiability under $\hat{\mathbf r}\to-\hat{\mathbf r}$) with the
  Hermann–Krener local/global distinction. Remaining: a worked observability-Gramian
  example showing motion resolving a weakly-observable pose over a short arc.
- Compute and plot a **PDOP map** explicitly (a pure-geometry quantity) and the
  PDOP reduction from adding transmitter coils / a 2nd sensor element (ties §24.3,
  Ch. 9/13/19) — a small Phase-5 addition.
- Quantify the conditioning improvement of a second (askew) sensor element vs.
  EM+IMU fusion for the 5→6-DOF case (ties Ch. 13, 21).
- Add a worked preconditioning/SVD example showing the $\kappa$ reduction from
  non-dimensionalization.

## Sources cited
- [@kay1993] Fisher information, CRLB, MLE efficiency. [@nocedal2006] conditioning,
  SVD/QR, trust region. [@groves2013] dilution of precision / multisensor
  navigation. [@marquardt1963] LM regularization. [@hermann1977] nonlinear
  observability rank condition / Lie derivatives (§24.7). Full 6-DOF FIM and the
  coupling penalty computed in `simulations/run_all.py` (§24.6, `data/crlb_6dof.json`).
  Observability links to Ch. 13; error budget to Ch. 25.
