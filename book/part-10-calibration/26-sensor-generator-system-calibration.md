# Chapter 26 — Calibration of Sensors, Generators & Systems

> **Status:** DEEPENED (awaiting review) · **Part X — Calibration**
> Opens Part X. The remedy for the *deterministic* error terms of Ch. 25 §25.3.
> Distortion compensation (the environmental terms) follows in Ch. 27. Citation
> keys resolve to [`../../citations/bibliography.json`](../../citations/bibliography.json).

Calibration is where a tracker's *deterministic* errors — tolerances, model
mismatch, gain/phase offsets — are measured and removed (Ch. 25 §25.3). It is
also where the idealized forward model of Part II is reconciled with the messy
reality of a particular physical unit and its installation. This chapter covers
the three levels of calibration (sensor, generator, system/field-map), the
verification that proves it worked, and the long-term-stability problem that
determines how often it must be repeated. The unifying principle from Ch. 7:
**a tracker is only as accurate as the forward model it inverts** — calibration is
how that model is made true.

---

## 26.1 What calibration can and cannot do

Calibration removes errors that are **stable and repeatable**:

- ✅ **Removable:** per-unit area-turns/axis/geometry tolerances (Ch. 15 §15.1),
  channel gain/phase offsets, frequency-dependent AFE/filter phase (Ch. 17–18),
  cored-generator field shape (Ch. 7 §7.2), *static* environmental distortion
  fixed in the installation.
- ❌ **Not removable by static calibration:** stochastic noise (Ch. 25 §25.2, the
  precision floor), *moving* distorters (Ch. 27), and anything that **drifts**
  after calibration (thermal, aging — §26.6).

This split mirrors Ch. 25's classes: calibration is the deterministic-error tool;
fusion/flagging/witness methods (Ch. 21, 27) handle the environmental ones; and
nothing but lower-noise design and integration beats the stochastic floor.

## 26.2 Sensor characterization

Each sensor's true parameters are measured and stored to replace the nominal
values in the forward model (Ch. 5):

- **Effective area-turns $N_sA_{s,\text{eff}}$** per element (sets channel gain).
- **Element axis directions** $\hat{\mathbf n}_s$ (winding skew, assembly).
- **Inter-element geometry** for multi-element/triad sensors (orthogonality
  error, separation for dual-5-DOF, Ch. 13 §13.3).
- For **biased sensors (TMR)**: per-device sensitivity vs. bias and offset
  (Ch. 25 §25.2), since these vary unit-to-unit and with the chosen bias point
  [@monteblanco2021].

This is typically a **factory** step on a precision fixture; its cost/throughput
is a manufacturing design parameter (Ch. 15 §15.5). The output is a per-sensor
calibration record that travels with the device.

## 26.3 Generator characterization

The generator's *actual* field is mapped against its model:

- **Cored-radiator correction.** Ferromagnetic cores (used for moment, Ch. 9
  §9.1) make the vacuum dipole formula wrong; the real field is captured by FEA/
  BEM (Ch. 7) and/or measurement, then fitted to a fast online representation.
- **Coil geometry & relative placement** for multi-coil planar generators (the
  medical form factor), where superposed fields are not simple co-located dipoles
  (Ch. 9 §9.2).
- **Drive gain/phase** per axis/frequency, and a **monitored drive reference** for
  ratiometric rejection of generator-side noise (Ch. 25 §25.4).

## 26.4 System-level field mapping

The most powerful (and expensive) calibration measures the **realized field /
pose response over the working volume** and builds a correction:

1. **Ground truth.** Move a sensor to many known poses using an independent,
   higher-accuracy reference — a coordinate-measuring machine, a precision robot,
   an optical tracker, or a machined phantom (the Hummel grid plate, §26.5)
   [@hummel2005].
2. **Measure** the tracker's raw output at each pose.
3. **Fit a correction** mapping raw → true. Standard representations, catalogued
   in Kindratenko's survey [@kindratenko2000]: **tri-linear / spline
   interpolation** on a grid, **global high-order polynomials**, **shape
   functions**, and **machine-learning** fits (neural networks, Ch. 27)
   [@kindratenko2005].

**Trade-offs** among representations:
- *Lookup/interpolation*: simple, local, needs dense sampling and memory; doesn't
  extrapolate.
- *Global polynomial*: compact, smooth; risks oscillation (Runge) and poor local
  fit.
- *ML/NN*: flexible, handles position+orientation jointly [@kindratenko2005]; risks
  overfitting and opaque failure (Ch. 27 §27.5).

**Sampling density.** The grid spacing $h$ must resolve the field's spatial
variation: the residual of a *linear* interpolant scales as
$\sim \tfrac18\|\nabla^2 \mathbf B\|\,h^2$, so accuracy improves quadratically as
the grid tightens — but the **acquisition cost scales as $h^{-3}$** (a 0.5 m
volume at a 5 cm grid is $\sim10^3$ points, each measured at several orientations
with the ground-truth fixture). Dense where the gradient is steep (near metal, the
volume edge), coarse where smooth.

