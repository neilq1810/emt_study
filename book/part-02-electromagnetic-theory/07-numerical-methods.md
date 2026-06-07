# Chapter 7 — Analytical & Numerical Field Methods

> **Status:** DEEPENED (awaiting review) · **Part II — Electromagnetic Theory**
> Closes Part II. Builds on Ch. 4–6. Citation keys resolve to
> [`../../citations/bibliography.json`](../../citations/bibliography.json).

Chapters 4–6 gave closed-form field models (point dipole, finite loop) and the
physics of distortion. Real field generators have ferromagnetic cores, finite
windings, and live in environments full of conductors — none of which the
dipole formula captures exactly. This chapter surveys the modeling toolbox that
takes us from idealized formulas to a **forward model accurate enough to invert
for sub-millimeter pose**: when the analytic models suffice, when to reach for
finite-element (FEA) or boundary-element (BEM) methods, and how models are
verified against measurement. The governing engineering truth is that **EMT
accuracy is limited by how well you know the field** — a tracker can be no more
accurate than its forward model [@franz2014].

---

## 7.1 The hierarchy of forward models

EMT forward models form a hierarchy of increasing fidelity and cost:

| Tier | Model | Valid when | Cost |
|---|---|---|---|
| 0 | Point dipole (eq. 4.1 / 5.3) | $r\gtrsim 5$–$10\,a$, air, no core | trivial (closed form) |
| 1 | Finite-loop elliptic integrals (eq. 4.3+) | air, no core, any $r>0$ | cheap (special functions) |
| 2 | Multipole expansion of the real coil | air, beyond source region | moderate (precomputed moments) |
| 3 | FEA / BEM with cores & geometry | cored generators, near field | expensive (offline) |
| 4 | Measured field map / calibration LUT | any, captures *this* unit + room | one-time measurement |

A well-engineered system typically uses **Tier 3/4 offline** to build an
accurate static model of the generator, then a **cheap Tier 0–2 evaluation
online** (often a fitted analytic or interpolated form) so the real-time solver
of Part VIII can evaluate the forward model thousands of times per second
(Ch. 12 latency). The art is choosing the *online* representation that is both
fast and faithful.

## 7.2 When the analytic models suffice (and when they lie)

From Ch. 4 §4.6, the dipole error scales as $(a/r)^2$. The practical
implications:

- **Air-cored, small generator coils, sensor well outside the coil:** Tier 0–1
  is often adequate after a scalar gain calibration per axis.
- **Ferromagnetic-cored generators** (used to boost moment $m$ for SNR, Ch. 9):
  the core's high $\mu_r$ reshapes the field and adds a temperature- and
  drive-dependent component the vacuum dipole formula *cannot* represent. The
  field equations must be augmented to account for perturbations due to
  ferromagnetic cores — exactly the regime where calibration measurements
  diverge from the theoretical dipole (conf: med — this divergence and the need
  to model cored radiators is reported in the field-generator calibration
  literature; see *Open questions* for the specific primary source to attach).
- **Anywhere near a conductor or steel:** no air model is valid; either keep
  such material out of the volume or move to Tier 4 mapping (Ch. 26).

**A fast intermediate — the reluctance (magnetic-circuit) model.** Before
committing to full FEA, a cored radiator can often be captured by a lumped
**magnetic-circuit** model: treat the core, air gaps, and return path as
reluctances $\mathcal R = \ell/(\mu A)$ in series/parallel, driven by the
magnetomotive force $NI$. This yields the working-point flux and the effective
moment (including the demagnetizing/saturation behaviour of Ch. 5 §5.1) in closed
form — cheap enough for design sweeps, accurate enough to size a core before a
single mesh is built. It is the magnetics analogue of a first-pass circuit
estimate; FEA then refines it.

### The spherical-harmonic field model (the fast *online* representation)
The central practical problem of §7.1 — get a model that is both **faithful**
(Tier 3/4) and **fast** (Tier 0–2) — has a clean, rigorous solution. In a
**current-free** region (the working volume, sources outside it), the field is
both curl- and divergence-free, so it derives from a **magnetic scalar
potential** $\mathbf B = -\mu_0\nabla\psi$ with $\nabla^2\psi=0$. The
regular-at-origin solution is a sum of **solid spherical harmonics**:

