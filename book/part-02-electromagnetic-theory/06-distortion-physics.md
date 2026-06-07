# Chapter 6 — Distortion Physics: Conductors, Ferromagnetics & Eddy Currents

> **Status:** DEEPENED (awaiting review) · **Part II — Electromagnetic Theory**
> Builds on Ch. 4 (fields) and Ch. 5 (coupling). Citation keys resolve to
> [`../../citations/bibliography.json`](../../citations/bibliography.json).

Field distortion is the original sin of electromagnetic tracking. The same
near-field magnetic coupling that lets EMT see through tissue also couples into
any nearby **conductor** (inducing eddy currents) or **ferromagnetic** object
(concentrating flux). Both perturb the field the sensor measures, corrupting the
pose estimate in ways that are *spatially structured* and therefore not
removable by simple averaging. This chapter develops the physics of the two
distortion mechanisms, explains the **AC-vs-pulsed-DC** architectural response,
and frames what calibration (Part X) can and cannot fix. The headline practical
fact, repeatedly confirmed in the literature, is that **AC systems are more
sensitive to conductive (eddy-current) distortion, while ferromagnetic material
distorts both AC and DC systems** [@franz2014; @birkfellner1998].

---

## 6.1 Two distinct mechanisms

It is essential to separate two physically different effects that are often
lumped together as "metal distortion":

| Mechanism | Cause | Material | Frequency behavior |
|---|---|---|---|
| **Eddy currents** | Faraday induction in a conductor → secondary field | Any conductor (Al, Cu, stainless steel, 3D-US probe) | Grows with frequency; transient after a step |
| **Ferromagnetic concentration** | High $\mu_r$ reshapes/short-circuits flux | Iron, mild steel, ferrite, some surgical steels | Present even at DC; ~frequency-independent |

The distinction is decisive: pulsed-DC architectures can largely *wait out*
eddy currents but **cannot** escape ferromagnetic distortion, because the latter
exists in the static limit. (conf: high — standard, and stated in the review
[@franz2014].)

## 6.2 Eddy currents: Faraday + Ohm

