# Chapter 29 — Clinical Applications & Workflows

> **Status:** DRAFT · **Part XII — Medical Applications** (the whole of Part XII)
> Connects the technology (Parts II–X) and products (Ch. 28) to clinical use.
> Citation keys resolve to [`../../citations/bibliography.json`](../../citations/bibliography.json).

Electromagnetic tracking earns its place in medicine for one reason restated
throughout this book: it localizes small instruments **inside the body, without
line of sight** (Ch. 1 §1.1) [@franz2014]. This chapter surveys where that
capability matters clinically — cardiac electrophysiology, navigation
bronchoscopy, ENT/skull-base, interventional radiology, robotics, and image-
guided therapy — with attention to the **clinical workflow**, the **distortion-
management discipline** that the OR imposes (Ch. 6, 25, 27), and the
**regulatory** framework (Ch. 17). Reported accuracies are quoted with their
conditions; clinical *outcomes* (yield, complications) are cited from
peer-reviewed studies, not vendor claims.

---

## 29.1 Cardiac electrophysiology and ablation

The application that made EMT a major medical industry (Ch. 1 §1.8). A catheter-
borne magnetic sensor is localized over an external low-field generator
("location pad"), building a real-time 3-D **electroanatomical map** — chamber
geometry color-coded with electrical activation — so the electrophysiologist can
navigate an ablation catheter to arrhythmia substrate **without continuous
fluoroscopy**, cutting ionizing-radiation dose to patient and staff
[@gepstein1997] (the CARTO lineage, Ch. 28.4). The clinical workflow couples EMT
to the therapy itself (mapping → targeting → ablation → remap to confirm). In
practice, EP platforms often **fuse magnetic with impedance** localization
(Ch. 28.5), and the magnetic channel provides the drift-free absolute reference.

## 29.2 Electromagnetic navigation bronchoscopy (ENB)

For peripheral lung lesions beyond the reach of conventional bronchoscopic vision,
ENB uses a **CT-derived 3-D airway map** plus an **EM-tracked steerable catheter**
to navigate to the target for biopsy (the superDimension lineage, Ch. 28.6)
[@covidien_superdimension2012]. The evidence base is substantial: the prospective,
multicenter **NAVIGATE** study (>1,000 subjects) reported a **12-month diagnostic
yield of ~73%**, with ENB-related grade ≥2 **pneumothorax in ~2.9%** — a
diagnostic reach in roughly three-quarters of patients at a low complication rate
[@folch2019]. ENB exemplifies the **plan-then-navigate** workflow: pre-procedure CT
planning, intra-procedure registration of the patient to the plan, then EM-guided
navigation — and it is acutely sensitive to **respiratory motion** and CT-to-body
registration error (a clinical instance of the dynamic/model-mismatch errors of
Ch. 25). (conf: high — peer-reviewed outcomes [@folch2019].)

## 29.3 ENT and skull-base navigation

In endoscopic sinus and skull-base surgery, EMT localizes instruments relative to
the patient's CT near critical structures (orbit, skull base, carotid, optic
nerve) **without the line-of-sight constraint** of optical navigation — valuable
in the confined nasal corridor where the surgeon's hands and scope block sightlines.
Reported intraoperative localization accuracy is on the order of **~1–2 mm**
(application- and registration-dependent), and image guidance is associated with
safer, more complete surgery (conf: med — clinical literature; specific primary
ENT studies flagged in *Open questions*) [@franz2014]. The workflow hinges on
**registration** (patient-to-CT), whose error often dominates the EMT sensor error
in the clinical accuracy budget — a recurring theme: *system* accuracy is
registration ⊕ tracking ⊕ tip-offset (Ch. 14.2), not tracking alone.

## 29.4 Interventional radiology and biopsy guidance

EMT guides **needles, catheters, and probes** in percutaneous procedures (biopsy,
ablation, drainage), often **fused with CT or ultrasound** so the tracked tool is
displayed on pre-acquired or live imaging [@franz2014; @yaniv2009]. The
line-of-sight-free property is essential: the needle tip is *inside* the patient.
The dominant practical limitation is the **OR/IR distortion environment** — the
CT gantry, C-arm, table, and instruments — which Poulin & Amiot quantified
(ambient noise small, but ferromagnetic/electrical devices up to several mm and
large angular error) [@poulin2002], and which witness-sensor/compensation methods
target (the C-arm case reduced to 1.52 mm RMS, Ch. 27) [@cavaliere2023]. Clinical
accuracy here is the standardized-assessment story of Ch. 26 (Hummel)
[@hummel2005] applied in a hostile room.

## 29.5 Robotic surgery and image-guided therapy

