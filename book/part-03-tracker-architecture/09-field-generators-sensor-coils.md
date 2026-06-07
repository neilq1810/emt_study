# Chapter 9 — Field Generators & Sensor Coils

> **Status:** DEEPENED (awaiting review) · **Part III — Tracker Architecture**
> Builds on Ch. 4–8. Hands off to Part IV (sensor engineering) and Ch. 16–18
> (AFE/ADC). Citation keys resolve to
> [`../../citations/bibliography.json`](../../citations/bibliography.json).

The field generator and the sensor are the two physical ends of the signal
chain (Ch. 8). This chapter covers their *architecture-level* design — coil
geometries, drive electronics, field shaping, and the mapping from coil
arrangement to degrees of freedom — leaving detailed sensor construction
(wire-wound vs. PCB vs. **TMR/MR** solid-state) to Part IV and the analog
electronics to Part V. The unifying constraint, inherited from Ch. 4, is the
$1/r^3$ range law: every generator-design decision is ultimately a fight to put
enough signal at the far edge of the working volume.

---

## 9.1 The generator's job: moment, geometry, and working volume

From Ch. 4–5, the sensed signal scales with the generator's magnetic moment
$m_t = N_t I_t A_t$ and falls as $1/r^3$. The generator designer has three
knobs:

- **Turns $N_t$** — raises moment but also raises inductance (slower current
  slew, higher drive voltage) and resistance (heat, noise).
- **Current $I_t$** — raises moment linearly; limited by drive electronics,
  heating, and (in medical contexts) patient-safety field limits.
- **Area $A_t$ / geometry** — raises moment but, per Ch. 4 §4.6, a physically
  large coil makes the convenient point-dipole model invalid close in, forcing
  a higher-fidelity forward model (Ch. 7).

These trade against each other and against the **working volume**: a larger
volume needs more moment (to overcome $1/r^3$ at greater $r$), which pushes
toward larger coils and/or **ferromagnetic cores** (high-$\mu_r$ cores multiply
moment for given $N I$) — at the cost of the core nonlinearity and modeling
burden discussed in Ch. 7 §7.2.

### The coil as an electrical load
The three "knobs" are not free: a generator coil is an inductor, and the moment
$m_t=N_tI_tA_t$ is bought against electrical reality. For a coil of inductance
$L$, winding resistance $R$, driven at $\omega$ to carry current $I_t$:

$$
V_\text{drive} = I_t\,\big|R + j\omega L\big| = I_t\sqrt{R^2 + (\omega L)^2},
\qquad
P_\text{diss} = I_t^2 R .
\tag{9.1}
$$

At EMT frequencies an air coil of any size is **strongly inductive**
($\omega L \gg R$), so the drive voltage is dominated by the reactive term
$I_t\omega L$ — which can reach hundreds of volts for a high-moment coil
(§9.4). The dissipation $P_\text{diss}=I_t^2R$ is pure heat in the winding, the
root cause of the **thermal drift** that degrades calibration (Ch. 15 §15.5,
Ch. 25). Estimating $L$ and $R$ from the geometry uses the standard
inductance formulas — e.g. for a multi-turn loop of radius $a$ and wire radius
$r_w$, $L\approx\mu_0 N^2 a\,[\ln(8a/r_w)-2]$, and $R=\rho\,(N\,2\pi a)/A_\text{wire}$
[@grover1946]. These two numbers, with (9.1), set the power amplifier
specification (Part V) and feed the resonant-drive decision (§9.4).

## 9.2 Generator coil arrangements

The canonical 6-DOF generator is the **orthogonal triad**: three mutually
perpendicular coils sharing a common center, producing three linearly
independent dipole fields whose superposition the sensor decodes (Ch. 5
§5.4–5.6). Variations seen across the field:

- **Co-located orthogonal triad** (the Raab et al. template [@raab1979]):
  compact, the cleanest mapping to the $3\times3$ coupling matrix.
- **Planar / distributed coil sets** ("field generator" boards): multiple coils
  arranged on a plane to shape a usable volume *above* the board — the medical
  form factor (a flat generator placed under the patient table). The fields are
  no longer simple co-located dipoles, so the forward model is calibrated/mapped
  (Ch. 7 Tier 3/4).
