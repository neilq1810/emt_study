# Chapter 5 — Coil Coupling, Mutual Inductance & Magnetic Moment

> **Status:** DEEPENED (awaiting review) · **Part II — Electromagnetic Theory**
> Builds directly on Chapter 4 (dipole field, eq. 4.1). Citation keys resolve to
> [`../../citations/bibliography.json`](../../citations/bibliography.json).

Chapter 4 gave the field a generator coil produces. This chapter answers the
question a tracker actually measures: *given that field, what voltage appears on
a sensor coil, and how does that voltage encode the sensor's position and
orientation?* The answer is **mutual inductance**, and the central object of the
whole field is the **3×3 coupling matrix** between a transmitter triad and a
sensor triad. Everything in Parts VII–VIII (DSP and solvers) is, mathematically,
the inversion of the relationships built here.

---

## 5.1 Magnetic moment and effective area (recap and refinement)

From Chapter 4, an $N$-turn coil of area $A$ carrying current $I$ has dipole
moment $\mathbf{m}=NIA\,\hat{\mathbf{n}}$. Two refinements matter in practice:

- **Effective area $\neq$ geometric area.** Winding pitch, layering, and the
  finite cross-section of a multilayer coil mean the *effective* magnetic area
  used in the forward model must be calibrated, not assumed (Chapter 15,
  tolerance analysis). We write $\mathbf{m}=N I A_\text{eff}\hat{\mathbf{n}}$.
- **Sensor "moment" by reciprocity.** A receive coil is characterized by the
  same $N_s A_{s,\text{eff}}$ product; reciprocity (§5.5) lets us treat a coil
  identically whether it transmits or receives.
- **Ferrite cores and the demagnetizing limit.** A high-permeability core boosts
  the effective area, but *not* by the bulk $\mu_r$: a finite rod's field is
  limited by its own **demagnetizing factor** $D$ (a geometric constant, small for
  long thin rods). The **apparent permeability** is
  $$
  \mu_\text{app} = \frac{\mu_r}{1 + D\,(\mu_r - 1)} \xrightarrow{\mu_r\to\infty} \frac{1}{D},
  $$
  so for $\mu_r\gg1$ the gain saturates at $\sim1/D$ regardless of the material —
  a long, slender core ($D\sim0.01$) yields $\mu_\text{app}\sim100$, a stubby one
  far less. This is *the* reason catheter sensors are made long and thin
  (Ch. 14.2), and why the moment of a cored coil must be calibrated, not computed
  from $\mu_r$. Practical self/mutual-inductance formulas for real coil geometries
  are tabulated by Grover [@grover1946]. (conf: high — standard magnetostatics.)

## 5.2 Flux linkage and the induced EMF (Faraday)

The flux through a sensor coil of $N_s$ turns and effective area $A_s$ with
normal $\hat{\mathbf{n}}_s$, sitting in flux density $\mathbf{B}$ (assumed
approximately uniform over the small sensor), is

$$
\Phi = N_s\!\int_{A_s}\!\mathbf{B}\cdot d\mathbf{a}\;\approx\;N_s A_s\,(\mathbf{B}\cdot\hat{\mathbf{n}}_s).
$$

By Faraday's law the open-circuit induced EMF is

$$
\varepsilon=-\frac{d\Phi}{dt}=-N_s A_s\,\hat{\mathbf{n}}_s\cdot\frac{d\mathbf{B}}{dt}.
\tag{5.1}
$$

For sinusoidal AC excitation $I(t)=I_0\cos\omega t$, the field is
$\mathbf{B}(t)=\mathbf{B}_0\cos\omega t$ and the EMF amplitude is

$$
|\varepsilon|=N_s A_s\,\omega\,|\mathbf{B}_0\cdot\hat{\mathbf{n}}_s| .
\tag{5.2}
$$

Two design facts fall straight out of (5.2):

