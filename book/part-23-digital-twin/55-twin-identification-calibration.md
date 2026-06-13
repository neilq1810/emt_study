# Chapter 55 — Twin Identification: Calibration as Parameter Fitting

> **Status:** DRAFT (awaiting review) · **Part XXIII — Model-Based Engineering & the Digital Twin**
> The chapter that closes the calibration cliff — the single most common reason a *built*
> EM tracker fails to reach spec. It reframes calibration as **identifying the digital
> twin's parameters** from measurements of the real unit, makes the **identifiability**
> question precise (Ch. 24 applied to parameters, not pose), and backs the method with a
> Phase-5 simulation. Builds on the twin/credibility opener (Ch. 53), calibration physics
> (Ch. 26), tolerance (Ch. 15), the forward model (Ch. 7), observability (Ch. 24), the
> golden fixture (Ch. 50), and the differentiable-model frontier (Ch. 30 §30.6). Citation
> keys resolve to [`../../citations/bibliography.json`](../../citations/bibliography.json).

A team can build the generator, the sensor, the front end, and the solver exactly as this
book describes, power it on, and measure 5–15 mm of error — then spend a year unable to
close it. That is the **calibration cliff**, and it sinks real programs because the
published literature (this book included) teaches the *physics* of calibration (Ch. 26) but
not the *procedure* that reaches sub-millimetre, which is the vendors' core IP. The digital
twin reframes the problem in a way that is teachable without giving away anyone's tuned
numbers: **calibration is the inverse problem of identifying the twin's parameters.** This
chapter makes that precise, identifies the one analysis that separates a working
calibration from a diverging one, and demonstrates — quantitatively — that the reframing
turns a 15 mm tracker into a 0.1 mm tracker.

---

## 55.1 Calibration *is* twin identification

The forward twin (Ch. 53) predicts the measurement $\mathbf z = h(\mathbf x;
\boldsymbol\theta)$ from the pose $\mathbf x$ **and a parameter vector $\boldsymbol\theta$**
— coil gains and positions, sensor effective-areas and non-orthogonality, the volumetric
field-map coefficients (Ch. 7 §7.2), and a distortion residual (the *environment-twin*
chapter). The *nominal*
model assumes design values $\boldsymbol\theta_0$; the *real unit* deviates by its
manufacturing tolerances (Ch. 15). Two inverse problems share one machinery (Ch. 23):

- **Pose estimation (operation):** $\boldsymbol\theta$ fixed (calibrated), estimate
  $\mathbf x$ from one measurement.
- **Calibration (identification):** $\mathbf x$ *known* (a golden fixture, Ch. 50),
  estimate $\boldsymbol\theta$ from many measurements at known poses.

So calibration is not a separate art — it is **the same least-squares solve, with the roles
of known and unknown swapped**, fitting the twin to the unit:
$$
\hat{\boldsymbol\theta} = \arg\min_{\boldsymbol\theta}\ \textstyle\sum_k
\big\| h(\mathbf x_k;\boldsymbol\theta) - \mathbf z_k \big\|^2 ,
\qquad \{\mathbf x_k\}\ \text{known}.
\tag{55.1}
$$
Solving with the nominal $\boldsymbol\theta_0$ instead of $\hat{\boldsymbol\theta}$ is
exactly the mistake that produces the cliff.

## 55.2 The identifiability question — Ch. 24, applied to parameters

The decisive subtlety, and the thing that separates a calibration that *converges* from one
that *diverges*, is **identifiability**: not every parameter is recoverable from the data.
This is the observability analysis of Ch. 24 — but applied to the **calibration Jacobian**
$\partial h/\partial\boldsymbol\theta$ instead of the pose Jacobian $\partial h/\partial
\mathbf x$. The calibration Fisher information $\mathbf F_\theta = \sum_k (\partial
h/\partial\boldsymbol\theta)^\top\mathbf R^{-1}(\partial h/\partial\boldsymbol\theta)$ has
the same story: a zero eigenvalue is an **unidentifiable parameter combination**, a small
one a weakly-identifiable one.

The canonical EMT example is the **transmit/sensor gain degeneracy**: if the measurement is
$M_{ji}=s_j\,g_i\,M^{\text{ideal}}_{ji}$, only the **products** $s_j g_i$ affect the data, so
six gain parameters collapse to a rank-5 identifiable set (one null direction: $g\to\alpha
g,\ s\to s/\alpha$). Fitting all six anyway lets the solver wander along the null direction —
the calibration "diverges" not from a bug but from over-parameterization. The fix is the
same as for an unobservable pose: **fix the redundant combination by convention** (set
$g_1\equiv1$) or constrain it, and fit only what the data determines. *The identifiability
analysis must be done before the calibration, not discovered after it fails.*

## 55.3 The golden fixture, and how few poses suffice (computed)

Equation (55.1) needs measurements at **known** poses — a **golden fixture** holding a
reference sensor at machined, traceable positions (Ch. 50 §50.1–50.2). How many poses?
Identifiability answers it: each known pose contributes a full $3\times3=9$-measurement
constraint on $\boldsymbol\theta$, so a low-dimensional parameter set is pinned by very few
poses.

