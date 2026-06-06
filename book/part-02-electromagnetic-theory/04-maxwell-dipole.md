# Chapter 4 — Maxwell's Equations, Quasistatics & the Magnetic Dipole

> **Status:** DRAFT · **Part II — Electromagnetic Theory**
> Math is written in LaTeX delimited by `$…$` (inline) and `$$…$$` (display).
> Citation keys resolve to [`../../citations/bibliography.json`](../../citations/bibliography.json).

This chapter builds the physical foundation on which every electromagnetic
tracker rests. The central claims of the chapter are: (i) EMT operates in the
**quasi-magnetostatic near-field regime**, where radiation and propagation
delay are negligible; (ii) in that regime each small generator coil is
accurately modeled as a **point magnetic dipole**, whose field falls off as
$1/r^3$; and (iii) the measurable coupling between a generator and a sensor coil
is governed by **mutual inductance**, which encodes both position and
orientation. The $1/r^3$ scaling is *the* defining fact of EMT — it dictates
working volume, dynamic range (Chapter 16), and noise floor (Chapter 15) — so we
derive it carefully and quantify when the dipole approximation breaks down.

---

## 4.1 Maxwell's equations and constitutive relations

In SI units, the macroscopic Maxwell equations are

$$
\nabla\cdot\mathbf{D}=\rho_f,\qquad
\nabla\cdot\mathbf{B}=0,
$$
$$
\nabla\times\mathbf{E}=-\frac{\partial \mathbf{B}}{\partial t},\qquad
\nabla\times\mathbf{H}=\mathbf{J}_f+\frac{\partial \mathbf{D}}{\partial t},
$$

with constitutive relations $\mathbf{D}=\varepsilon\mathbf{E}$,
$\mathbf{B}=\mu\mathbf{H}$, and (in conductors) Ohm's law
$\mathbf{J}_f=\sigma\mathbf{E}$. Here $\mathbf{E}$ is the electric field,
$\mathbf{B}$ the magnetic flux density, $\mathbf{H}$ the magnetic field
intensity, $\mathbf{D}$ the electric displacement, $\rho_f$ and $\mathbf{J}_f$
the free charge and current densities, and $\varepsilon,\mu,\sigma$ the
permittivity, permeability, and conductivity of the medium. The two equations
that matter most for EMT are Ampère's law (with Maxwell's displacement-current
correction) and Faraday's law: the generator coil's current creates $\mathbf{B}$
via Ampère, and the time variation of $\mathbf{B}$ induces the sensor EMF via
Faraday. (Standard electrodynamics; see e.g. Jackson, *Classical
Electrodynamics* — **to add to bibliography**.)

## 4.2 The quasi-magnetostatic (near-field) regime

EMT systems excite their coils at low frequencies — typically $f$ from a few
hundred Hz to a few tens of kHz. The corresponding free-space wavelength is

$$
\lambda=\frac{c}{f}.
$$

For $f=10\,\text{kHz}$, $\lambda=c/f \approx 3\times10^{8}/10^{4}=3\times10^{4}\,\text{m}=30\,\text{km}$.
A tracking working volume is on the order of $r\lesssim 1\,\text{m}$. Hence

$$
\frac{r}{\lambda}\sim\frac{1}{3\times10^{4}}\approx 3\times10^{-5}\ll 1 .
$$

When the source–observer separation is vanishingly small compared with a
wavelength, two simplifications follow:

1. **Retardation is negligible.** The phase delay $kr=2\pi r/\lambda$ is
   $\sim2\times10^{-4}$ rad — utterly negligible — so the field at the sensor
   tracks the source current essentially *instantaneously*. The field is
   *quasi-static*: a static-field solution that merely scales in time with the
   drive current.
2. **The radiation (far) field is negligible** compared with the near field.
   For an oscillating dipole the radiation term scales as $1/r$ and the
   induction/near-field term as $1/r^3$; their ratio is $\sim (kr)^2\sim10^{-8}$
   here. EMT therefore lives entirely in the **near field**, and the relevant
   solution is the **magnetostatic** one (a static current distribution),
   carried slowly in time by the drive waveform.

