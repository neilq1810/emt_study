# Chapter 33 — Performance Characterization & Benchmarking

> **Status:** DEEPENED (awaiting review) · **Part XVI — Performance Characterization**
> The empirical counterpart to the capstone (Ch. 31): you have built a
> generator + sensor system — now how do you *measure*, *report*, and *compare* its
> performance honestly? Citation keys resolve to
> [`../../citations/bibliography.json`](../../citations/bibliography.json).

Throughout this book we have predicted performance (the CRLB, Ch. 24; the error
budget, Ch. 25) and corrected it (calibration, Ch. 26; compensation, Ch. 27). This
chapter closes the loop with the third discipline: **empirically characterizing**
the delivered performance of a generator + sensor combination, so it can be
*verified against the budget*, *put on a datasheet*, and *compared* — fairly —
against alternatives. It is the methodology the book has invoked dozens of times
("standardized assessment," "independent comparison," "insist on the conditions,"
Ch. 28) but never laid out: the **metrics / figures of merit**, the **comparison
methodology** across a working volume and between sensor–generator pairs, and the
**characterization rig** that generates the data — with the honesty discipline that
a number without its conditions is a claim, not a measurement.

---

## 33.1 Three distinct disciplines: don't conflate them

| Discipline | Question | Direction | Chapter |
|---|---|---|---|
| **Error budgeting** | what error *should* this system have? | bottom-up, predictive | Ch. 25 |
| **Calibration** | how do I *correct* my system to be accurate? | inward, fitting | Ch. 26 |
| **Characterization** | what error *does* it actually deliver, under stated conditions? | empirical, on independent data | **this chapter** |

The cardinal sin is collapsing the third into the second: quoting a
**calibration-set residual** as if it were independent characterization. A model
evaluated on the data that trained it overstates accuracy (Ch. 26 §26.5); honest
characterization is measured on **held-out poses** the calibration never saw, and
its job is partly to *catch* a wrong error budget — if the measured map does not
match the predicted budget (Ch. 31 §31.6) within the rig's own uncertainty, the
budget is incomplete.

## 33.2 The figures of merit

The vocabulary, with the distinctions practitioners most often blur:

- **Trueness vs. precision vs. "accuracy" (ISO 5725 [@iso5725]).** *Trueness* is
  closeness to truth — the **systematic/bias** term, i.e. the deterministic floor
  (Ch. 25 §25.3). *Precision* is **repeatability/reproducibility** — the **random**
  term, i.e. the stochastic floor and what is loosely called *jitter* (Ch. 25
  §25.2). Colloquial "accuracy" bundles both. The distinction is operational: a
  system can be **precise but untrue** (a repeatable bias — *calibratable*, Ch. 26)
  or **true but imprecise** (correct on average but noisy — needs averaging/SNR,
  not calibration). **Report both**, never one as a proxy for the other.
- **Resolution** — the smallest change that moves the output beyond the noise; set
  by jitter/quantization (Ch. 18), and *not* the same as accuracy (a system can
  resolve 10 µm steps yet be 1 mm untrue).
- **Position and orientation error**, for 5- or 6-DOF, reported separately;
  orientation in degrees, remembering the **tip lever-arm** that converts an
  angular error into a position error at the instrument tip (Ch. 15 §15.2, Ch. 29).
- **Statistical descriptors** — mean (bias/trueness), standard deviation
  (precision/jitter), **RMS**, **95th percentile**, and **max**. RMS flatters;
  safety-critical use (Ch. 29) lives on the percentile/max tail.
- **Working volume and spatial coverage** — the volume over which a spec *holds*,
  and the **accuracy-vs-position map** (the z⁴ degradation toward the edges,
  Ch. 24). "Accuracy = X mm" is meaningless without "over volume V, at range r."
- **Dynamic metrics** — update rate, **latency**, **dynamic accuracy** (error vs.
  target speed), and group delay / phase lag (Ch. 12). Static accuracy does *not*
  imply dynamic accuracy.
- **Distortion robustness** — error vs. a **standardized distorter** (material,
  size) at a **standardized distance** — the Hummel metal-object test [@hummel2005];
  report the *sensitivity curve*, not one clean-room number.
- **Stability** — warm-up transient, drift over time and temperature (Ch. 26
  §26.6), and repeatability across power cycles and re-mounts.

| Metric | Bounds / reveals | Book tie |
|---|---|---|
| Trueness (bias) | calibratable systematic error | 25.3, 26 |
| Precision (jitter) | irreducible noise floor | 25.2, 24 |
| Accuracy map | usable volume vs range (z⁴) | 24 |
| Latency / dynamic acc. | real-time/closed-loop fitness | 12, 21 |
| Distortion sensitivity | robustness to the OR/IR room | 6, 27 |
| Drift / warm-up | recalibration interval | 26.6, 15 |

