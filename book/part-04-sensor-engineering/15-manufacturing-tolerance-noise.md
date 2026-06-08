# Chapter 15 — Manufacturing, Tolerance & Noise

> **Status:** DEEPENED (awaiting review) · **Part IV — Sensor Engineering**
> Closes Part IV. Builds on Ch. 13–14. Feeds the AFE (Ch. 16), ADC (Ch. 18),
> and the error budget (Ch. 25). Citation keys resolve to
> [`../../citations/bibliography.json`](../../citations/bibliography.json).

A sensor's *design* sets its best-case performance; its *manufacturing* sets
what you actually ship. This chapter covers the three things that turn an ideal
sensor into a real, calibratable, noise-limited component: **tolerance** (how
much do unit-to-unit variations move the forward model?), **sensitivity** (how
do those variations and the environment map into pose error?), and **noise**
(the fundamental floor below which no calibration helps). These quantities are
the sensor-side inputs to the system error budget of Part IX.

---

## 15.1 Tolerance analysis

The forward model (Ch. 5, eq. 5.3/5.6) assumes exact knowledge of each sensing
element's **effective area-turns $N_sA_s$**, its **axis direction**
$\hat{\mathbf n}_s$, and (for multi-element sensors) the **relative geometry**
between elements. Manufacturing perturbs all three:

| Parameter | Source of variation | First-order effect on measurement |
|---|---|---|
| Effective area $A_s$ | winding count/pitch, core $\mu_r$ spread, layer geometry | scales coupling → gain error per axis |
| Axis direction $\hat{\mathbf n}_s$ | winding skew, assembly misalignment | rotates the sensed projection → orientation bias |
| Inter-element angle (triad) | mechanical assembly tolerance | off-diagonal coupling errors → roll/orientation error |
| Core properties | ferrite batch, temperature | gain + nonlinearity, drift (§15.3) |
| Element position offset | placement within package | small position bias (matters at the tip, Ch. 14.2) |

Two responses, used together:
1. **Per-unit calibration** (Ch. 26) measures and stores each sensor's true
   $N_sA_s$, axes, and geometry, folding them into the forward model — this
   removes *stable, repeatable* tolerance errors (the majority). The
   factory-calibration burden is itself a cost/throughput design parameter.
2. **Tolerancing for what calibration can't fix** — drift, hysteresis,
   temperature dependence, and anything that changes after calibration. These
   set the *residual* tolerance that enters the error budget.

A practical rule: **make the sensor reproducible enough that a feasible
calibration can capture it, and stable enough that the calibration stays valid.**
Reproducibility (PCB/MEMS/MR batch processes) and stability (materials,
mechanical design) are therefore first-class manufacturing goals.

