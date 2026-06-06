# Chapter 27 — Distortion Compensation

> **Status:** DRAFT · **Part X — Calibration**
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
  (Ch. 21 §21.6, Ch. 23 §23.6).

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
- **Compensation adds its own error and latency** (model residual, witness noise,
  inference time) that must re-enter the error budget (Ch. 25) — compensation is
  not free.

> **Engineering takeaway.** The distortion hierarchy is: **keep distorters out**
> (protocol) → **map static distortion** (Ch. 26) → **observe it** (witness
> sensors) → **detect and down-weight it** (fusion/gating) → **model it** (physics
> + ML, with validation and uncertainty). Real systems layer several of these.
> The one thing never to do is silently trust a distorted measurement.

---

## Open questions / to verify
- Source quantitative generalization results for witness-sensor and ML
  compensation across *different* rooms/distorters (beyond the original
  demonstrations) to gauge real-world robustness [@cavaliere2023; @kindratenko2005].
- Add the online/uncertainty-aware compensation literature (e.g. spatial-
  uncertainty online error compensation) with verified citations.
- Build a Phase-5 "distortion field visualizer" + "eddy-current simulator" and a
  worked witness-sensor compensation demo (project brief modules).

## Sources cited
- [@cavaliere2023] witness-sensor pre-trained distortion compensation (C-arm
  1.52 mm RMS). [@kindratenko2005] neural-network calibration; [@kindratenko2000]
  correction-method survey. [@poulin2002; @birkfellner1998] distortion magnitudes/
  characterization. Fusion/gating from Ch. 21; error re-entry to Ch. 25.