## 33.3 Why single-number FoMs mislead — and how to normalize

A lone "accuracy" number hides volume, range, conditions, static-vs-dynamic, and
which tail (RMS vs. 95th vs. max). Two defensible responses:

1. **Report the distribution and the map, not a hero number** — a spec table with
   *conditions*, plus the accuracy-vs-position map (§33.2). This is the Ch. 28
   discipline applied to your own system.
2. **Normalize to compare designs, not just sizes.** The link budget (Ch. 8
   eq. 8.1) says $\sigma_\text{pos}\propto e_n\sqrt{\text{ENBW}}\,r^4\,\text{PDOP}/
   (m_t N_sA_s\omega)$ — so two generators can differ in accuracy *trivially*
   because one has a bigger moment. To compare the **design quality** of two
   generator + sensor pairs, hold the protocol fixed **and** normalize out the
   moment / area-turns / bandwidth, leaving the part that reflects engineering
   (noise efficiency, geometry/PDOP, distortion handling) rather than brute size.
   A "moment-normalized accuracy" or "accuracy × usable-volume" composite is more
   honest than raw millimetres — provided the normalization is *disclosed*.

## 33.4 Established protocols

- **The Hummel protocol** [@hummel2005] is the de-facto EMT standard: a machined
  base plate with a precise **50 mm grid of holes** plus a circle of equispaced
  holes for rotation, enabling reproducible, comparable measurement of residual
  position/orientation error **and** the influence of metallic objects. Its value
  is *comparability* — the same fixture and procedure across labs and systems
  (Ch. 28), traceable to the plate's machining tolerance.
- **ASTM F2554** [@astm_f2554] is the formal *standard practice* for measuring and
  reporting the **positional accuracy of computer-assisted surgical systems** (the
  tracking subsystem) — defining how to locate known points and report accuracy/
  repeatability so users can compare **within and between** manufacturers. It is the
  closest thing to a recognized navigation-accuracy standard, and like Hummel it is
  essentially **static**.
- **The assessment/validation literature** — Franz et al.'s review [@franz2014] and
  Yaniv et al.'s clinical-environment study [@yaniv2009] — codifies *reporting with
  conditions* and the lab-vs-in-situ gap.
- **General metrology underpinnings** — ISO 5725 for the trueness/precision
  decomposition [@iso5725] and the GUM for combined/expanded uncertainty
  [@gum2008] (the same machinery as the Ch. 25 budget).
- **The gap (Ch. 30).** Standard protocols are largely **static**; a
  *dynamic*- and *distortion*-standardized protocol — so moving-target and
  moving-distorter claims are comparable — is an open community need.

## 33.5 The characterization rig: the ground-truth hierarchy

To measure a system you need a reference pose that is **better** and **traceable**.

> **The cardinal rule.** The ground-truth (GT) uncertainty must be **≈ 5–10×
> smaller** than the DUT spec you wish to resolve, and **traceable** to a standard.
> To credibly verify a 1 mm system, the GT must be good to ~0.1–0.2 mm.

Representative references and their typical accuracies (conf: med — vendor-class
ranges, not a single source):

| Reference | Typical accuracy | DOF / mode | Notes |
|---|---|---|---|
| Machined aperture / phantom board (Hummel) | hole positions ~0.01–0.1 mm | discrete static poses | cheap, reproducible, comparable; traceable to machining |
| Precision linear / rotary stages | ~1–10 µm / ~0.001° | programmable volume scan | best for automated maps; stack XYZ + goniometer |
| Coordinate measuring machine (CMM) | ~1–5 µm | touch poses | static gold standard; slow |
| Robot arm | repeatability ~50–100 µm (abs. worse) | continuous 6-DOF trajectories | great for dynamic — but it is full of steel/motors |
| Optical tracker (stereo IR) | ~0.1–0.3 mm | continuous 6-DOF, non-contact | needs line of sight; must itself be characterized |

Match the reference to the metric: **stages/CMM/phantom board** for static trueness
and the accuracy map; **robot/optical** for dynamic accuracy and latency; the
**phantom board** for cheap cross-system comparison.

## 33.6 The rig's own error budget (worked)

The GT uncertainty enters **every** measurement, so you can only resolve system
error well above the combined rig floor. If the terms are independent (Ch. 25
§25.5),

$$
\sigma_\text{measured}^2 = \sigma_\text{system}^2 + \sigma_\text{GT}^2 + \sigma_\text{reg}^2 + \sigma_\text{thermal}^2 .
$$

**Worked example.** A rig built around a precision stage: GT $\sigma_\text{GT}=
0.02$ mm, GT-to-EMT frame **registration** $\sigma_\text{reg}=0.15$ mm,
thermal/mechanical $\sigma_\text{thermal}=0.05$ mm → rig floor
$\sqrt{0.02^2+0.15^2+0.05^2}\approx \mathbf{0.16}$ **mm**.