$$
\psi(\mathbf r) = \sum_{l=0}^{L}\sum_{m=-l}^{l} a_{lm}\, r^{l}\, Y_{lm}(\theta,\phi),
\qquad
\mathbf B = -\mu_0\nabla\psi .
\tag{7.1}
$$

Fit the coefficients $a_{lm}$ (by least squares) to field samples from FEA or
measurement over the volume; a modest truncation $L\sim3$–$5$ captures a smooth
generator field to well below the noise floor. The payoff is large: (7.1) is
**analytic, exactly source-free** ($\nabla\!\cdot\!\mathbf B=\nabla\!\times\!\mathbf B=0$
by construction — unlike a naïve interpolation), **differentiable in closed form**
(so the solver Jacobian of Ch. 24 comes for free and exactly), and evaluates in
microseconds. This is the standard way to compress an expensive offline field into
a real-time forward model, and it generalizes the multipole "Tier 2" row of §7.1
to the *full* cored/planar generator (not just a dipole). (conf: high — solid
harmonics are the standard Laplace-equation basis [@jackson1998]; the
fit-and-evaluate workflow is widely used for cored/planar field generators.)

## 7.3 Finite element analysis (FEA)

FEA solves the magnetostatic (or low-frequency eddy-current) boundary-value
problem on a discretized mesh [@jin2014]. For EMT the relevant formulations are:

- **Magnetostatic, $\mathbf A$-formulation.** With $\mathbf B=\nabla\times\mathbf A$
  (which enforces $\nabla\!\cdot\!\mathbf B=0$ identically) and reluctivity
  $\nu=1/\mu$, Ampère's law becomes
  $$
  \nabla\times(\nu\,\nabla\times\mathbf A) = \mathbf J ,
  $$
  solved in weak (Galerkin) form. The gauge freedom in $\mathbf A$ is fixed by a
  Coulomb gauge or, in practice, a tree–cotree gauging of the discrete system.
- **Low-frequency eddy-current ($\mathbf A$–$V$) formulation** for the Ch. 6
  distortion physics: in conductors
  $\nabla\times(\nu\nabla\times\mathbf A) + \sigma(\partial_t\mathbf A + \nabla V)=0$,
  solved as a complex phasor at the excitation frequency — capturing the
  skin-depth response of eq. (6.1).

**Edge (vector) elements are essential.** Representing a vector field like
$\mathbf A$ with ordinary nodal (scalar-per-component) elements produces *spurious
modes* and mis-handles the tangential-continuous / normal-discontinuous behaviour
at material interfaces. **Nédélec edge elements** assign degrees of freedom to
mesh *edges* and enforce exactly the right continuity, and are the standard choice
for magnetostatic/eddy-current EMT modeling [@jin2014].

Practical FEA requirements specific to EMT:

1. **Open-boundary treatment.** The near field decays slowly ($1/r^3$), so a
   simple truncated box with a Dirichlet wall placed too close creates artificial
   image effects. Remedies (in increasing fidelity): extend the box several
   working-volume radii and apply $\mathbf A\times\hat{\mathbf n}=0$; **infinite
   elements** or a **Kelvin/ballooning transformation** that maps the exterior to
   a finite region; or a **hybrid FEM–BEM** that imposes the exact exterior
   solution on the truncation surface [@jin2014].
2. **Mesh resolution.** Refine where the gradient is steep — near windings and
   core edges (pose accuracy depends on the field *gradient*, Ch. 5 §5.7) — and,
   for eddy-current runs, **resolve the skin depth** with at least ~2 elements per
   $\delta$ (eq. 6.1), or the conductor's surface current is mis-computed.
3. **Material curves & convergence.** Model core $\mu_r(H)$ nonlinearity/saturation
   if the generator is driven hard for moment (Ch. 9); and demonstrate **mesh
   convergence** — refine until the field (and its gradient) over the working
   volume stops changing within tolerance, guided by an a-posteriori error
   estimator.

