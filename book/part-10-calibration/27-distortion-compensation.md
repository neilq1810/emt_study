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
can and cannot do.

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
uncertainty, and validation, never trusted blindly.

## 27.6 The limits of compensation

No method fully escapes physics:

- **Ferromagnetic, hysteretic distortion** (Ch. 6 §6.3) is history-dependent and
  hardest to model.
- **Strong, close, fast-moving distorters** can overwhelm any compensation; the
  honest response is detect-and-flag (§27.4), keep distorters away (the clinical
  protocol lesson of [@poulin2002]), or fall back to fused/other modalities.
- **Compensation reduces, it does not eliminate.** Reported reductions are
  $\sim$5–10×, not to zero: static mapping took a ~1.56% raw distortion to ~0.20%
  residual in the Ch. 25 worked budget (~8×), and witness compensation took a
  C-arm's centimetre-scale error to 1.52 mm RMS [@cavaliere2023]. The **residual**
  is what enters the environmental term of the error budget (Ch. 25 §25.4/§25.7),
  alongside the compensation's own added noise and latency (witness-sensor noise,
  model error, inference time). Compensation is not free, and its residual must be
  budgeted like any other term.

> **Engineering takeaway.** The distortion hierarchy is: **keep distorters out**
> (protocol) → **map static distortion** (Ch. 26) → **observe it** (witness
> sensors) → **detect and down-weight it** (fusion/gating) → **model it** (physics
> + ML, with validation and uncertainty). Real systems layer several of these.
> The one thing never to do is silently trust a distorted measurement.

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

## Sources cited
- [@cavaliere2023] witness-sensor pre-trained distortion compensation (C-arm
  1.52 mm RMS). [@widrow1975] adaptive (LMS) reference cancellation — the unifying
  view of §27.3. [@kindratenko2005] neural-network calibration; [@kindratenko2000]
  correction-method survey. [@poulin2002; @birkfellner1998] distortion magnitudes/
  characterization. Fusion/gating from Ch. 21; error re-entry to Ch. 25.