**Computed (Phase-5, `data/twin_identification.json`,
`figures/ch55_twin_identification.png`).** With **±5 % per-axis transmit and sensor gain
errors** (a realistic Ch. 15 tolerance), the nominal-model solver gives a position **RMS of
14.9 mm** across the volume — clinically useless, and exactly the "built it, can't close it"
symptom. Identifying the gains from a golden-fixture set via (55.1) recovers the
(scale-free) product matrix to **0.01 %** and drops the calibrated-twin solver to **0.11 mm
RMS — a 132× improvement**, back to the noise floor. And because the six gains carry only
five identifiable degrees of freedom against nine measurements per pose, the parameters are
pinned by a **single known pose** (the over-determination is why gains calibrate so
cheaply). This is the calibration cliff, closed — *as method*. (conf: high — computed; the
absolute improvement depends on the assumed tolerance and noise, but the structure is
exact.)

## 55.4 Scaling to the real twin: the parameter hierarchy and factory amortization

The gain demo is the *simplest identifiable subset*; a product twin carries a parameter
**hierarchy**, cheap to expensive:

| Level | Parameters | Count | Known-pose demand |
|---|---|---|---|
| Per-channel gain/offset | $s_j, g_i$, baselines | ~6–12 | few poses (§55.3) |
| Sensor geometry | effective area, axis, non-orthogonality | ~3–6 | modest |
| Coil pose | generator coil positions/orientations | ~tens | many, spread |
| **Volumetric field map** | harmonic coefficients $a_{lm}$ (Ch. 7 §7.2) | tens–hundreds | dense volumetric scan |
| Distortion residual | environment field (environment-twin chapter) | many | per-room (Ch. 52) |

This hierarchy answers the open question Ch. 50 §50.2 posed — *which DOF to calibrate per
unit*. The economical architecture is **identify the expensive, high-dimensional field map
once at the design level** (a slow, dense reference characterization), then **per-unit
identify only the low-dimensional subset that actually varies between units** (the gains and
a little geometry, §55.3) — inheriting the design-level map. Calibration throughput at the
factory (Ch. 50) is therefore set by *how few parameters are unit-specific*, which the
identifiability analysis (§55.2) quantifies.

## 55.5 The differentiable-twin inverse

When the forward model is **differentiable** (the harmonic field surrogate, Ch. 7; the
frontier of Ch. 30 §30.6), (55.1) is solved by gradient descent and gains a powerful
extension: **co-identify the physical parameters and a learned residual** for what the
physics misses (a PINN, [@raissi2019]), while the physics supplies the inductive bias that
keeps the fit identifiable and the covariance interpretable. This is the principled form of
ML calibration the book argued for (Ch. 27 §27.5, Ch. 30 §30.6): learn the *residual on a
physical twin*, not a black-box raw→true map that discards identifiability and extrapolates
unpredictably outside its training poses.

## 55.6 Credibility: validate on held-out poses, not the calibration set

An identified twin is a computational model, so Ch. 53's credibility rule binds it: it must
be **validated on poses it was not calibrated on**. Fitting the calibration set well proves
nothing — it is the *no-testing-on-training-data* discipline of Ch. 26 §26.5 and Ch. 33,
and the held-out residual is the twin's **validation evidence** (ASME V&V 40 [@asme_vv40]).
An identified twin that nails its golden poses and misses held-out poses is **overfit** —
the calibration analogue of the "sixth way to fail" (Ch. 53): a confident, wrong model. The
honest calibration report is therefore not "the fit residual was small" but "the *held-out*
target error was X mm across the working volume," characterized exactly as in Ch. 33.

> **Engineering takeaway.** Calibration *is* twin identification — the same least-squares
> solve as pose estimation (Ch. 23) with known and unknown swapped: hold the pose known on a
> **golden fixture** and fit the twin's parameters (55.1). The make-or-break step is the
> **identifiability analysis** — Ch. 24's observability applied to the *calibration*
> Jacobian — which tells you which parameter combinations the data determines (e.g. only the
> rank-5 gain *products*, not all six gains); fit only those, or the calibration diverges by
> over-parameterization. Done right it is dramatic: a Phase-5 demo turns a **14.9 mm**
> uncalibrated tracker into **0.11 mm (132×)** by identifying ±5 % gain errors, with the
> parameters pinned by **one** known pose. Scale by the **parameter hierarchy** — identify
> the expensive field map once at design level, per-unit identify only the few varying DOF
> (closing the Ch. 50 §50.2 question) — prefer the **differentiable/PINN inverse** (learn the
> residual on the physics, Ch. 30 §30.6), and **validate on held-out poses** (Ch. 53 V&V 40),
> because an overfit twin is just the sixth failure wearing a calibration hat. This is the
> calibration cliff closed *as method* — the tuned values remain the builder's to measure.

---

## Open questions / to verify
- Extend sim 13 to **field-map identification** (fit low-order harmonic $a_{lm}$ from a
  volumetric golden scan) and report the poses-vs-parameters demand and held-out error —
  the realistic calibration, not just gains.
- Add a worked **calibration-Jacobian conditioning** map showing which physical parameters
  are weakly identifiable in a given generator geometry (ties §55.2 to Ch. 9/24).
- Demonstrate the **differentiable/PINN co-identification** (§55.5) on a synthetic
  physics-plus-residual case, with a credibility (held-out) assessment per Ch. 53.

## Sources cited
- [@raissi2019] physics-informed neural networks — the differentiable co-identification of
  §55.5; [@asme_vv40] computational-model credibility — the held-out validation of §55.6.
  Identification machinery is the inverse problem of Ch. 23; identifiability is Ch. 24
  applied to the calibration Jacobian; tolerance (the parameters that vary) is Ch. 15;
  the forward/field model is Ch. 7; the golden fixture and factory amortization are Ch. 50;
  the credibility frame is Ch. 53; the distortion residual is the environment-twin chapter. Computed in
  `simulations/run_all.py` (sim 13).
