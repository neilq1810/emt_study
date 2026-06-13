# Chapter 27 — Distortion Compensation

> **Status:** DEEPENED (awaiting review) · **Part X — Calibration**
> Closes Part X. The remedy for the *environmental* distortion terms of Ch. 25
> §25.4 / Ch. 6, where static calibration (Ch. 26) is insufficient. Citation keys
> resolve to [`../../citations/bibliography.json`](../../citations/bibliography.json).

Field distortion (Ch. 6) is the dominant environmental error (Ch. 25 §25.4):
ferromagnetic and conductive objects in the working volume can produce
centimetre-scale position errors and large orientation errors
[@poulin2002; @birkfellner1998]. Static field-mapping (Ch. 26 §26.4) corrects
distortion that is *fixed in the installation*, but the hard, often-unsolved
problem is **distortion from objects that move** — an advancing steel instrument,
a repositioned ultrasound probe, a swinging fluoroscopy C-arm. This chapter
covers the compensation toolbox, from static maps through **witness-sensor** and
**fusion-based** methods to **machine learning**, and is honest about what each
can and cannot do. It also quantifies the one **architectural** lever that rejects
conductive distortion *at the source* — pulsed-DC excitation (§27.6) — and the
**transmitter-side** dual of the witness sensor, in which the generator itself
senses distortion through its own drive impedance (§27.7).

---

## 27.1 The static vs. dynamic distinction

| Distorter | Example | Best tool | Residual |
|---|---|---|---|
| **Static, in installation** | OR table, fixed metal | field map / LUT (Ch. 26) | small, calibratable |
| **Static, but variable placement** | US probe parked at a spot | parameterized model keyed to its pose | moderate |
| **Dynamic / moving** | advancing instrument, C-arm | witness sensor, fusion, online estimation | the hard case |

The key realization: distortion is **smooth, repeatable, and spatially
structured** (Ch. 6 §6.6) — *for a fixed distorter geometry*. That repeatability
is what makes the static case tractable and what the dynamic methods try to
exploit by *parameterizing* the distortion by the offending object's state.

## 27.2 Static field-distortion correction

The baseline: build a correction over the volume *with the distorters present and
fixed* (Ch. 26 §26.4), using interpolation/LUT, polynomials, shape functions, or
ML fits [@kindratenko2000; @kindratenko2005]. This folds the installation's static
distortion into the same map that corrects generator/sensor imperfections. Its
fatal limitation: it is only valid while the environment is **identical** to the
mapped state — move a metal tray and the map is wrong.

## 27.3 Witness / reference-sensor methods

The most promising approach to *dynamic* distortion uses **witness sensors** —
extra field sensors at *known* fixed positions that observe how the field deviates
from its undistorted (calibrated) value:

- A witness at a known pose should read a *known* field; any deviation is a direct
  **measurement of the local distortion**, which can be used to detect, localize,
  and compensate.
- Cavaliere & Cantillon-Murphy demonstrate a **pre-trained witness-sensor
  distortion model**: the field variation at a witness position is used to *localize
  the distorting object* and apply the matching compensation **without attaching
  any sensor to the distorter** [@cavaliere2023]. In their experiments a
  fluoroscopy **C-arm** caused centimetre-scale errors that were reduced to
  **1.52 mm RMS** after compensation, and an ultrasound probe was tracked with
  millimetric accuracy via its distortion signature [@cavaliere2023]. (conf: high
  — reported result; generalization to other distorters/geometries is the open
  question the authors themselves frame.)