- Measuring a **1 mm** system: $\sqrt{1^2+0.16^2}=1.013$ mm — the rig inflates the
  reading ~1.3 %. Fine.
- Measuring a **0.2 mm** system: $\sqrt{0.2^2+0.16^2}=0.256$ mm — a **28 %**
  inflation. You *cannot* credibly characterize a 0.2 mm system on this rig — it
  violates the 5–10× rule. The rule, made numeric.

Note which term dominates: **registration** (0.15 mm), not the GT device (0.02 mm)
— exactly the clinical-chain lesson (Ch. 29 §29.7). The GT-to-EMT transform is a
6-DOF fit; minimize its error with many **well-spread fiducials** spanning the
volume and a good solve (Ch. 23), and **report it separately** (its fiducial- and
target-registration error) so it is never silently charged to the system.

## 33.7 Building the rig — practical considerations

The hard, easily-overlooked part — *how to build a rig that measures EMT without
corrupting it*:

- **The rig must not distort the field it measures (the irony).** Construct the
  moving fixtures from **non-magnetic *and* non-conductive** materials — acrylic,
  Delrin/POM, glass-epoxy, ceramic. Beware that "non-magnetic" metals still distort
  AC systems: **aluminium and brass are conductive → eddy currents** (Ch. 6). Many
  precision stages are steel-and-aluminium; keep their **motors, encoders, bearings
  (magnets + steel)** far from the volume on long non-metallic extension arms, or
  use ceramic/air-bearing stages. This constraint often *dominates* rig design.
- **Baseline the empty volume first.** Map the volume with no distorter to capture
  the room's residual non-uniformity (rebar, equipment); that "null map" is your
  environmental noise floor and must be subtracted/acknowledged.
- **Thermal control.** Warm up DUT *and* rig, and **log temperature** — the system
  drifts ~1.5 mm per 5 °C (Ch. 15 §15.5, Ch. 26 §26.6), so a few uncontrolled
  degrees masquerade as accuracy error.
- **Registration procedure.** Collect fiducials spread across the volume, solve the
  rigid (or scaled-rigid) GT→EMT transform, and report **FRE/TRE** so registration
  error is separated from system error (§33.6).
- **Sampling design.** Trade density (the $h^{-3}$ cost, Ch. 26 §26.4) against
  coverage; **dwell** long enough per pose to average jitter down and expose the
  *bias* (separating trueness from precision); **randomize** visit order to
  decorrelate slow drift; **revisit** poses to quantify repeatability.
- **Dynamic tests.** Drive programmed trajectories at known velocity:
  cross-correlate the GT and EMT time series to extract **latency/group delay**
  (Ch. 12), and report **dynamic accuracy** vs. speed; a rotating fixture exercises
  orientation and the roll DOF (Ch. 13).
- **Automation & data.** Programmatic stage control synchronized and **timestamped**
  with EMT capture; store raw + GT + temperature; collect enough samples for GUM
  Type-A confidence intervals (Ch. 25 §25.1).

**Pitfalls that quietly ruin a characterization:** metal in the rig; registration
error counted as system error; testing on calibration data; reporting only the
best region; ignoring dynamics; and measuring at a single temperature.

## 33.8 Reporting — the honesty contract

A defensible performance report states, at minimum: the **protocol**; the
**volume/range** and where in it; **static vs. dynamic**; the **distorter
conditions**; the sample count **n**; the **distribution** (RMS *and* 95th
percentile *and* max); **trueness and precision separately**; the **GT traceability
and rig floor**; and the **temperature**. Reading a competitor's datasheet
(Ch. 28), demand the same — a single accuracy figure stripped of these is
marketing, not measurement. And this is precisely how you **validate the capstone**
(Ch. 31 §31.6): the measured accuracy map must reproduce the predicted error budget
(Ch. 25) to within the §33.6 rig floor, or the budget is wrong or incomplete.

## 33.9 The standards landscape and a proposed dynamic/distortion benchmark

Pulling §33.4 together, the **recognized basis for comparing EMT performance is thin and
static**: the **Hummel** protocol [@hummel2005] (de-facto, static accuracy + a metal-object
influence test), **ASTM F2554** [@astm_f2554] (a formal static positional-accuracy
practice for navigation systems), and the metrology underpinnings **ISO 5725 / GUM**
[@iso5725; @gum2008]; the IEC 60601 family governs *safety/EMC*, not accuracy. None of
these characterizes the regime where EMT actually fails clinically — a **moving** sensor
near a **moving** conductor (the C-arm, Ch. 29 §29.9; the breathing patient, Ch. 41) — and
none standardizes the distorter tightly enough for cross-lab dynamic comparison. The
result is the recurring problem of Part XVI: vendor accuracy numbers are static, optimistic,
and not comparable in the dynamic-distortion conditions that matter (Ch. 30).

