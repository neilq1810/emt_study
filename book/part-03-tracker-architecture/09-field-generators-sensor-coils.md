# Chapter 9 — Field Generators & Sensor Coils

> **Status:** DRAFT · **Part III — Tracker Architecture**
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

## 9.4 Drive electronics (brief; full treatment in Part V)

- **AC generators** require stable sinusoidal current sources — typically a DDS
  (direct digital synthesis) reference into a power amplifier driving the coil
  (an inductive, often resonant, load). Frequency stability and phase noise of
  the reference directly set the synchronous-detection performance downstream
  (Ch. 10, Ch. 20).
- **Pulsed-DC generators** require clean current *steps* with controlled
  settling, plus the timing to define the post-step sample instant after
  eddy-current decay (Ch. 6 §6.4).
- **Resonant drive.** Tuning the coil with a capacitor to resonate at the drive
  frequency boosts current (and thus moment) for given drive voltage, at the
  cost of bandwidth and tuning sensitivity — a classic Q-vs-bandwidth trade
  revisited in Ch. 16.

## 9.5 Sensor coils — the receive end (overview)

The sensor converts the local field into a measurable signal. Two families
(developed in Part IV, now explicitly including solid-state field sensors):

- **Induction pickup coils** — EMF $\propto N_s A_s\,\omega\,B$ (Ch. 5, eq. 5.2).
  Simple, passive, but sensitivity collapses as $\omega\to0$, so they suit
  *AC* architectures. Miniaturization trades area $A_s$ (and thus signal)
  against the need to fit inside a catheter or needle — the central tension of
  Ch. 14.
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
- Source representative generator moments / drive currents / working-volume
  sizes for named commercial generators (Ch. 28), with conditions, rather than
  asserting numbers.
- Add a field-shaping example (multi-coil planar generator) with a simulated
  field map (Phase 5) and the resulting observability map (Ch. 24).
- Quantify the resonant-drive Q-vs-bandwidth trade with a worked example tied to
  a target update rate (Ch. 12).

## Sources cited
- [@raab1979] orthogonal-triad template. [@plotkin2003] transmitter arrays.
  [@paperno2001] rotating-field generators. (Sensor families → Part IV;
  drive electronics → Part V.)