**The physics behind it.** A witness at known pose reads
$\mathbf B_\text{meas}-\mathbf B_\text{expected}=\mathbf B_\text{distortion}$
directly. Because a compact distorter acts as an **induced dipole**
$\mathbf m_\text{ind}$ (Ch. 6 §6.3/6.5), a few witnesses sample enough of that
dipole's field to estimate $\mathbf m_\text{ind}$ *and* its location, from which
the perturbation at the *sensor* can be predicted and subtracted — the model
[@cavaliere2023] inverts. Witness **placement** is governed by the same scaling
law that governs the error itself (Ch. 6 eq. 6.4, distortion $\propto
a^3 r^3/d_t^3 d_s^3$): a witness must be *close enough to the distorter to feel a
comparable perturbation* yet *outside the working volume* so it does not corrupt
tracking.

**A unifying view.** Witness-sensor compensation is the spatial analogue of the
**adaptive noise cancellation** of Ch. 20 §20.7: the witness is a *reference
input* that observes the disturbance (not the signal), and the corrector subtracts
the learned mapping from reference to corruption — exactly Widrow's LMS canceller
[@widrow1975]. §20.7 cancels a temporal interferer; §27.3 cancels a spatial
distorter; both fail the same way — if the reference is contaminated by the signal
(a witness *inside* the volume sensing the tracking field), the canceller erodes
the signal. Seeing them as one idea clarifies both.

Witness methods turn distortion from a pure nuisance into an *observable* — a
powerful inversion of the problem, and a bridge to the fusion methods below.

## 27.4 Redundancy and fusion-based detection

If you cannot model the distortion, you can at least **detect** it and stop
trusting corrupted measurements:

- **Redundant EM channels.** Over-determined sensors/transmitters (Ch. 13 §13.3)
  yield a consistency residual; an inconsistent solve flags distortion (large
  solver residual, Ch. 23 §23.6).
- **Cross-modality disagreement.** EM vs. IMU/optical disagreement beyond the
  combined covariance flags distortion in real time, after which the estimator
  down-weights EM (inflates $\mathbf R$) until it passes (Ch. 21 §21.5) — arguably
  the single most practical real-world distortion defense.
- **Innovation gating** in the Kalman filter rejects distortion spikes as outliers
  (Ch. 21 §21.6, Ch. 23 §23.6). Quantitatively, the **normalized innovation
  squared** $\text{NIS}=\boldsymbol\nu^\top\mathbf S^{-1}\boldsymbol\nu$ is
  $\chi^2_m$-distributed for $m$ measurement DOF under nominal conditions; a
  sustained $\text{NIS}$ above its 95–99% threshold (e.g. $\chi^2_{9,0.99}\approx
  21.7$ for a 9-channel coupling vector) is a statistically principled
  **distortion alarm** — not a hand-tuned threshold. This is the same test used
  for filter consistency (Ch. 21 §21.8), now read as a detector.

Detection-plus-flagging is weaker than correction but far more robust: it converts
a *silent* error (dangerous) into a *known* loss of accuracy (manageable, and
required for the "essential performance" posture of Ch. 17 §17.3 / Ch. 29).

## 27.5 Machine-learning compensation — promise and pitfalls

ML appears throughout modern distortion work: neural-network calibration mapping
raw→true pose [@kindratenko2005], pre-trained distortion models keyed to a
distorter's signature [@cavaliere2023], and online/uncertainty-aware compensation.
Its appeal is fitting the high-dimensional, nonlinear raw→true relationship that
parametric models struggle with, jointly over position and orientation
[@kindratenko2005].

**The pitfalls are serious and must be stated** (conf: high — standard ML caveats,
acutely relevant to a safety-critical medical context):

- **Distribution shift.** A model trained on one room/distorter set can fail
  silently when the environment differs from training — exactly the dynamic case
  it is meant to solve. Generalization must be *demonstrated*, not assumed.
- **Train/test contamination.** Evaluating on data drawn from the calibration set
  overstates accuracy (Ch. 26 §26.5). Hold-out and independent-modality validation
  are mandatory.
- **Opaque failure.** Unlike a polynomial whose extrapolation is predictable, an NN
  can produce confident, wrong outputs out of distribution. Pair ML with
  **uncertainty estimates** and the detection/flagging of §27.4 so failures are
  caught.