A time-varying applied field $\mathbf{B}_0(t)$ threads a conductor and, by
Faraday's law, drives a circulating EMF; Ohm's law turns that EMF into a current
density $\mathbf{J}=\sigma\mathbf{E}$. These **eddy currents** are themselves a
magnetic dipole (and higher multipoles) that radiate a **secondary field**
$\mathbf{B}_\text{eddy}$ opposing the change (Lenz's law). The sensor measures
$\mathbf{B}_0+\mathbf{B}_\text{eddy}$, so the inferred coupling matrix
$\mathbf{M}$ (Ch. 5) is wrong.

For sinusoidal excitation, the induced eddy current — and hence the distortion —
scales (to first order, well below the conductor's self-resonance) **linearly
with frequency** $\omega$, because the driving EMF is $\propto d\mathbf{B}/dt
\propto\omega$. This is the quantitative reason AC systems pay a distortion
penalty that *worsens* as you raise frequency to gain sensitivity (Ch. 5, §5.2):
the very $\omega$ that buys signal also buys distortion. Designers therefore
choose AC frequencies as a **compromise** between SNR and eddy-current
immunity. (conf: high — first-order $\omega$ scaling is standard; exact behavior
requires the skin-depth treatment below.)

### Skin depth
At higher frequencies the eddy currents are confined to a surface layer of
thickness

$$
\delta=\sqrt{\frac{2}{\omega\mu\sigma}}=\frac{1}{\sqrt{\pi f\mu\sigma}} .
\tag{6.1}
$$

For copper ($\sigma\approx5.8\times10^{7}\,\text{S/m}$, $\mu\approx\mu_0$) at
$f=10\,\text{kHz}$:

$$
\delta=\frac{1}{\sqrt{\pi (10^4)(4\pi\times10^{-7})(5.8\times10^7)}}\approx 6.6\times10^{-4}\,\text{m}\approx0.66\,\text{mm}.
$$

Computed skin depths at 10 kHz (Phase-5 simulation, `data/skin_depth.json`,
`figures/ch06_skin_depth.png`) make the material dependence concrete:

| Material (10 kHz) | $\sigma$ [S/m] | $\delta$ [mm] |
|---|---:|---:|
| Copper | $5.8\times10^7$ | **0.66** |
| Aluminium | $3.5\times10^7$ | 0.85 |
| Stainless 304 (non-magnetic) | $1.4\times10^6$ | 4.25 |

(The copper value reproduces the hand calculation above.) When the conductor is
thick compared with $\delta$, the field is excluded from its interior and the
eddy-current response saturates and develops a characteristic phase lag; when it
is thin compared with $\delta$, the response is volumetric and grows with
thickness. Skin depth thus sets *which* nearby metal matters at a given frequency
and *how* its distortion scales — a key input to the EMC and
mechanical-integration choices of Part V and Chapter 9. (conf: high — (6.1) is
the standard skin-depth result; values computed in Phase 5.)

## 6.3 Ferromagnetic materials

A material with relative permeability $\mu_r\gg1$ provides a low-reluctance path
that **concentrates and reshapes** magnetic flux. The canonical solvable case is
a permeable sphere of radius $a$ in a uniform field $\mathbf B_0$, which acquires
an **induced magnetic dipole** (the magnetostatic analogue of Clausius–Mossotti)
[@jackson1998]:

$$
\mathbf m_\text{ind} = \frac{4\pi a^3}{\mu_0}\,\frac{\mu_r-1}{\mu_r+2}\,\mathbf B_0
\;\xrightarrow{\ \mu_r\to\infty\ }\; \frac{4\pi a^3}{\mu_0}\,\mathbf B_0 .
\tag{6.2}
$$

Two features are decisive: the moment is **parallel** to $\mathbf B_0$ (flux is
*concentrated*, sign opposite to the conductor case of §6.5), and it has **no
$\omega$ dependence** — it exists in the **static** limit, because this is a
magnetostatic boundary-value problem, not an induction problem. Hence
ferromagnetic distortion afflicts pulsed-DC systems exactly as it does AC ones. Ferromagnets additionally exhibit **hysteresis** and
**nonlinearity** (the response depends on field history and amplitude), which
makes ferromagnetic distortion harder to calibrate out than the (linear,
repeatable) eddy-current distortion of a fixed conductor in a fixed AC field.
The practical consequence stated throughout the medical literature: keep
ferromagnetic instruments (and steel furniture, OR tables) out of the working
volume, because no architecture fully escapes them [@franz2014; @birkfellner1998].
(conf: high.)

## 6.4 The pulsed-DC rationale: settling of eddy currents

This is the central architectural insight of Chapter 1, §1.6, now made physical.
A **pulsed-DC** system energizes a transmitter axis with a current *step* and
holds it. Immediately after the step, large transient eddy currents flow in
nearby conductors; but with no further $d\mathbf{B}/dt$ driving them, those
currents **decay** with the conductor's L/R time constant. If the system
**waits** for this decay and samples the field only afterward, it measures the
(eddy-current-free) static field — which, for non-ferromagnetic conductors, is
*undistorted*. The trade-offs:

- **Pro:** strong immunity to *conductive* (non-ferromagnetic) distortion.
- **Con:** requires a sensor that responds to (quasi-)static fields
  (fluxgate/magnetoresistive magnetometers rather than a simple AC pickup coil,
  since a coil's EMF $\propto d\Phi/dt\to0$ in the static hold), a slower
  effective update because of the settling wait, and *no* relief from
  ferromagnetic distortion.

**Quantifying the settling time.** The eddy current in a conductor decays by
magnetic diffusion; for a sphere of radius $a$ and conductivity $\sigma$ the
slowest mode has time constant

$$
\tau_e = \frac{\mu_0\sigma a^2}{\pi^2}.
\tag{6.3}
$$

This depends **quadratically on size** and linearly on conductivity, so the
*largest, most conductive* nearby object dominates. Worked values for copper
($\sigma=5.8\times10^7$):

| Copper object | $\tau_e$ (eq. 6.3) | wait $\sim5\tau_e$ | max rate |
|---|---:|---:|---:|
| 1 cm | 0.74 ms | 3.7 ms | ~270 Hz |
| 5 cm | 18 ms | 92 ms | ~11 Hz |

So a fist-sized conductor in the volume can throttle a pulsed-DC system to ~10 Hz
— a concrete statement of the settling-vs-rate trade. Choosing the sample instant
is an explicit design parameter: too early leaves a residual eddy bias (a
*deterministic* error, Ch. 25 §25.3); too late wastes update rate and SNR
(Ch. 20 §20.6). (conf: high — (6.3) is the standard sphere eddy-decay result
[@jackson1998]; consistent with the pulsed-DC rationale of [@franz2014].)

## 6.5 Field-perturbation theory and image models

For quantitative modeling, two complementary tools:

1. **Induced-dipole (polarizability) model.** Treat the conductor as acquiring an
   induced dipole $\mathbf m_\text{ind}=\alpha(\omega)\,\mathbf B_0(\text{at
   conductor})$. For a conducting sphere of radius $a$ the polarizability is known
   exactly (spherical Bessel functions [@jackson1998]); the two limits are what
   matter:
   $$
   \mathbf m_\text{ind} \approx
   \begin{cases}
   -\,\dfrac{2\pi a^3}{\mu_0}\,\mathbf B_0, & a\gg\delta\ \text{(perfect-conductor limit: field expelled)}\\[2mm]
   -\,j\,C\,\dfrac{a^2}{\delta^2}\,\dfrac{a^3}{\mu_0}\,\mathbf B_0\ \propto\ -j\,\omega, & a\ll\delta\ \text{(low-frequency limit)}
   \end{cases}
   $$
   So the conductive induced moment is **opposite** to $\mathbf B_0$ (Lenz; field
   *expelled*, unlike the ferromagnet of §6.3) and **grows $\propto\omega$ at low
   frequency, then saturates** at $|\mathbf m_\text{ind}|=2\pi a^3 B_0/\mu_0$ once
   $a\gtrsim\delta$. This is the quantitative form of "AC conductive distortion
   rises with frequency" (§6.2) — it rises, then plateaus near the skin-depth
   crossover $a\sim\delta$. (The Phase-6 *distortion visualizer* uses exactly the
   perfect-conductor limit, $\mathbf m_\text{ind}=-(2\pi a^3/\mu_0)\,\mathbf B_0$.)
   The distortion at the sensor is then a *second* $1/r^3$ dipole field added to
   the primary.
2. **Image methods.** For simple geometries (a coil above an infinite
   conducting or permeable half-space), the perturbed field equals that of an
   **image source** behind the boundary. Image models give closed-form intuition
   for the sign and scaling of distortion near large flat conductors (e.g. an OR
   table) and are useful sanity checks for the FEA/BEM models of Chapter 7.

These analytic tools complement the numerical methods of Chapter 7 and the
*empirical* field-mapping of Chapter 26.

## 6.6 Quantifying and characterizing distortion

Distortion is characterized empirically by mapping pose error as a function of
(a) the type, size, and geometry of the intruding material, (b) its distance
from the coils, and (c) the excitation frequency. Foundational characterizations
(e.g. Birkfellner et al. on systematic distortions in magnetic digitizers
[@birkfellner1998]) and the standardized assessment protocols (Hummel et al.
[@hummel2005], which explicitly include "the influence of metallic objects in
the operating volume") provide the methodology. Reported behavior consistently
shows that:

- distortion **decays rapidly with distance** from the offending object;
- distortion **increases with object size and conductivity** (more eddy current)
  and dramatically with **ferromagnetic content**;
- AC systems show **frequency-dependent** conductive distortion; pulsed-DC
  systems show little conductive but full ferromagnetic distortion
  [@franz2014; @birkfellner1998].

**A scaling law for the distortion fraction.** Chaining the §6.5 induced-dipole
through the two $1/r^3$ falloffs makes the distance dependence concrete. With a
generator–sensor separation $r$, a distorter at distance $d_t$ from the generator
and $d_s$ from the sensor, the perturbation field relative to the primary at the
sensor scales (perfect-conductor regime) as

$$
\frac{|\mathbf B_\text{pert}|}{|\mathbf B_0|}\ \sim\ \frac{a^3\,r^3}{d_t^3\,d_s^3}.
\tag{6.4}
$$

Two lessons: distortion grows as the **cube of conductor size** $a^3$ and falls
**very steeply** — as $1/d_t^3$ *and* $1/d_s^3$ (an overall $\sim1/d^6$ if the
object moves away from both). This is why **keeping distorters a modest distance
out of the volume is so effective**, and why a small steel tool *at the sensor
tip* ($d_s\to0$) is catastrophic while the same tool across the room is
invisible. Equation (6.4) is the analytic backbone of the Phase-6 distortion
visualizer and the witness-sensor compensation of Ch. 27. (conf: med — scaling
derivation; absolute coefficients are geometry-dependent and best taken from FEA
(Ch. 7) or measurement [@birkfellner1998].)

> **Engineering takeaway.** Distortion is *not* random noise — it is a smooth,
> repeatable, spatially structured field error. That repeatability is exactly
> what makes **calibration / field-mapping** (Ch. 26–27) viable for *static*
> distorters, and what makes *moving* distorters (a steel instrument advancing
> in the field) the genuinely hard, open problem (witness-sensor and ML
> approaches, Ch. 27 and Part XIII). The survey of calibration techniques by
> Kindratenko [@kindratenko2000] catalogs the static-correction toolbox.

---

## Open questions / to verify
- ✅ **Resolved:** induced-dipole polarizability now given for both conductors
  (perfect-conductor & low-freq limits, §6.5) and ferromagnets (eq. 6.2, §6.3),
  with the eddy-decay time constant (eq. 6.3) and the distortion-vs-distance
  scaling (eq. 6.4) [@jackson1998]. Remaining: full Bessel-function $\alpha(\omega)$
  and a validating Phase-5 eddy-current sim against (6.4).
- Re-confirm Birkfellner (1998) DOI/pages against the Wiley *Medical Physics*
  record (currently 25(11):2242–2248, DOI 10.1118/1.598425 — **to verify**).
- ✅ **Partially resolved (Phase 5):** skin-depth vs frequency for Cu/Al/SS
  computed (`figures/ch06_skin_depth.png`, `data/skin_depth.json`) and a
  pulsed-DC settling illustration added (`ch06_pulsed_dc_settling.png`).
  *Still needed:* a first-principles eddy-current distortion-vs-distance dataset.
- Add at least one quantitative distortion-vs-distance dataset (digitized from a
  primary source or generated by the Phase-5 eddy-current simulation) to
  `data/` and reference it here.
- Verify whether modern AC systems' "dynamic metal immunity" (vendor patents
  surfaced in research) materially changes the §6.2 conclusion; tag findings.

## Sources cited
- [@franz2014] review (AC vs DC sensitivity). [@jackson1998] sphere
  polarizability, eddy diffusion, image methods. [@birkfellner1998] systematic
  distortion characterization. [@hummel2005] metallic-object assessment.
  [@kindratenko2000] calibration/correction survey.