**A proposed dynamic-and-distortion benchmark.** The gap is fillable with a reproducible
protocol that extends Hummel/F2554 from static poses to *motion under distortion*:

| Element | Specification (proposed) |
|---|---|
| **Sensor motion** | a programmable stage drives the sensor along a **standardized trajectory** (a defined 3-D Lissajous *and* a clinically representative respiratory waveform, Ch. 41) at **specified speeds**, so dynamic path error and lag are measured, not just static residuals |
| **Distorter** | a **specified** conductor (material/size/shape — e.g. a defined stainless and a defined aluminium plate, plus a "reference C-arm surrogate") at **standardized distances**, tested **both static and moving** on a second stage to excite dynamic eddy-current distortion (Ch. 6) |
| **Ground truth** | an **independent** dynamic reference (encoded stage and/or optical tracker) with its **own stated dynamic uncertainty** — the hardest element (Ch. 33 §33.5, Ch. 41) and the one that sets the benchmark's floor |
| **Metrics** | dynamic/path RMS vs speed; **latency / phase lag** (Ch. 12); distortion-induced error vs distorter distance **and velocity**; and — decisively — **detect-and-flag performance**: does the quality flag assert *before* error exceeds tolerance, with what **latency and false-alarm rate** (an ROC-style curve)? |
| **Reporting** | the §33.8 honesty contract, extended: trajectory, speeds, full distorter spec, GT method **and its dynamic uncertainty** |

The decisive addition is the last metric. The entire safety argument of this book rests on
**detect-and-flag firing before the error becomes dangerous** (Ch. 27/44/45, and the V&V
line in Ch. 48 §48.5). Yet no current protocol *tests that claim* — it is asserted, not
measured. A standardized dynamic-distortion benchmark with an explicit
**flag-latency / false-alarm characterization** would convert the load-bearing safety
control from a design intention into a **measured, comparable, auditable** property — which
is exactly what a "definitive" benchmark for clinical EMT should do, and a concrete
candidate to take to the standardization community (Ch. 30). (conf: med — the landscape and
gap are well-supported; the specific benchmark is a *proposal* to be piloted and refined,
e.g. as a Phase-5 dynamic-error/flag-ROC simulation before a physical rig.)

> **Engineering takeaway.** Characterization is the empirical twin of the error
> budget. A figure of merit without its conditions, its distribution, and its
> traceable ground-truth floor is not a measurement — it is a claim. Build the rig
> so its own error sits 5–10× below what you report, keep it non-magnetic and
> thermally controlled, separate trueness from precision and static from dynamic,
> map the *whole* volume, and disclose everything. And recognize that the recognized
> standards (Hummel, ASTM F2554) are **static**: the open need — and a concrete
> contribution this book proposes (§33.9) — is a **dynamic, distortion-standardized
> benchmark that measures detect-and-flag latency and false-alarm rate**, turning the
> safety case's load-bearing control into a comparable, audited number.

---

## Open questions / to verify
- 🟡 **Proposed (§33.9, T2.27):** a **dynamic- and distortion-standardized** benchmark
  (standardized trajectory + moving distorter + flag-latency/false-alarm metrics)
  extending Hummel [@hummel2005] / ASTM F2554 [@astm_f2554]. Remaining: **pilot it as a
  Phase-5 dynamic-error / flag-ROC simulation** before a physical rig, and take to the
  Ch. 30 standardization community.
- Back §33.2/§33.6 with a **Phase-5 accuracy-vs-position map** simulation and a
  **Phase-6 "characterization explorer"** tool (accuracy map + rig-floor calculator
  over the working volume) tying to the existing CRLB/working-volume tools.
- Re-confirm the representative reference accuracies in §33.5 against current
  metrology vendor specs (currently conf: med, vendor-class ranges) and add a
  traceability/NIST reference for the ground-truth chain.
- Add primary references for optical/CMM/robot accuracy-assessment methodology
  (e.g. target-registration-error theory) to firm up §33.6.

## Sources cited
- [@hummel2005] Hummel assessment protocol (the EMT standard; metal-object test).
  [@franz2014; @yaniv2009] validation/clinical-environment assessment with
  conditions. [@iso5725] trueness/precision (accuracy) definitions. [@gum2008]
  uncertainty propagation. [@birkfellner1998] systematic-distortion
  characterization methodology. [@astm_f2554] ASTM positional-accuracy practice for
  computer-assisted surgical systems (the formal static standard, §33.4/§33.9).
  Budget/CRLB ties to Ch. 24–25; capstone validation to Ch. 31; dynamic-distortion
  standardization to Ch. 30.