- **Data cost.** Training needs large, accurately ground-truthed datasets across
  realistic distortion conditions — expensive to collect (Ch. 26 §26.4).

ML is a powerful *complement* to physics-based models and witness/fusion methods,
not a replacement — and in a medical device it must be wrapped in detection,
uncertainty, and validation, never trusted blindly. The principled way to get that
complement — **physics-informed / differentiable-field models that learn only the
residual and preserve the covariance** — is developed as a frontier in Ch. 30 §30.6.

## 27.6 Architectural rejection at the source: pulsed-DC, quantified

Every method above *corrects* distortion after it has entered the measurement.
There is a complementary move that *rejects* it at the source before it is ever
sampled: **pulsed-DC excitation** (Ch. 6 §6.4). It belongs in this chapter because,
for the *conductive* mechanism, it is the single most powerful distortion lever
available — and unlike the post-hoc methods, its improvement is **exponential and
designable**.

**The mechanism, as a suppression factor.** A pulsed-DC axis energizes with a
current *step* and holds it. The step induces a transient eddy current in any
nearby conductor that then decays with the slowest diffusion mode (Ch. 6 eq. 6.3),
$\tau_e=\mu_0\sigma a^2/\pi^2$. If the system **waits** a settling time $t_s$ after
the step and samples only then, the residual eddy distortion relative to its
initial (step-instant) magnitude — which is comparable to the full steady-state
eddy distortion an *AC* system of similar drive would suffer — is suppressed by

$$
S \;=\; \frac{\text{conductive distortion, AC}}{\text{conductive distortion, pulsed-DC at }t_s}\;\approx\; e^{\,t_s/\tau_e}.
\tag{27.1}
$$

The exponent $t_s/\tau_e$ is a pure design choice; the $O(1)$ prefactor relating
the step transient's initial amplitude to the AC steady-state amplitude is
geometry/frequency-dependent and is folded into the residual calibration below.
Equation (27.1) is the quantitative content of the qualitative claim that
"pulsed-DC is immune to conductive distortion" — it is not immune, it is
*exponentially suppressed*, and you choose the suppression by choosing how long
to wait.

**Worked numbers (the dominant 5 cm copper distorter of Ch. 6, $\tau_e=18$ ms).**
Take a representative **1.5 %** raw AC eddy-distortion fraction (the order of the
raw distortion in the Ch. 25 §25.7 worked budget) and read off the pulsed-DC
residual and its rate cost:

| Wait $t_s$ | Suppression $S=e^{t_s/\tau_e}$ | 1.5 % AC eddy → residual | Update rate $\sim 1/t_s$ |
|---|---:|---:|---:|
| $3\tau_e$ = 54 ms | ~20× | 0.075 % | ~18 Hz |
| $5\tau_e$ = 90 ms | ~150× | 0.010 % | ~11 Hz |
| $7\tau_e$ = 126 ms | ~1100× | 0.0014 % | ~8 Hz |

A same-conductor **AC** system at 10 kHz pays the full 1.5 % but updates at
hundreds of Hz with no settling wait. So pulsed-DC **trades ~10× update rate for
~150× conductive-distortion suppression** — an *exponential* rejection bought with
a *linear* rate cost. That trade is extraordinarily favorable whenever conductive
clutter dominates and the target is slow (the rate ceiling is set by the largest,
most conductive object, Ch. 6 eq. 6.3, since $\tau_e\propto a^2\sigma$).

**The asymmetry — Amdahl's law for distortion.** Pulsed-DC does **nothing** for
ferromagnetic distortion: the induced *permeable* dipole (Ch. 6 eq. 6.2) has no
$\omega$-dependence and no transient to decay, so its suppression is **0 dB** at
any $t_s$. The bottom line is therefore set by whatever pulsed-DC cannot touch.
If an environmental budget is, say, **0.5 % conductive ⊕ 0.5 % ferromagnetic**
(RSS 0.71 %), then $5\tau_e$ pulsed-DC crushes the conductive term to ~0.003 % but
leaves the 0.5 % ferromagnetic untouched — total **0.50 %**, an overall
improvement of only **1.4×** despite the **150×** on the conductive part. Pulsed-DC
pays off *only in proportion to the conductive share* of the budget; quote its
benefit against the *total* environmental term, never against the conductive part
alone.