1. **Sensitivity rises with frequency** ($\propto\omega$): an AC sensor coil is a
   *differentiator*, so higher drive frequency buys signal — but also worsens
   eddy-current distortion (Chapter 6). This is the fundamental AC frequency
   trade.
2. **The signal is a projection** ($\mathbf{B}_0\cdot\hat{\mathbf{n}}_s$): the
   sensor sees only the component of the field along its own axis. A single coil
   therefore cannot, by itself, resolve all orientation degrees of freedom — the
   origin of the 5-DOF vs. 6-DOF distinction (Chapter 13).

## 5.3 Mutual inductance as the core observable

Combining the dipole field (4.1) with the flux integral, the flux linked into
the sensor is proportional to the transmitter current. The constant of
proportionality is the **mutual inductance** $M$:

$$
\Phi_{s}=M\,I_t,\qquad
\varepsilon_s=-M\frac{dI_t}{dt}.
$$

$M$ depends *only on geometry* — the relative position and orientation of the
two coils — which is precisely why measuring $M$ (via the ratio of sensor EMF to
known transmitter current) yields pose. Using (4.1) for a transmitter of moment
$m_t\hat{\mathbf{n}}_t$ and a sensor of effective area-turns $N_sA_s$ at
displacement $\mathbf{r}$:

$$
M(\mathbf{r},\hat{\mathbf{n}}_t,\hat{\mathbf{n}}_s)
=\frac{\mu_0\, (N_tA_t)(N_sA_s)}{4\pi r^{3}}
\Big[\,3(\hat{\mathbf{n}}_t\!\cdot\hat{\mathbf{r}})(\hat{\mathbf{n}}_s\!\cdot\hat{\mathbf{r}})-(\hat{\mathbf{n}}_t\!\cdot\hat{\mathbf{n}}_s)\Big].
\tag{5.3}
$$

Equation (5.3) is the **forward model** of a single-transmitter/single-sensor
pair. Note its structure: a $1/r^3$ *range* factor multiplying an *angular*
factor in square brackets that couples the two coil orientations through the
line-of-sight direction $\hat{\mathbf{r}}$. Recovering $\mathbf{r}$ and the
orientations from measured $M$ values is the inverse problem of Part VIII.

### Neumann's formula (the rigorous definition)
For arbitrary coil shapes the mutual inductance is the Neumann double line
integral

$$
M=\frac{\mu_0}{4\pi}\oint_{C_t}\oint_{C_s}\frac{d\boldsymbol{\ell}_t\cdot d\boldsymbol{\ell}_s}{|\mathbf{r}_t-\mathbf{r}_s|},
\tag{5.4}
$$

which is manifestly **symmetric in $t\leftrightarrow s$** — the formal statement
of reciprocity (§5.5). Equation (5.3) is the point-dipole limit of (5.4) and
inherits its $r\gg a$ validity bound from Chapter 4, §4.6. (The reduction
(5.4)→(5.3) is: expand $1/|\mathbf r_t-\mathbf r_s|$ to the leading multipole for
$r\gg a$, perform the loop integrals to recover the moments $N_tA_t$, $N_sA_s$,
and the dipole angular factor — the dipole field of Ch. 4 integrated over the
sensor.)

### Coupling coefficient and the *loaded* voltage
Two practical refinements connect the idealized $M$ to what the front end
actually measures:

- **Coupling coefficient.** Normalizing $M$ by the self-inductances,
  $k = M/\sqrt{L_t L_s}$ with $|k|\le1$, expresses how tightly the coils are
  linked. For EMT $k$ is **minuscule** ($k\ll10^{-3}$): the coils are far apart
  relative to their size, so almost no flux links — which is *why* the received
  signal is microvolt-class (Ch. 4 §4.7) and the whole receive chain must be so
  low-noise (Parts IV–VI). It also means the sensor's back-reaction on the
  transmitter (reflected impedance $\sim k^2$) is utterly negligible, so the
  transmitter drive is independent of sensor pose.