EMT integrates with **robotic** platforms (e.g. robotic bronchoscopy/catheter
systems) and broader **image-guided therapy** (IGT) to provide instrument pose
where optical tracking cannot see, frequently **fused with robot kinematics, IMU,
and imaging** (Ch. 21). Here the **time-alignment** of modalities (Ch. 12 §12.5)
and the **latency** budget (Ch. 12) become first-order: a robot closing a control
loop on EM pose needs bounded, timestamped, low-jitter pose, and graceful
degradation/flagging under distortion (Ch. 22 §22.6, Ch. 27 §27.4). IGT couples
tracking to therapy delivery (ablation, brachytherapy, targeted drug delivery),
where pose error maps directly to therapeutic margin.

## 29.6 AR-assisted navigation and future applications

Augmented-reality overlays of tracked instruments and plans onto the surgeon's
view, untethered hidden sensors, and **hybrid optical+EM/IMU** systems (Ch. 30)
are active directions. The clinical promise is intuitive guidance with EMT's
no-line-of-sight robustness; the challenge is the same distortion/registration/
latency triad, now with a human-perception loop that is unforgiving of lag and
mis-registration. (conf: low–med — emerging; treated as frontier in Ch. 30.)

## 29.7 Clinical workflow, regulatory requirements & integration

### The clinical accuracy chain
A theme across §§29.1–29.5: **clinical accuracy ≠ sensor accuracy.** The patient-
facing error is the composition of (i) sensor/tracking error (Parts IV–IX),
(ii) **registration** (patient/image-to-tracker), (iii) **tip/instrument offset**
(Ch. 14.2), (iv) **target motion** (respiration, cardiac) between imaging and
action, and (v) residual **distortion** (Ch. 27). Often (ii)–(iv) dominate (i).
A rigorous clinical claim budgets all five (Ch. 25).

### Regulatory framework
A tracker used clinically is a regulated **medical device**:
- **Electrical safety & EMC.** IEC 60601-1 (two means of protection; **Type CF**
  leakage limits for intracardiac sensors, Ch. 17 §17.3) [@iec60601_1] and
  IEC 60601-1-2 EMC with **pose-defined essential performance** [@iec60601_1_2].
- **Market clearance.** FDA **510(k)** clearance (substantial equivalence) or PMA,
  and CE marking under EU MDR — requiring the verification/validation,
  risk management, and accuracy evidence that Parts IX–X and standardized
  assessment [@hummel2005] supply. (conf: med — general regulatory framing;
  specific clearances per product flagged in Ch. 28 open questions.)
- **Essential performance in pose terms.** The system must define and defend, e.g.,
  "position error within X mm under stated conditions, or flag loss of tracking"
  (Ch. 17 §17.3) — connecting clinical safety to the error budget (Ch. 25) and
  fault behavior (Ch. 22, 27).

### Integration architectures
Clinical EMT rarely stands alone: it integrates with imaging (CT/US/fluoro/MRI
planning), navigation software, robots, and the OR network, exchanging
**timestamped pose + covariance** (Ch. 11, 21) over defined interfaces. The
integration must preserve the latency budget (Ch. 12) and propagate uncertainty
so downstream decisions (display, control, therapy) are made with honest error
bars.

> **Takeaway.** EMT's clinical value is the no-line-of-sight localization of hidden
> instruments — proven at scale in EP and ENB and broadly across IR/ENT/robotics.
> But clinical accuracy is a *system* property dominated as often by registration,
> motion, and distortion as by the tracker itself, and it must be delivered inside
> a regulated safety/EMC framework with honest, flagged uncertainty.

---

## Open questions / to verify
- Attach primary ENT/skull-base accuracy studies (e.g. multicenter EM image-guided
  endoscopic surgery; registration-modality comparisons) to firm up §29.3
  (currently review-cited, conf: med).
- Confirm Folch 2019 NAVIGATE vol/issue/pages (14(3):445-458) and expand the author
  list [@folch2019].
- Source specific FDA 510(k)/CE clearances for named systems (Aurora, CARTO,
  superDimension) with clearance numbers/dates (ties Ch. 28).
- Add EP clinical-outcome and EM+US/CT fusion-accuracy references for §29.1/29.4.

## Sources cited
- [@gepstein1997] EP electroanatomical mapping. [@folch2019] NAVIGATE ENB outcomes.
  [@covidien_superdimension2012] superDimension. [@franz2014; @yaniv2009] clinical
  EMT review/environment. [@poulin2002] OR interference. [@cavaliere2023] C-arm
  compensation. [@hummel2005] standardized assessment. [@iec60601_1; @iec60601_1_2]
  safety/EMC.
