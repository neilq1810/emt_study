# Chapter 6 — Distortion Physics: Conductors, Ferromagnetics & Eddy Currents

> **Status:** DRAFT · **Part II — Electromagnetic Theory**
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

When the conductor is thick compared with $\delta$, the field is excluded from
its interior and the eddy-current response saturates and develops a characteristic
phase lag; when it is thin compared with $\delta$, the response is volumetric and
grows with thickness. Skin depth thus sets *which* nearby metal matters at a
given frequency and *how* its distortion scales — a key input to the EMC and
mechanical-integration choices of Part V and Chapter 9. (conf: high — (6.1) is
the standard skin-depth result.)

## 6.3 Ferromagnetic materials

A material with relative permeability $\mu_r\gg1$ provides a low-reluctance path
that **concentrates and reshapes** magnetic flux. Unlike eddy currents, this
effect is present in the **static** limit (it is a magnetostatic boundary-value
problem, not an induction problem), so it distorts pulsed-DC systems just as it
does AC systems. Ferromagnets additionally exhibit **hysteresis** and
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

The settling time is set by the longest L/R constant among nearby conductors;
choosing the sample instant is an explicit design parameter trading update rate
against residual eddy distortion. (conf: high — this mechanism is the standard
explanation for pulsed-DC immunity and is consistent with the review
literature [@franz2014].)

## 6.5 Field-perturbation theory and image models

For quantitative modeling, two complementary tools:

1. **Perturbation expansion.** Treat $\mathbf{B}_\text{eddy}$ as a small
   correction $\mathbf{B}=\mathbf{B}_0+\mathbf{B}_1+\dots$, where
   $\mathbf{B}_1$ is the field of the lowest induced multipole of the conductor.
   For a compact conductor far from both coils, the conductor acts as an
   **induced dipole** $\mathbf{m}_\text{ind}\propto\alpha\,\mathbf{B}_0(\text{at
   conductor})$ with a complex, frequency-dependent polarizability $\alpha$. The
   distortion at the sensor is then a *second* $1/r^3$ dipole field added to the
   primary — which means distortion, like signal, falls off steeply with
   distance from the offending object.
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

- distortion **decays rapidly with distance** from the offending object
  (consistent with the induced-dipole $1/r^3$ argument of §6.5);
- distortion **increases with object size and conductivity** (more eddy current)
  and dramatically with **ferromagnetic content**;
- AC systems show **frequency-dependent** conductive distortion; pulsed-DC
  systems show little conductive but full ferromagnetic distortion
  [@franz2014; @birkfellner1998].

> **Engineering takeaway.** Distortion is *not* random noise — it is a smooth,
> repeatable, spatially structured field error. That repeatability is exactly
> what makes **calibration / field-mapping** (Ch. 26–27) viable for *static*
> distorters, and what makes *moving* distorters (a steel instrument advancing
> in the field) the genuinely hard, open problem (witness-sensor and ML
> approaches, Ch. 27 and Part XIII). The survey of calibration techniques by
> Kindratenko [@kindratenko2000] catalogs the static-correction toolbox.

---

## Open questions / to verify
- Add a quantitative induced-dipole polarizability $\alpha(\omega)$ derivation
  (sphere in uniform AC field) to Appendix C, with the standard closed form.
- Re-confirm Birkfellner (1998) DOI/pages against the Wiley *Medical Physics*
  record (currently 25(11):2242–2248, DOI 10.1118/1.598425 — **to verify**).
- Add at least one quantitative distortion-vs-distance dataset (digitized from a
  primary source or generated by the Phase-5 eddy-current simulation) to
  `data/` and reference it here.
- Verify whether modern AC systems' "dynamic metal immunity" (vendor patents
  surfaced in research) materially changes the §6.2 conclusion; tag findings.

## Sources cited
- [@franz2014] review (AC vs DC sensitivity). [@birkfellner1998] systematic
  distortion characterization. [@hummel2005] metallic-object assessment.
  [@kindratenko2000] calibration/correction survey.