**How it stacks with the compensation toolbox.** Pulsed-DC and the §27.2–27.5
methods are complementary along every axis:

| | Pulsed-DC rejection | Post-hoc compensation (§27.2–27.5) |
|---|---|---|
| Acts | at the source, before sampling | after, on the measurement |
| Mechanism covered | conductive only | conductive **and** ferromagnetic |
| Improvement | exponential in $t_s/\tau_e$ (100–1000×) | ~5–10× (§27.7) |
| Cost | update rate (settling) + a DC-capable sensor | model/witness noise, latency, data |
| Sensor | fluxgate/MR magnetometer (Ch. 14.3) | any, incl. AC pickup coil |

The strong design **layers them**: pulsed-DC to exponentially crush the conductive
term, then witness/fusion/ML (§27.3–27.5) on the *ferromagnetic* residual, with
detect-and-flag (§27.4) underneath. Moreover the residual eddy bias sampled at
$t_s$ is **deterministic and repeatable** (a fixed conductor gives a fixed
$e^{-t_s/\tau_e}$ offset), so it is itself **calibratable** by the static map of
§27.2 — pulsed-DC and field-mapping compound.

**The cost is a budget transfer, not a free lunch.** Pulsed-DC moves error *out*
of the environmental column but *into* two others: the settling wait re-enters the
**latency/rate** budget (Ch. 12), and the DC-capable sensor it requires
(fluxgate/MR, no $\omega$-gain, Ch. 14.3) carries 1/f/bias-reference noise that
re-enters the **stochastic** budget (Ch. 25 §25.2). The honest comparison is
therefore at the level of the *whole* error-and-rate budget (Ch. 31 §31.6), not
the distortion term in isolation: pulsed-DC wins decisively in a conductive-clutter
environment with a slow target, and loses to a high-$\omega$ AC coil where
ferromagnetics dominate or high update rate is essential. (conf: high — eq. (27.1)
follows directly from the eq. 6.3 decay; absolute prefactor and the 1.5 % figure
are illustrative/geometry-dependent.)

## 27.7 Transmitter-side sensing: generator current & impedance monitoring

The witness sensor (§27.3) observes distortion at the **receive** end. Its
**dual** is to observe distortion at the **transmit** end — by watching how a
distorter loads the *generator*. This is the "build intelligence into the
generator" idea, and it is real: a distorter perturbs not only the field at the
sensor but the **drive current, voltage, and phase** of the transmitter itself.

**The physics — reflected impedance (Ch. 5).** A nearby conductor or ferromagnet
is a magnetically coupled secondary circuit, so it reflects an impedance back into
the transmitter coil,
$$
Z_\text{reflected}\ \sim\ \frac{(\omega M)^2}{R_2 + j\omega L_2},
\tag{27.2}
$$
shifting the transmitter's effective inductance and resistance and hence its
drive current/phase. Chapter 5 §5.5 noted that the *sensor's* back-reaction
($\sim k^2$, $k\ll10^{-3}$) is negligible — but a **distorter can be larger and
closer to the transmitter** than the millimetric sensor, so *its* reflected
impedance is measurable. This is precisely the operating principle of **metal
detectors and eddy-current NDT**, turned on the EMT generator.

The reflected signature also **discriminates the mechanism** (Ch. 6):
- **Conductive (eddy):** raises reflected *resistance*, lowers inductance, with a
  quadrature phase set by $\omega\tau_e$ — the conductive-vs-ferrous phase
  discrimination metal detectors exploit.