- **Transmitter arrays of uniaxial coils**, activated in subsets to balance
  accuracy against computation, as demonstrated by Plotkin & Paperno
  [@plotkin2003].
- **Rotating-field generators**: two-axis excitation producing a rotating
  quasi-static field decoded by phase/amplitude [@paperno2001] — an alternative
  to amplitude-only triad decoding.

## 9.3 Field shaping and uniformity

A perfectly uniform field carries *no position information* (zero gradient →
unobservable position, Ch. 5 §5.7); a wildly nonuniform field is hard to model
and has dynamic-range extremes. Good generator design seeks a field with
**strong, smoothly varying gradients** across the working volume — enough
spatial structure for observability, smooth enough to model and calibrate. This
is why naive Helmholtz-style uniformity is *not* the goal in EMT (unlike many
other magnetics applications); EMT *wants* a structured field. Field shaping is
achieved through coil geometry, relative placement, and (in distributed
generators) the relative drive amplitudes/phases of multiple coils.

**Designing the shape with spherical harmonics.** The field-shaping problem has a
clean formulation via the solid-harmonic representation of Ch. 7 §7.2: each
generator coil contributes a known set of harmonic coefficients
$\{a_{lm}^{(c)}\}$, and the *total* field over the volume is the linear
combination $\sum_c I_c\,a_{lm}^{(c)}$ weighted by the per-coil currents. The
designer therefore *synthesizes* a desired field structure by solving a linear
system for the coil currents/placements — choosing strong, smoothly varying
gradients (good observability/low PDOP, Ch. 24) while keeping the high-order
$a_{lm}$ small (so the dipole/low-order model stays accurate and the dynamic
range stays bounded). This turns "field shaping" from art into a tractable linear
design, and the same harmonics become the fast online forward model the solver
uses (Ch. 7).

## 9.4 Drive electronics (brief; full treatment in Part V)

- **AC generators** require stable sinusoidal current sources — typically a DDS
  (direct digital synthesis) reference into a power amplifier driving the coil
  (an inductive, often resonant, load). Frequency stability and phase noise of
  the reference directly set the synchronous-detection performance downstream
  (Ch. 10, Ch. 20).
- **Pulsed-DC generators** require clean current *steps* with controlled
  settling, plus the timing to define the post-step sample instant after
  eddy-current decay (Ch. 6 §6.4).
- **Resonant drive.** Tuning the coil with a series capacitor $C=1/(\omega^2 L)$
  cancels the inductive reactance, so the power amplifier sees only the winding
  resistance $R$ — collapsing the drive voltage from $I_t\omega L$ to $I_tR$ while
  the reactive energy circulates in the tank. The current (hence moment) is
  boosted by the quality factor $Q=\omega L/R$ for given amplifier capability, at
  the cost of bandwidth $\mathrm{BW}=f_0/Q$ and temperature-sensitive tuning.

### Worked example — coil design & the resonant-drive trade
Target $m_t=1\,\text{A·m}^2$ with $N=100$ turns and area $A=10^{-3}\,\text{m}^2$
(loop radius $a=1.8\,\text{cm}$) → required current $I_t=m_t/(NA)=10\,\text{A}$.
From the §9.1 formulas (wire radius $r_w\approx0.5$ mm):
$L\approx0.8\,\text{mH}$, $R\approx0.24\,\Omega$. At $f=10\,\text{kHz}$,
$\omega L\approx50\,\Omega$ — so the coil is **~210×** more reactive than
resistive ($Q=\omega L/R\approx210$).

| Drive mode | Amplifier voltage (eq. 9.1) | Amplifier sees | Coil power |
|---|---|---|---|
| **Non-resonant** | $I_t\,\omega L \approx \mathbf{500\ V}$ | $|R+j\omega L|=50\,\Omega$ | $I_t^2R=24\,\text{W}$ |
| **Resonant** ($C\approx0.32\,\mu\text{F}$) | $I_t R \approx \mathbf{2.4\ V}$ | $R=0.24\,\Omega$ | $I_t^2R=24\,\text{W}$ |