This is exactly the regime invoked by Raab et al. when they speak of
"quasi-static magnetic-dipole fields" [@raab1979]. It is the reason EMT can use
simple, closed-form dipole models rather than full wave electrodynamics. The
displacement-current term $\partial\mathbf{D}/\partial t$ in Ampère's law is
correspondingly negligible relative to conduction/source currents at these
frequencies and scales, which is what makes the problem *magneto*-static rather
than fully electromagnetic. (conf: high — standard near-field scaling.)

> **Pedagogical aside.** The same near-field, $1/r^3$ physics that makes EMT
> work also makes it *short-range*: doubling the distance attenuates the signal
> by a factor of 8 (≈18 dB). EMT is intrinsically a centimeter-to-meter
> technology; it does not scale to room-spanning volumes the way RF
> time-of-flight does. Keep this in view through the entire book.

## 4.3 The magnetic vector potential of a current loop

Because $\nabla\cdot\mathbf{B}=0$, we may write $\mathbf{B}=\nabla\times\mathbf{A}$.
In magnetostatics (Coulomb gauge $\nabla\cdot\mathbf{A}=0$) the vector potential
of a localized current distribution is

$$
\mathbf{A}(\mathbf{r})=\frac{\mu_0}{4\pi}\int \frac{\mathbf{J}(\mathbf{r}')}{|\mathbf{r}-\mathbf{r}'|}\,d^3r'.
$$

For a current loop of radius $a$ carrying current $I$, expand
$1/|\mathbf{r}-\mathbf{r}'|$ in a multipole series for $r\gg a$. The monopole
term vanishes (no magnetic charge); the leading nonzero term is the **dipole**
term:

$$
\mathbf{A}_{\text{dip}}(\mathbf{r})=\frac{\mu_0}{4\pi}\,\frac{\mathbf{m}\times\hat{\mathbf{r}}}{r^{2}},
$$

where the **magnetic dipole moment** of the loop is

$$
\boxed{\;\mathbf{m}=I\,\mathbf{A}_{\text{area}}=I\,(\pi a^{2})\,\hat{\mathbf{n}}\;}
$$

and, for an $N$-turn coil of cross-sectional area $A$,
$\mathbf{m}=N I A\,\hat{\mathbf{n}}$, with $\hat{\mathbf{n}}$ the coil's normal.
The dipole moment $\mathbf{m}$ (units $\text{A·m}^2$) is the *single most
important design parameter of a generator coil*: it sets the field strength and
hence the available SNR (Chapter 9).

## 4.4 The magnetic dipole field

Taking $\mathbf{B}=\nabla\times\mathbf{A}_{\text{dip}}$ gives the field of a
point magnetic dipole — the workhorse equation of EMT:

$$
\boxed{\;\mathbf{B}(\mathbf{r})=\frac{\mu_0}{4\pi}\,\frac{1}{r^{3}}\Big[\,3(\mathbf{m}\cdot\hat{\mathbf{r}})\,\hat{\mathbf{r}}-\mathbf{m}\,\Big]\;}
\tag{4.1}
$$

In spherical coordinates aligned so that $\mathbf{m}=m\hat{\mathbf{z}}$, the
components are

$$
B_r=\frac{\mu_0 m}{4\pi}\frac{2\cos\theta}{r^{3}},\qquad
B_\theta=\frac{\mu_0 m}{4\pi}\frac{\sin\theta}{r^{3}},\qquad
B_\phi=0 .
$$

The field magnitude is

$$
|\mathbf{B}|=\frac{\mu_0 m}{4\pi r^{3}}\sqrt{3\cos^2\theta+1}.
\tag{4.2}
$$

Three consequences drive everything downstream:

- **$1/r^3$ range law.** Signal falls 60 dB per decade of distance. This single
  fact sets the working-volume/SNR trade and forces large generator moments and
  very low-noise front ends (Parts IV–V).
- **Angular structure carries orientation information.** The factor
  $3(\mathbf{m}\cdot\hat{\mathbf{r}})\hat{\mathbf{r}}-\mathbf{m}$ means the field
  *direction* depends on where you are relative to the dipole axis — this
  angular dependence is what lets a sensor triad recover orientation, not just
  range (Chapter 5, Part VIII).
- **The field on the dipole axis is twice the field on the equator** at equal
  $r$ ($\sqrt{3+1}=2$ vs. $\sqrt{0+1}=1$ in (4.2)), a handy 6 dB sanity check
  for field maps and FEA validation (Chapter 7).

### Derivation note (full curl)
Writing $\mathbf{A}_{\text{dip}}=\frac{\mu_0}{4\pi}\frac{\mathbf{m}\times\mathbf{r}}{r^3}$
and using the identity
$\nabla\times\!\left(\frac{\mathbf{m}\times\mathbf{r}}{r^3}\right)
=\frac{3(\mathbf{m}\cdot\hat{\mathbf{r}})\hat{\mathbf{r}}-\mathbf{m}}{r^3}$
for $r\neq0$ reproduces (4.1). (The delta-function contact term at the origin is
irrelevant for tracking, where source and sensor never coincide.) A complete
step-by-step curl is deferred to Appendix C.

## 4.5 Field of a finite circular loop (on- and off-axis)

The dipole expression (4.1) is an approximation valid for $r\gg a$. The exact
on-axis field of a single circular loop of radius $a$ at axial distance $z$ is
elementary (Biot–Savart):

$$
B_z(0,0,z)=\frac{\mu_0 I a^{2}}{2\,(a^{2}+z^{2})^{3/2}}
\;\xrightarrow{\,z\gg a\,}\;
\frac{\mu_0 I a^{2}}{2 z^{3}}=\frac{\mu_0\,m}{2\pi z^{3}},
\tag{4.3}
$$

which agrees with the on-axis ($\theta=0$) dipole result
$B_r=\mu_0 m/(2\pi r^3)$ from (4.2) — a reassuring consistency check. Off-axis,
the exact loop field requires **complete elliptic integrals** $K(k)$ and
$E(k)$:

$$
B_\rho=\frac{\mu_0 I}{2\pi}\frac{z}{\rho\sqrt{(a+\rho)^2+z^2}}\!\left[-K(k)+\frac{a^2+\rho^2+z^2}{(a-\rho)^2+z^2}E(k)\right],
$$
$$
B_z=\frac{\mu_0 I}{2\pi}\frac{1}{\sqrt{(a+\rho)^2+z^2}}\!\left[K(k)+\frac{a^2-\rho^2-z^2}{(a-\rho)^2+z^2}E(k)\right],
$$
$$
k^2=\frac{4a\rho}{(a+\rho)^2+z^2}.
$$

These are the reference expressions used to (a) validate the dipole
approximation near the generator, and (b) build accurate forward models for
*physically large* field generators where the dipole model is insufficient
close in. A numerical comparison of (4.1) vs. the elliptic-integral field is one
of the planned simulations (Phase 5; `simulations/`).

## 4.6 Dipole-approximation error vs. distance and size

The fractional error of the dipole model relative to the exact loop field scales
with $(a/r)^2$ for the leading correction (the next multipole, the
"octupole"-type term, is the first nonzero correction for a symmetric loop). The
table below gives the **computed** error — maximum over polar angle
$\theta\in[0,90°]$ — from the finite-loop vs. dipole simulation
(`simulations/run_all.py`, data in `data/dipole_vs_loop_error.csv`):

| $r/a$ | max error over $\theta$ [%] | mean error [%] | Design implication |
|------:|----------------------------:|---------------:|--------------------|
| 1.5   | 73.6                        | 40.9           | dipole model invalid; use exact/elliptic or FEA |
| 2     | 39.8                        | 22.6           | dipole model unsafe; exact/elliptic or FEA |
| 3     | 17.1                        | 9.9            | usable only with calibrated residual |
| 5     | 6.1                         | 3.5            | acceptable for coarse work; calibrate residual |
| 7     | 3.1                         | 1.8            | good for most work |
| 10    | 1.5                         | 0.88           | dipole model generally adequate |
| 15    | 0.67                        | 0.39           | dipole model very good |
| 20    | 0.38                        | 0.22           | dipole model excellent |

(conf: high — computed numerically; the log–log slope confirms the $(a/r)^2$
scaling. See `figures/ch04_dipole_vs_loop_error.png`.) Note the error is
**worst near the dipole axis** (the $\theta$-max column exceeds the mean by
~1.7×). The lesson for Chapter 9:
**small generator coils** validate the point-dipole model over a larger fraction
of the working volume, but **large moments** (which favor SNR) push toward
physically large coils — a direct tension resolved by either keeping the sensor
beyond $\sim$5–10 coil radii or by using a calibrated non-dipole forward model.

## 4.7 Worked example — field-magnitude budget for a benchtop volume

**Goal:** estimate the flux density a sensor sees at the edge of a 0.5 m working
volume, to feed the noise budget of Chapter 16.

Assume a generator coil with moment $m = 1\,\text{A·m}^2$ (e.g.
$N=100$ turns, area $A=10^{-3}\,\text{m}^2$, current $I=10\,\text{A}$ — note
$m=NIA=100\cdot10\cdot10^{-3}=1$). Take the worst-case (equatorial) point at
$r=0.5\,\text{m}$, $\theta=90^\circ$, where (4.2) gives the minimum field:

$$
|\mathbf{B}|=\frac{\mu_0 m}{4\pi r^{3}}
=\frac{(4\pi\times10^{-7})(1)}{4\pi (0.5)^3}
=\frac{10^{-7}}{0.125}
=8.0\times10^{-7}\,\text{T}=0.80\,\mu\text{T}.
$$

For comparison the Earth's static field is $\sim 50\,\mu\text{T}$, so the
*signal* here is ~60× *below* the geomagnetic field — which is exactly why EMT
relies on **time-varying excitation and synchronous (lock-in) detection** to
reject DC and out-of-band interference (Part VII, Chapter 20), rather than
trying to measure absolute field. The induced sensor EMF follows from
$\varepsilon=-N_s A_s\,\omega\,|\mathbf{B}|$ for a sensor of $N_s$ turns and area
$A_s$ at angular drive frequency $\omega=2\pi f$; this connects (4.2) to the
front-end noise budget and is carried forward in Chapter 5 (mutual inductance)
and Chapter 16 (AFE). (conf: high — direct application of (4.2) and Faraday's
law; the geomagnetic comparison uses the standard $\sim25$–$65\,\mu\text{T}$
range.)

> **Takeaway.** The combination of (i) microtesla-and-below signal levels,
> (ii) $1/r^3$ range law, and (iii) a much larger static background field is the
> quantitative core of every EMT design problem. Everything in Parts IV–VIII is,
> in one way or another, a response to these three numbers.

---

## Open questions / to verify
- Add Jackson and/or Griffiths (electrodynamics) to the bibliography with
  verified ISBNs to formally back §4.1–4.4.
- ✅ **Resolved (Phase 5):** §4.6 error table now holds computed values from
  `simulations/run_all.py` (`data/dipole_vs_loop_error.csv`,
  `figures/ch04_dipole_vs_loop_error.png`); the $(a/r)^2$ slope is confirmed.
  Field streamlines: `figures/ch04_dipole_field.png`.
- Confirm the exact next-order multipole correction coefficient for a circular
  loop for inclusion in Appendix C.

## Sources cited in this chapter
- [@raab1979] Raab et al. (1979) — quasi-static magnetic-dipole framing.
- (Electrodynamics textbook citations — Jackson / Griffiths — **to be added**.)