General-purpose solvers (e.g. ANSYS-class magnetostatic/eddy-current modules)
are the standard tooling [@jin2014]; the offline FEA field is then compressed into
the fast spherical-harmonic online model of §7.2.

## 7.4 Boundary element / method of moments (BEM/MoM)

Where FEA meshes the whole *volume*, BEM/MoM discretizes only *surfaces* (coil
conductors, conductor boundaries) and uses free-space Green's functions — a
natural fit for EMT because (a) the medium is mostly homogeneous air, and (b)
the $1/|\mathbf{r}-\mathbf{r}'|$ kernel of the Neumann/Biot–Savart integrals
(Ch. 5, eq. 5.4) *is* the Green's function. Mutual inductances between source
surfaces can be computed by integral methods, and distortion from compact
conductors handled as induced surface-current problems. BEM avoids the
open-boundary truncation problem of FEA (the radiation condition is built into
the Green's function) at the cost of dense system matrices. Many production
field-map and distortion-correction pipelines blend integral (BEM-like) methods
with measured calibration (conf: med — integral-methodology field mapping is
documented in the patent/engineering literature surfaced in research; primary
academic citation to attach).

## 7.5 Verification & validation (V&V)

A forward model used for medical pose estimation must be *validated*, not merely
*computed*. The V&V chain:

1. **Verification (math).** Confirm the numerical solver reproduces known
   analytic cases: on-axis loop (eq. 4.3), the 2:1 on-axis/equator ratio
   (Ch. 4 §4.4 / Ch. 5 worked example), the dipole far-field limit, and — where no
   closed form exists — a **method of manufactured solutions** (insert a known
   $\mathbf A$, derive the source it implies, and check the solver recovers it).
   These are the cheap sanity checks every implementation must pass. The Phase-5
   suite already encodes the analytic benchmarks: `sim_coupling_checks` confirms
   the $\{2,-1,-1\}$ tensor eigenstructure and the 2:1 ratio exactly, and
   `sim_dipole_vs_loop` validates the finite-loop↔dipole limit (Ch. 4 §4.6) — the
   same checks any FEA build must reproduce.
2. **Validation (physical).** Compare the model against **measured** field maps
   or against **pose ground truth** from an independent, higher-accuracy
   modality (optical tracker, coordinate-measuring machine, precision phantom).
   The standardized phantom/protocol of Hummel et al. [@hummel2005] is the
   reference methodology for the *system-level* validation that closes this
   loop, and the calibration-technique survey of Kindratenko [@kindratenko2000]
   catalogs how measured maps are turned into correction models.
3. **Uncertainty propagation.** A model is incomplete without its error bars;
   model residuals feed directly into the error budget of Part IX (Ch. 25) and
   the solver covariance of Ch. 24.

> **Engineering takeaway.** The dipole formula is where you *start*, not where
> you *ship*. Production EMT couples an offline high-fidelity model (FEA/BEM
> and/or measured map) to a fast online evaluator, and proves the whole thing
> against an independent ground truth. Chapters 26–27 turn this into concrete
> calibration procedures.

---

## Open questions / to verify
- ✅ **Resolved:** FEA formulation/edge-elements/open-boundary now grounded in
  Jin [@jin2014]; the fast online model (spherical harmonics) and the
  reluctance intermediate are added (§7.2). Remaining: attach an *EMT-specific*
  cored-radiator FEM-calibration paper as a worked case study.
- Add a worked spherical-harmonic fit (Phase-5): fit (7.1) to a synthetic
  cored-generator field and report fit residual vs. truncation $L$ and the
  online evaluation speed-up — makes §7.2 quantitative.
- Specify mesh-density rules of thumb (elements per skin depth; near-winding
  refinement) with a convergence study.

## Sources cited
- [@franz2014] forward-model/accuracy dependence. [@jin2014] FEA formulations,
  edge elements, open-boundary treatment. [@jackson1998] solid-harmonic /
  scalar-potential field representation. [@hummel2005] system-level validation
  methodology. [@kindratenko2000] measured-map → correction-model techniques.
