# Chapter 7 — Analytical & Numerical Field Methods

> **Status:** DRAFT · **Part II — Electromagnetic Theory**
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

## 7.3 Finite element analysis (FEA)

FEA solves the magnetostatic (or low-frequency eddy-current) boundary-value
problem on a discretized mesh. For EMT the relevant formulations are:

- **Magnetostatic** ($\nabla\times\mathbf{H}=\mathbf{J}$,
  $\nabla\cdot\mathbf{B}=0$), usually via a magnetic vector potential
  $\mathbf{A}$ with $\mathbf{B}=\nabla\times\mathbf{A}$, to model the generator
  with its ferromagnetic core and winding geometry.
- **Low-frequency eddy-current (A–V) formulation** to model the *distortion*
  physics of Ch. 6: induced currents in nearby conductors as a function of
  excitation frequency, capturing the skin-depth behavior of eq. (6.1).

Practical FEA requirements specific to EMT:

1. **Open-boundary truncation.** The near field decays slowly ($1/r^3$), so the
   computational domain must extend well beyond the working volume, or use
   infinite/absorbing boundary elements, to avoid artificial image effects.
2. **Mesh refinement where the gradient is steep** — near windings and core
   edges — since pose accuracy depends on the field *gradient* (Ch. 5 §5.7).
3. **Material curves.** Core $\mu_r(H)$ nonlinearity and saturation must be
   modeled if the generator is driven hard for moment.

General-purpose solvers (e.g. ANSYS-class magnetostatic/eddy-current modules)
are the standard tooling; the discipline of **quantitative assessment** of such
magnetostatic FEA models against analytic benchmarks is itself a studied subject
(conf: med — to be cited from the magnetostatic-FEA assessment literature, see
*Open questions*).

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
   (Ch. 4 §4.4 / Ch. 5 worked example), and dipole far-field limit. These are
   the cheap sanity checks every implementation must pass.
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
- Attach a primary citation for cored-radiator field modeling / FEM-based
  field-generator calibration (candidate: magnetostatic-FEA assessment paper in
  *Nucl. Instrum. Methods A*, 2021 — verify and add to bibliography).
- Add a worked FEA-vs-dipole comparison figure (Phase 5, `simulations/`) and a
  digitized field-map dataset (`data/`) to make §7.2–7.3 quantitative.
- Specify recommended open-boundary treatment and mesh-density rules of thumb
  with a sourced example.

## Sources cited
- [@franz2014] forward-model/accuracy dependence. [@hummel2005] system-level
  validation methodology. [@kindratenko2000] measured-map → correction-model
  techniques.