- **Open-circuit EMF vs. loaded voltage.** Equation (5.1) is the *open-circuit*
  EMF. The sensor coil ($L_s$, winding resistance $R_s$, self-capacitance) feeds
  the AFE input impedance $Z_\text{in}$, so the measured voltage is the divider
  $$
  v = \varepsilon\,\frac{Z_\text{in}}{Z_\text{in} + R_s + j\omega L_s}.
  $$
  A high-impedance voltage-mode front end ($Z_\text{in}\gg|R_s+j\omega L_s|$)
  recovers $v\approx\varepsilon$; near the coil's self-resonance the denominator
  shapes the response and adds a temperature/phase dependence the calibration must
  absorb (Ch. 15 §15.3, Ch. 16 §16.3). The forward model (5.3) is the *coupling*;
  this divider is the *transduction* — both enter the calibrated channel gain
  (Ch. 11 §11.2).

## 5.4 The 3×3 coupling matrix

Real 6-DOF systems use a transmitter *triad* (three mutually orthogonal coils,
moments along $\hat{\mathbf{x}},\hat{\mathbf{y}},\hat{\mathbf{z}}$) and a sensor
*triad* (coupling geometry: `figures/ch05_coupling_geometry.png`). Each (transmit
axis $i$, sense axis $j$) pair has a mutual inductance
$M_{ij}$, assembled into a matrix

$$
\mathbf{M}(\mathbf{r},\mathbf{R})=\big[M_{ij}\big]_{3\times3},
$$

where $\mathbf{R}\in SO(3)$ is the sensor's orientation relative to the
transmitter frame. Writing the transmitter dipole tensor at the sensor location
as

$$
\mathbf{K}(\mathbf{r})=\frac{\mu_0\,m_t}{4\pi r^3}\big(3\,\hat{\mathbf{r}}\hat{\mathbf{r}}^{\!\top}-\mathbf{I}\big),
\tag{5.5}
$$

(a symmetric, traceless $3\times3$ field-coupling tensor — note $\mathrm{tr}=0$
because $3\,\hat{\mathbf{r}}\!\cdot\!\hat{\mathbf{r}}-3=0$), the full coupling
matrix factorizes as

$$
\boxed{\;\mathbf{M}=(N_sA_s)\,\mathbf{R}^{\!\top}\,\mathbf{K}(\mathbf{r})\;}
\tag{5.6}
$$

(up to per-axis area-turns constants absorbed into a calibration). This
factorization is the conceptual heart of EMT decoding:

- $\mathbf{K}(\mathbf{r})$ carries the **position** information (through
  $\hat{\mathbf{r}}$ and $1/r^3$);
- $\mathbf{R}$ carries the **orientation** information;
- The measured $\mathbf{M}$ is their product, contaminated by noise and
  distortion.

**Two readouts of one coupling — induction vs field sensing.** Equations (5.5)–(5.6)
are about *geometry*; how a sensor turns $\mathbf{M}$ into a signal is a second,
independent choice (Ch. 13–14). An **induction coil** measures the *rate*: by Faraday
(§5.2) its EMF is $\varepsilon_j=-\dot\Phi_j=-\sum_i M_{ij}\dot I_i$, so it reads
$\mathbf{M}$ **scaled by $\omega$**, responds only to a *changing* field (AC, or the
transient of pulsed-DC), and carries the area-turns $N_sA_s$ of (5.6). A **field sensor**
(TMR/GMR/AMR, fluxgate, Hall) instead reads the *field projection itself* — the
$j$-component of $\mathbf{R}^{\!\top}\mathbf{K}\,$ at its location — **directly and down to
DC**, with no factor of $\omega$ and no differentiation; the $N_sA_s$ scale is replaced by
the sensor's field-to-output gain. The **geometry is common to both** ($\mathbf{K}$,
$\mathbf{R}$, the $4{:}1{:}1$ eigenstructure, observability), but the readout differs in
ways that ripple through the book: the coil's $\propto\omega$ sensitivity favours a *higher*
excitation frequency and gives a **passive, offset-free**, and — for an **air core** —
**highly linear, hysteresis-free** element (a soft *ferrite* core trades a little
linearity/hysteresis for sensitivity, kept small by weak-field operation and the
demagnetization-clamped geometry of Ch. 14.2), whereas
the field sensor buys **DC capability and chip-scale miniaturisation** at the cost of a
**1/f noise floor, offset, hysteresis, nonlinearity, and a bias reference** (Ch. 14.3,
16, 25.2–25.3, 37 §37.4). Both ultimately deliver the *same* $\mathbf{M}$ to the solver —
which is why the estimation, calibration, and error machinery (Ch. 23–26) is written in
terms of $\mathbf{M}$, not of EMF.