**How tolerances map to error (the propagation rules).** Each tolerance enters
through a known sensitivity coefficient (Ch. 25 §25.5):
- **Effective-area / gain error** $\delta A/A=\varepsilon$ is a fractional
  amplitude error. Because the dipole amplitude $\propto r^{-3}$, it maps to range
  via the **cube root**: $\delta r/r = \tfrac13\varepsilon$ (the "cube-root
  forgiveness" of Ch. 25). So a **±1% area tolerance → ±0.33% range** → ±1.0 mm at
  $r=0.3$ m.
- **Axis misalignment** $\delta\theta_n$ rotates the sensed projection, mapping
  ~1:1 into an **orientation bias** of order $\delta\theta_n$ (with a small
  coupled position term).
- **Inter-element angle error** $\delta\alpha$ in a triad/dual sensor corrupts the
  off-diagonal couplings → a **roll/orientation bias** of order $\delta\alpha$
  (and, near the small-angle degeneracy of Ch. 13 §13.3, with amplified
  sensitivity).

These are *deterministic* contributions — calibration removes the stable part;
the residual and the drift (§15.5) are what remain in the budget.

## 15.2 Sensitivity analysis

Sensitivity analysis asks: *given a perturbation $\delta p$ in some parameter
$p$ (a tolerance, a temperature change, a field distortion), how large is the
resulting pose error $\delta\mathbf{x}$?* Formally it is the Jacobian
$\partial \mathbf{x}/\partial p$, evaluated through the measurement-to-pose map
(Stage 3, Ch. 11). Key points:

- The map is **pose-dependent**: the same tolerance produces different pose
  error at different locations/orientations in the volume, because the forward-
  model Jacobian (and its conditioning) varies in space (Ch. 5 §5.7, Ch. 24).
  Worst-case sensitivity often occurs at the volume edges and at poorly
  observable orientations.
- It is **parameter-specific**: gain errors (area) tend to map into *range*
  error (via the $1/r^3$ amplitude); axis/angle errors map into *orientation*
  error. Knowing which tolerance dominates which DOF guides where to spend
  manufacturing precision.
- Sensitivity analysis is the bridge from component specs (this chapter) to the
  system **error budget** and **Monte Carlo** analysis of Ch. 25, and to the
  **covariance/CRLB** of Ch. 24.

**Worked tolerance → pose table** (mid-volume, $r=0.3$ m; using the §15.1
propagation rules). This is the *residual* after calibration would normally be
much smaller; the values are pre-calibration to size the manufacturing spec:

| Tolerance | Example value | Maps to | Pose contribution |
|---|---|---|---|
| Effective area $\delta A/A$ | ±1% | range (÷3) | ±0.33% → **±1.0 mm** |
| Axis misalignment $\delta\theta_n$ | ±1° | orientation bias | **±1°** (+ small position) |
| Inter-element angle $\delta\alpha$ | ±0.5° | roll/orientation | **±0.5°** (amplified near small angles, Ch. 13) |
| Element position offset | ±0.1 mm | position | **±0.1 mm** |
| Tip offset error (115 mm lever) | ±0.5° pointing | tip position | **±1.0 mm** at the tip (Ch. 14.2) |

The table shows where to spend precision: **area/gain dominates *range*,
angles dominate *orientation*, and the tip lever-arm can dominate the
*clinically relevant* tip error** even when the sensor itself is accurate — which
is why calibration (Ch. 26) targets exactly these parameters. The stochastic
counterpart (noise → pose) is validated by the Phase-5 Monte-Carlo (Ch. 24,
`data/monte_carlo_vs_crlb.json`).

## 15.3 Sensor self-noise: the fundamental floor

Below all tolerances lies stochastic noise that calibration cannot remove. The
dominant mechanisms differ by sensor type (Ch. 13.0):

### Induction coils — thermal (Johnson) noise
A coil of resistance $R$ at temperature $T$ has open-circuit voltage noise
spectral density

$$
\overline{v_n} = \sqrt{4 k_B T R}\quad[\text{V}/\sqrt{\text{Hz}}],
\tag{15.1}
$$

independent of frequency (white), while the *signal* grows as $\omega N_sA_sB$
(Ch. 5). Hence the **coil SNR improves with frequency** (signal ∝ ω, noise flat)
— a key reason AC systems push frequency up until eddy distortion (Ch. 6) forces
a stop. Minimizing $R$ (thicker wire, fewer-but-larger turns, lower temperature)
and maximizing $N_sA_s$ are the levers. The coil's self-resonance (with its
parasitic capacitance) bounds the usable frequency from above. (conf: high —
(15.1) is the Johnson–Nyquist result; the ∝ω SNR follows from Ch. 5.)

*Worked floor:* a coil with $R = 100\,\Omega$ at $T=300\,\text{K}$ has
$\overline{v_n}=\sqrt{4(1.38\times10^{-23})(300)(100)}\approx 1.29\,\text{nV}/\sqrt{\text{Hz}}$.
Over a $1\,\text{Hz}$ effective bandwidth (long integration, Ch. 11) that is
~1.3 nV RMS — setting the scale the AFE (Ch. 16) must not spoil. (conf: high —
Johnson–Nyquist [@horowitz_hill].)

### Magnetoresistive sensors — 1/f-dominated
MR/TMR sensors are limited at EMT frequencies by **1/f (flicker) noise**, not
white noise (Ch. 14.3.4): the noise spectral density rises toward low frequency,
detectivity improves with die area, and the floor is quasi-fundamental for a
given area [@davies2021]. The mitigations are architectural — larger area,
bridge configuration, set/reset and chopping to operate above the 1/f corner
(Ch. 14.3.2–3). Unlike the coil's flat noise, the MR floor must be quoted *with
its frequency* (e.g. value @ 1 Hz).