**The compact alternative — spherical harmonics.** For the *generator's own*
(source-free) field, a far cheaper representation than a dense LUT is the
solid-harmonic fit of Ch. 7 §7.2 (eq. 7.1): a few dozen coefficients $a_{lm}$
($L\!\sim\!3$–$5$) fit from sparse, well-placed samples give an **analytic,
exactly source-free, closed-form-differentiable** model — which also hands the
solver its Jacobian for free (Ch. 24). The division of labour is clean: harmonics
for the smooth generator field; an interpolation/polynomial **residual map** only
for the part that is *not* source-free (installation distortion, §26.1).

**Model order is a bias–variance trade.** Fitting a degree-$d$ polynomial (or an
NN with $N$ parameters) to $M$ calibration points: too low an order **underfits**
(leaves real structure uncorrected); too high an order with too few points
**overfits** (excellent at the samples, *worse* between them). The right order is
chosen by cross-validation (the no-test-on-training rule of §26.5). The Phase-6
*calibration-workflow* tool demonstrates exactly this: raising the polynomial
degree past what the sample count supports increases the between-sample residual.

A field map captures *installation-specific static distortion* too — but only as
long as the environment does not change (§26.1, Ch. 27).

## 26.5 Verification procedures

Calibration is not done until it is **verified against an independent standard**:

- **Standardized assessment protocols.** The Hummel protocol [@hummel2005] uses a
  machined base plate with a precise grid of holes (50 mm spacing) and a circle of
  equispaced holes for rotation, enabling *reproducible, comparable* measurement
  of residual position/orientation error and the influence of metallic objects —
  the reference method for system-level verification, and for comparing systems
  (Ch. 28). "Best-practice" assessment extends this.
- **Residual reporting.** Quote *post-calibration* error with conditions
  (distance, volume region, distorter presence) — the deterministic floor that
  remains (Ch. 25 §25.3) — not just the best-case bench number.
- **Independent modality cross-check.** Verify against optical/CMM ground truth
  distinct from the data used to *fit* the calibration (no testing on training
  data — a discipline borrowed from ML that applies to *all* calibration).

## 26.6 Long-term stability and recalibration

A calibration is valid only while the device and environment match the calibrated
state:

- **Thermal drift** of coil area/core permeability, MR/TMR offset and bias point,
  and electronics gain is the leading driver of calibration decay (Ch. 15 §15.5,
  Ch. 25 §25.3). The magnitude is concrete: a ferrite-cored coil at ~0.3 %/°C over
  a ±5 °C swing drifts ~1.5% in gain → ~0.5% in range → **~1.5 mm at $r=0.3$ m**
  (Ch. 15 §15.5) — comparable to the *entire* static budget. So the
  **recalibration interval is set by the allowed drift ÷ the drift rate**: if the
  budget allots 0.5 mm to drift and the system drifts ~0.3 mm/°C, a ~1.5 °C
  excursion exhausts it — hence warm-up procedures, temperature compensation
  (bridge sensors, Ch. 14.3.2; referenced gain), and a stated thermal operating
  window, not an open-ended "calibrate once."
- **Aging and mechanical change** (cable wear, connector resistance, fixture
  shift) require periodic **field recalibration** or verification.
- **Self-check.** Some systems include reference/witness coils enabling in-situ
  drift detection (links to the witness-sensor methods of Ch. 27).

> **Engineering takeaway.** Calibration converts the *deterministic* error budget
> (Ch. 25 §25.3) into a small, characterized residual — but it is a perishable
> good. Design for it: make the device reproducible (so factory calibration is
> feasible) and stable (so it stays valid), verify against an independent
> standard, and plan the recalibration interval from the drift data, not hope.

---

## Open questions / to verify
- ✅ **Partially resolved:** §26.4 now covers sampling density ($h^{-3}$ cost,
  $h^2$ residual), the spherical-harmonic compact model, and the bias–variance/
  overfitting trade (Phase-6 calibration tool); §26.6 gives a worked recalibration-
  interval calculation. Remaining: a Phase-5 notebook quantifying *residual vs.
  sampling density* for interpolation vs. polynomial vs. NN, vs. the Kindratenko
  taxonomy [@kindratenko2000; @kindratenko2005].
- Source typical recalibration intervals / drift rates from vendor or clinical
  literature (Ch. 28/29).
- Confirm the exact Hummel phantom geometry parameters (grid pitch, hole count)
  against the primary text [@hummel2005].

## Sources cited
- [@hummel2005] standardized verification protocol/phantom. [@kindratenko2000]
  calibration-method survey. [@kindratenko2005] neural-network calibration.
  [@monteblanco2021] TMR per-device bias/sensitivity. Forward-model dependence
  from Ch. 7; deterministic error classes from Ch. 25.