The eigenstructure of $\mathbf{K}$ is instructive: its eigenvalues are
$\propto\{2,-1,-1\}/r^3$ with the "+2" eigenvector along $\hat{\mathbf{r}}$.
Thus measuring $\mathbf{M}$ and removing $\mathbf{R}$ (e.g. by forming the
rotation-invariant $\mathbf{M}^{\top}\mathbf{M}$) exposes $\hat{\mathbf{r}}$ and
$r$ — the basis of several closed-form initializers used to seed the iterative
solvers of Chapter 23.

## 5.5 Reciprocity and its consequences

Neumann's formula (5.4) is symmetric under exchanging the two contours
($\mathbf r_t\leftrightarrow\mathbf r_s$, $d\boldsymbol\ell_t\leftrightarrow d\boldsymbol\ell_s$),
because the integrand $d\boldsymbol\ell_t\!\cdot\!d\boldsymbol\ell_s/|\mathbf r_t-\mathbf r_s|$
is itself symmetric. Hence $M_{ts}=M_{st}$: **a coil pair couples equally whether
you drive the "transmitter" and listen on the "sensor" or vice versa** (a special
case of the Lorentz reciprocity theorem [@jackson1998]). Consequences for system
design:

- **Architectural freedom.** One may build a *large transmitter / small sensor*
  system (the medical norm: a fixed field generator and a tiny catheter coil) or
  a *small transmitter / large receiver* system; the physics of $M$ is identical.
  The choice is driven by power, safety, and which element must be miniaturized
  (Chapters 8–9), not by the coupling physics.
- **Calibration symmetry.** A coil's transmit and receive characterizations are
  linked, reducing the independent parameters to be calibrated (Chapter 26).

## 5.6 Superposition of multiple transmitters

Because magnetostatics is linear, the fields of multiple transmitter coils
**superpose**. Two distinct ways to exploit this:

- **Separable excitation.** Drive transmitter axes on distinct frequencies
  (FDM), time slots (TDM), or orthogonal codes (CDM) so the receiver can
  attribute each measured component to a known transmitter axis (Chapter 19).
  This is how the individual $M_{ij}$ are disentangled from a single sensor
  voltage.
- **Transmitter arrays.** Large arrays of *uniaxial* transmitters can localize a
  single subminiature sensor, with subsets ("subarrays") activated to trade
  accuracy against computation, as demonstrated by Plotkin & Paperno
  [@plotkin2003]. A related idea uses a *rotating* quasi-static field from
  two-axis excitation, decoding pose from the phase and amplitude of the sensed
  signal relative to the excitation [@paperno2001].

These are not merely academic: the array and rotating-field approaches define
part of the design space surveyed in Part III and the research frontier of
Part XIII.

## 5.7 Field gradients and observability

The angular factor in (5.3) and the tensor $\mathbf{K}$ in (5.5) mean the field
*and its spatial gradient* vary across the working volume. Pose observability —
whether a given measurement set uniquely determines pose, and how sensitively —
is governed by the Jacobian of $\mathbf{M}$ with respect to the pose parameters.
Where the field is locally too uniform (small gradient), position is weakly
observable and the solver is ill-conditioned; this is developed quantitatively
in Chapter 24 (observability/conditioning) and connects to the error budget of
Chapter 25.