### Fluxgate and others
Fluxgates reach very low (pT-class) DC noise but are larger/power-hungry
[@lenz2006]; OPM/NV reach fT–pT at the cost of bandwidth/size (Ch. 30). Each has
a characteristic noise model that must enter the budget with its conditions.

## 15.4 From sensor noise to pose noise
Sensor voltage/field noise becomes *pose* noise only after passing through the
amplitude estimator (Ch. 11 §11.1, ∝1/√τ) and the forward-model Jacobian
(Ch. 11 §11.5, geometry-dependent gain). Therefore:

$$
\sigma_\text{pose} \;\sim\; \underbrace{\frac{\sigma_\text{sensor}}{\sqrt{\tau}\,\cdot\,(\text{signal level})}}_{\text{measurement SNR}}\;\times\;\underbrace{\|J^{-1}\|}_{\text{geometric amplification}}.
$$

This single relation ties the whole part together: **noise (this chapter) ×
integration (Ch. 11) ÷ signal (Ch. 9, via $m_t/r^3$) × conditioning (Ch. 24) =
pose uncertainty (Ch. 25).** It also explains the field's recurring trades:
more moment, lower-noise sensor/AFE, longer integration, and better-conditioned
geometry all reduce $\sigma_\text{pose}$, each at a known cost (size, latency,
update rate, working volume).

## 15.5 Thermal drift and stability

Thermal drift is the leading reason a valid calibration goes stale, so its
coefficients deserve real numbers (conf: med — material- and part-dependent):

| Source | Typical tempco | What it moves | EMT effect |
|---|---|---|---|
| Copper winding resistance | **+0.39 %/°C** | $R$ (hence coil noise, $Q$, resonant tuning) | shifts AC sensitivity & resonance, not gain directly |
| Ferrite core $\mu_r$ | ~+0.1 to +1 %/°C (grade-dependent) | effective area $A_\text{eff}$ → **gain** | **range** drift via the cube root |
| TMR/MR sensitivity & offset | ~−0.1 to −0.3 %/°C + offset drift | bias point | gain + bias drift (bridge & set/reset mitigate) |

A worked implication: a ±5 °C swing on a ferrite-cored coil at ~0.3 %/°C is a
~1.5% gain drift → ~0.5% range drift → **~1.5 mm at $r=0.3$ m** — comparable to
the entire static budget (Ch. 25), and far larger than the ~nV noise floor. This
is *the* number that sets the **recalibration interval** and motivates warm-up
procedures, temperature compensation (bridge sensors, Ch. 14.3.2; referenced
gain), and thermally stable cores/formers. The manufacturing goals follow:
- **Reproducibility** so factory calibration (Ch. 26) is feasible at scale.
- **Mechanical & thermal stability** so calibration stays valid in the field.
- **Low and characterized noise** so the budget is predictable.
- **Documented, traceable variation** so the error budget (Ch. 25) and
  regulatory submissions (Ch. 29) rest on data, not assumption.

This is the clean handoff into Part V (the AFE that must preserve the
~nV-class coil floor) and Part X (the calibration that captures the tolerances).

---

## Open questions / to verify
- ✅ **Resolved:** §15.2 now has a worked tolerance→pose table (area→range via
  cube root, angles→orientation, tip lever-arm), and §15.5 gives thermal-drift
  coefficients with the recalibration-interval implication. Remaining: replace the
  representative tempco ranges with values for the *specific* ferrite grade / TMR
  part chosen in a given design (cite per design).
- Verify the self-resonance frequency bound example for a realistic catheter
  coil (Ch. 9 §9.5).

## Sources cited
- [@horowitz_hill] Johnson–Nyquist noise (15.1) & low-noise design. [@davies2021]
  MR/TMR 1/f & area-limited detectivity. [@lenz2006] fluxgate/other noise floors.
  Copper tempco & ferrite μ_r(T): standard material data (grade-dependent).