- **Ferromagnetic:** *raises* inductance, in phase, present even at DC.
- **In pulsed-DC:** the drive-current **decay transient** after the step exposes
  the nearby conductor's $L/R$ directly — a transmitter-side measurement of the
  very $\tau_e$ that sets the §27.6 settling wait (closing an adaptive loop).

**It has been built.** Jaeger & Cantillon-Murphy modify the field-generator array
to **transmit *and* receive**, and invert a **mutual-inductance model** to estimate
a static distorter's **location, magnitude, and material from the generator side
alone** — the transmitter-side dual of the witness sensor, from the same group as
Anser and the witness-sensor work [@jaeger2018]. A complementary, feed-forward
form builds the intelligence into the **drive**: GE's Dumoulin patent
**pre-emphasizes the transmit-coil current waveform** (an ideal current plus a
compensation current defined by exponential amplitude/time-constant terms) so the
*generated field* is pre-corrected for eddy distortion before it reaches the sensor
[@dumoulin2001]. A broader family of vendor eddy-detection/compensation patents
(NDI/GE lineage) works the same seam (conf: med — patents surfaced in search; the
full set is an open-questions item).

**Why it is powerful but bounded (observability).** The transmitter-side
measurement is rich in *what* but poor in *where*:
- A drive impedance is **one complex scalar per coil per frequency**; it
  **integrates every distorter** in the volume into a single lump. Localizing from
  it is ill-posed — multi-coil and multi-frequency (impedance spectroscopy) add
  equations but the inverse stays hard [@jaeger2018].
- Sensitivity is **highest for distorters near the transmitter, lowest for those
  near the sensor** ($d_s\to0$). That is the exact *opposite* of where the error
  is worst — a small steel tool at the sensor tip is catastrophic for the pose
  (Ch. 6 eq. 6.4) yet almost invisible to the generator. The receiver-side witness
  has the complementary sensitivity, which is why the two ends pair so well.
- It is a **fractional impedance change on a coil carrying amps** — a real
  dynamic-range/SNR challenge against the huge primary drive.

**Where it earns its place (the intelligent generator).** Precisely because it is
global-but-coarse, it excels at jobs that do not need localization:
- **Environment-change / self-health monitor** — a measurable impedance shift is a
  cheap, robust "the room changed, re-map or inflate uncertainty" trigger feeding
  **detect-and-flag** (§27.4), even when it cannot correct.
- **Adaptive pulsed-DC** — sense $\tau_e$ from the drive transient and set the
  settling time adaptively (§27.6).
- **Mechanism classification** — conductive vs. ferromagnetic from the reflected
  phase, to choose *which* compensation to apply.
- **Feed-forward pre-emphasis** of the drive to pre-cancel *static* eddy distortion
  [@dumoulin2001].
- **Coarse prior** to a receiver-side witness/fusion estimator — the two ends fuse.
- It **reuses hardware already present**: the ratiometric drive-current monitor
  used to normalize generator drift (Ch. 25 §25.4) is the same sensor, read for a
  second purpose.

**Unifying view.** §27.3 (witness, receive end) and §27.7 (generator, transmit
end) are the **two ends of one observable** — the distortion field made visible by
sampling it where it is created versus where it lands. The strongest systems use
both: transmitter-side for a global *"something changed, and what kind,"*
receiver-side for the local *"how much, at the sensor."* (conf: high for the
reflected-impedance physics and [@jaeger2018; @dumoulin2001]; med for the broader
vendor-patent landscape.)

## 27.8 The limits of compensation

No method fully escapes physics:

- **Ferromagnetic, hysteretic distortion** (Ch. 6 §6.3) is history-dependent and
  hardest to model.
- **Strong, close, fast-moving distorters** can overwhelm any compensation; the
  honest response is detect-and-flag (§27.4), keep distorters away (the clinical
  protocol lesson of [@poulin2002]), or fall back to fused/other modalities.