---

## Worked micro-example — the 6 dB on-axis/equator coupling ratio
For collinear, coaxial transmitter and sensor on the dipole axis
($\hat{\mathbf{n}}_t=\hat{\mathbf{n}}_s=\hat{\mathbf{r}}$), the bracket in (5.3)
is $3(1)(1)-1=2$. For both transverse on the equator
($\hat{\mathbf{n}}_t=\hat{\mathbf{n}}_s\perp\hat{\mathbf{r}}$), the bracket is
$3(0)(0)-1=-1$. The magnitude ratio is $2{:}1$ (6 dB) at equal range — the same
factor seen in the field magnitude in Chapter 4, now expressed in the
*measured coupling*. This is a quick bench check that a forward-model
implementation is correct. (conf: high — direct from (5.3).)

## Worked numeric example — induced voltage across the volume
Take a generator moment $m_t=1\,\text{A·m}^2$, a sensor with
$N_sA_s=10^{-3}\,\text{m}^2{\cdot}\text{turns}$ (e.g. $N_s=1000$,
$A_s=10^{-6}\,\text{m}^2$), AC at $f=10\,\text{kHz}$ ($\omega=6.28\times10^4$).
Using $|\varepsilon|=N_sA_s\,\omega\,|\mathbf B_0\!\cdot\!\hat{\mathbf n}_s|$
(eq. 5.2) and the Ch. 4 fields:

- **Near, on-axis** ($r=0.3$ m, aligned): $B = \mu_0 m_t/(2\pi r^3) = 7.4\,\mu\text{T}$
  → $\varepsilon = 10^{-3}\cdot6.28\times10^4\cdot7.4\times10^{-6} \approx 0.47\,\text{mV}$.
- **Far edge, equatorial** ($r=0.5$ m): $B = 0.8\,\mu\text{T}$ (Ch. 4 §4.7)
  → $\varepsilon \approx 50\,\mu\text{V}$.

So the signal spans roughly $0.47\,\text{mV}$ down to $50\,\mu\text{V}$ — and far
less at unfavourable orientations — across this small volume, a **~20 dB swing
from range alone** (more once orientation and the full 60 dB working range are
included, Ch. 9 §9.6). Against the $\sim$13 nV-RMS demodulated noise floor of the
Ch. 20 worked example, the far-edge SNR is $\sim50\,\mu\text{V}/13\,\text{nV}\approx
3800$ — comfortably resolvable, and consistent with the sub-mm CRLB of Ch. 24.
This connects the coupling physics here directly to the AFE dynamic-range problem
(Ch. 16 §16.4) and the lock-in budget (Ch. 20 §20.9). (conf: high — eqs. (5.2),
(4.2); a full off-axis $\mathbf M$ is validated to machine precision in the
Phase-5 `sim_closed_form_init`, Ch. 23.)

---

## Open questions / to verify
- ✅ **Resolved:** the (5.4)→(5.3) reduction sketch is now given in §5.3; a worked
  numerical $\mathbf M$ / induced voltage is added above and the full off-axis
  $\mathbf M$ is machine-precision-validated in the Phase-5 closed-form sim
  (Ch. 23). Remaining: move the *full* step-by-step multipole reduction to
  Appendix C.
- Confirm IEEE DOIs for [@paperno2001] and [@plotkin2003] against IEEE Xplore.
- Add a measured/Grover-tabulated self-inductance for a representative catheter
  coil to make the §5.3 coupling-coefficient estimate concrete [@grover1946].

## Sources cited
- [@raab1979] dipole/coupling foundation. [@jackson1998] Neumann formula,
  reciprocity. [@grover1946] practical inductance formulas. [@plotkin2003]
  transmitter arrays. [@paperno2001] rotating-field excitation.