Resonance cuts the required amplifier voltage from an impractical ~500 V to
2.4 V (the 500 V now appears only *across the tank* $L$ and $C$, handled by
passives) — which is why **AC generators are almost always resonant**. The price
is bandwidth: $\mathrm{BW}=f_0/Q\approx10\,\text{kHz}/210\approx 48\,\text{Hz}$.
That narrow band has two consequences: the excitation frequency must be very
stable and the tank temperature-compensated; and each coil is effectively a
band-pass tuned to *its own* frequency — which is exactly why **planar FDM
generators give each coil a distinct resonant frequency** (the Anser 8-coil
design [@jaeger2017]) rather than sharing one. The heat ($24\,\text{W}$ in a
small coil) is the same in both modes and drives the thermal-stability problem of
Ch. 15. (conf: high — direct from (9.1) and the resonant-circuit relations;
inductance from [@grover1946].)

## 9.5 Sensor coils — the receive end (overview)

The sensor converts the local field into a measurable signal. Two families
(developed in Part IV, now explicitly including solid-state field sensors):

- **Induction pickup coils** — EMF $\propto N_s A_s\,\omega\,B$ (Ch. 5, eq. 5.2).
  Simple, passive, but sensitivity collapses as $\omega\to0$, so they suit
  *AC* architectures. Sensitivity scales with the **area-turns** $N_sA_s$, but
  more turns raise the inductance and the parasitic self-capacitance, lowering the
  **self-resonant frequency** $f_0=1/(2\pi\sqrt{L_sC_s})$ — which must stay safely
  above the excitation band, or the coil's response becomes peaked,
  temperature-sensitive, and hard to calibrate (Ch. 15 §15.3, Ch. 16 §16.3).
  Miniaturization trades area $A_s$ (and thus signal) against the need to fit
  inside a catheter or needle — the central tension of Ch. 14.
- **Direct field sensors** (fluxgate, Hall, **AMR/GMR/TMR** bridges) — respond
  to $B$ including DC, so they enable *pulsed-DC* and quasi-static
  architectures and chip-scale integration (Ch. 14.3). Their noise floor (1/f
  for MR/TMR) sets resolution rather than the coil/AFE chain.

The DOF a sensor resolves depends on its element count and geometry:

| Sensor | DOF resolved | Why |
|---|---|---|
| Single element (1 coil / 1 axis) | up to **5-DOF** | senses field projection on one axis; cannot resolve rotation *about* that axis (roll ambiguity) |
| Orthogonal triad (3 elements) | **6-DOF** | three projections reconstruct the full local field vector and orientation |

(See Ch. 13 for the geometry and Part VIII for why the single-element case loses
roll.)

## 9.6 The dynamic-range consequence

Because signal $\propto m_t/r^3$, a 10:1 span of working distances produces a
$10^3 = 60\,\text{dB}$ swing in received amplitude — *before* accounting for the
angular factor. The receiver chain (sensor → AFE → ADC) must therefore handle an
enormous dynamic range: strong enough not to clip near the generator, quiet
enough to resolve signal at the far edge against the noise floor of the Ch. 4
§4.7 worked example (sub-µT, well below geomagnetic). This single number — 60 dB
plus margin — sizes the AFE gain ranging and ADC ENOB requirements of Ch. 16 and
Ch. 18, and is one of the hardest constraints in the whole system.

---

## Open questions / to verify
- ✅ **Resolved:** the resonant-drive Q-vs-bandwidth trade is now worked (§9.4):
  ~520 V → 2.4 V amplifier reduction, $Q\approx216$, $\mathrm{BW}\approx46$ Hz,
  explaining per-coil FDM frequencies. Remaining: a Phase-5 notebook computing
  $L,R,Q$ for a few coil geometries.
- Add a field-shaping example (multi-coil planar generator) with a simulated
  field map (Phase 5) and the resulting observability/PDOP map (Ch. 24), via the
  §9.3 spherical-harmonic synthesis.
- Source representative generator moments / drive currents / working-volume
  sizes for named commercial generators (Ch. 28), with conditions.

## Sources cited
- [@raab1979] orthogonal-triad template. [@grover1946] coil inductance/resistance
  formulas. [@jaeger2017] planar FDM 8-coil generator (per-coil resonance).
  [@plotkin2003] transmitter arrays. [@paperno2001] rotating-field generators.
  (Sensor families → Part IV; drive electronics → Part V.)