- **A single-residual flag has a blind spot.** A redundancy/residual flag (§27.4)
  catches only distortion *inconsistent* with the model; distortion that **mimics a 6-DOF
  pose shift** inflates the pose error but not the residual. A Phase-5 pilot (Ch. 33 §33.9,
  `data/distortion_flag_roc.json`) shows the detection margin going **negative** for such a
  distorter — the flag fires *after* the error is dangerous — which is why single-sensor
  detection must be backed by **independent** redundancy (witness §27.3, second generator
  Ch. 9 §9.8, fusion Ch. 21 §21.9), not trusted alone.
- **Compensation reduces, it does not eliminate.** Reported reductions are
  $\sim$5–10×, not to zero: static mapping took a ~1.56% raw distortion to ~0.20%
  residual in the Ch. 25 worked budget (~8×), and witness compensation took a
  C-arm's centimetre-scale error to 1.52 mm RMS [@cavaliere2023]. The **residual**
  is what enters the environmental term of the error budget (Ch. 25 §25.4/§25.7),
  alongside the compensation's own added noise and latency (witness-sensor noise,
  model error, inference time). Compensation is not free, and its residual must be
  budgeted like any other term.

> **Engineering takeaway.** The distortion hierarchy is: **keep distorters out**
> (protocol) → **reject at the source** (pulsed-DC, exponentially, for the
> *conductive* part, §27.6) → **map static distortion** (Ch. 26) → **observe it**
> (witness sensors at the receive end *and* generator-impedance monitoring at the
> transmit end, §27.3/§27.7) → **detect and down-weight it** (fusion/gating) →
> **model it** (physics + ML, with validation and uncertainty). Real systems layer
> several of these — they are complementary, not competing. The one thing never to
> do is silently trust a distorted measurement.

---

## Open questions / to verify
- ✅ **Partially resolved:** the **distortion-field visualizer** and
  **skin-depth/eddy explorer** Phase-6 tools are built (and the distortion viz uses
  the induced-dipole model of §27.3 / Ch. 6 eq. 6.4). Remaining: a *witness-sensor
  compensation* interactive demo, and a Phase-5 sim quantifying residual vs.
  witness count/placement.
- Source quantitative generalization results for witness-sensor and ML
  compensation across *different* rooms/distorters (beyond the original
  demonstrations) to gauge real-world robustness [@cavaliere2023; @kindratenko2005].
- Add the online/uncertainty-aware compensation literature (e.g. spatial-
  uncertainty online error compensation) with verified citations.
- **Transmitter-side sensing (§27.7):** verify and enumerate the vendor
  eddy-detection/compensation patent family (e.g. "metal disturbance detection,"
  US 7,321,228; eddy-current compensation US 7,292,948 / US 7,957,925; multi-
  transmitter distortion compensation US 9,459,124) and any quantitative
  localization/accuracy results for generator-impedance distorter characterisation
  beyond [@jaeger2018]. Tie to the Ch. 6 "dynamic metal immunity" open question.
- A Phase-5 sim of the reflected-impedance signature (eq. 27.2) vs. distorter
  size/distance/material, and a Phase-6 toggle in the distortion dashboard showing
  the transmitter-side observable alongside the receiver-side error.

## Sources cited
- [@cavaliere2023] witness-sensor pre-trained distortion compensation (C-arm
  1.52 mm RMS). [@jaeger2018] transmitter-side distorter characterisation via
  mutual inductance (generator transmits *and* receives) — the dual of §27.3.
  [@dumoulin2001] generator-side transmit-waveform pre-emphasis (US 6,201,987).
  [@widrow1975] adaptive (LMS) reference cancellation — the unifying view of §27.3.
  [@kindratenko2005] neural-network calibration; [@kindratenko2000] correction-
  method survey. [@poulin2002; @birkfellner1998] distortion magnitudes/
  characterization. Fusion/gating from Ch. 21; error re-entry to Ch. 25.
