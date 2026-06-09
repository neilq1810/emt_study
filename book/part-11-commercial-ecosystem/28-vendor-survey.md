# Chapter 28 — Commercial Ecosystem: Vendor Survey

> **Status:** DEEPENED (awaiting review) · **Part XI — Commercial Ecosystem** (the whole of Part XI)
> Connects the engineering of Parts II–X to the products that embody it. Citation
> keys resolve to [`../../citations/bibliography.json`](../../citations/bibliography.json).

This chapter surveys the companies and systems that turned electromagnetic
tracking from physics into product. For each major player we note history,
technology, architecture, strengths/weaknesses, clinical adoption, and market
position — mapping each onto the architectural forks established earlier
(AC vs. pulsed-DC, Ch. 8; coil vs. field sensor, Ch. 13; the error/calibration
story of Parts IX–X).

> **A standing caution, restated (Ch. 1 §1.11, Ch. 25).** Vendor performance
> numbers are measured under non-standardized, often best-case conditions and are
> *not* directly comparable. Throughout, we prefer figures from **standardized
> protocols** [@hummel2005] and **independent assessments** [@franz2014;
> @yaniv2009] over datasheet claims, and tag vendor-reported values accordingly.
> Corporate dates/acquisitions below are from vendor and trade-press sources
> (conf: med unless corroborated).

---

## 28.1 Polhemus — the AC pioneer

- **History.** Founded **1969 by Bill Polhemus**, Colchester, Vermont; the
  original commercializer of **AC electromagnetic tracking**, born from
  military-aviation **helmet/head-tracking** (Ch. 1 §1.3) [@polhemus_history].
  The foundational Raab et al. 1979 paper comes from this lineage [@raab1979].
- **Technology/architecture.** Continuous **AC** excitation of an orthogonal
  transmitter triad, sensor pickup coils, synchronous detection (Ch. 8, 20);
  native 6-DOF [@polhemus_tech]. Products: **FASTRAK, LIBERTY, PATRIOT, G4**
  [@polhemus_history].
- **Strengths.** Mature, high-update-rate 6-DOF; strong in VR/AR, biomechanics,
  motion capture, simulation, and graphics digitizing.
- **Weaknesses.** As an AC architecture, more sensitive to **conductive
  (eddy-current) distortion** (Ch. 6 §6.2) than pulsed-DC; historically
  laboratory/industrial rather than catheter-scale medical.
- **Market.** The enduring AC reference brand outside the cath lab. (conf: med —
  vendor-sourced history/products.)

## 28.2 Ascension Technology — pulsed-DC and the "Flock of Birds"

- **History.** Co-founded **1986 by Jack Scully and Ernest ("Ernie") Blood**
  (a Raab et al. co-author, Ch. 1 §1.6), Vermont; pioneers of **pulsed-DC**
  tracking, famed for the **Flock of Birds** and **microBIRD**, plus OEM medical
  modules (**trakSTAR/driveBAY**) [@ascension_roper2012]. Acquired by **Roper
  Industries (~US\$19M, 2012)** and operated under **NDI** [@ascension_roper2012].
- **Technology/architecture.** **Pulsed-DC** excitation: energize, wait for
  eddy-current settling, sample the static field (Ch. 6 §6.4) — using
  (quasi-)static field sensing rather than pure AC pickup. Native 6-DOF.
- **Strengths.** Reduced **conductive** distortion versus AC (the pulsed-DC
  advantage); widely used in research and as OEM medical tracking; the Ascension
  microBIRD is one of the systems characterized by the **Hummel protocol**
  [@hummel2005].
- **Weaknesses.** No relief from **ferromagnetic** distortion (Ch. 6 §6.3);
  per-axis settling can limit update rate (Ch. 10 §10.5).
- **Market.** The pulsed-DC counterweight to Polhemus's AC; post-2012 part of the
  NDI medical-tracking portfolio. (conf: med — trade-press/vendor.)

## 28.3 Northern Digital Inc. (NDI) — Aurora and medical-grade EMT

- **History.** Waterloo, Ontario; established in **optical** surgical navigation
  (**Polaris**) before its **Aurora** EM system; acquired by **Roper (2011)** and
  itself acquired **Ascension (2012)**, consolidating much of the medical/OEM EM
  tracking market [@ndi_history; @ascension_roper2012].
- **Technology/architecture.** **Aurora** targets medical use with very small
  (sub-millimeter, e.g. micro 5-DOF ~0.3 mm dia.) sensor coils for catheters/
  needles/endoscopes, a planar field generator, and OR-grade electronics
  [@ndi_aurora; @yaniv2009] (Ch. 9, 13–14). Offers **5-DOF and 6-DOF** sensors.
- **Strengths.** The de facto **research/OEM standard** for medical EMT; extensive
  independent characterization [@hummel2005; @yaniv2009; @franz2014]; broad sensor
  catalog.
- **Weaknesses.** As a field-generator/small-sensor AC-class system, subject to
  the usual distortion constraints; performance strongly volume- and
  environment-dependent (Ch. 25).
- **Market.** Dominant supplier of **OEM EM tracking to medical-device
  integrators** and the most-cited platform in the academic EMT literature.
  (conf: med–high — vendor history + independent literature.)

## 28.4 Biosense Webster — CARTO and the EP breakthrough

- **History.** **Biosense** founded **1993 by Shlomo Ben-Haim**; acquired by
  **Johnson & Johnson in 1997 (~\$400M in shares)** and merged with Webster to form
  **Biosense Webster** [@globes_jnj_biosense]. The scientific basis is the
  Gepstein/Ben-Haim 1997 nonfluoroscopic electroanatomical-mapping paper
  [@gepstein1997] (Ch. 1 §1.8); **CARTO 3** launched 2009.
- **Technology/architecture.** Magnetic localization of a catheter sensor over an
  external low-field "location pad," reconstructing 3-D electroanatomical maps;
  later versions fuse magnetic with **impedance**-based localization for
  multi-electrode visualization. (conf: med — architecture per clinical
  literature; impedance fusion details vary by generation.)
- **Strengths.** The clinical and commercial juggernaut of **cardiac
  electrophysiology** (Ch. 29); deep integration with ablation workflows;
  reduces fluoroscopy [@gepstein1997].
- **Weaknesses.** Closed clinical ecosystem (not a general-purpose tracker);
  application-specific.
- **Market.** Market-leading EP electroanatomical-mapping platform under J&J
  MedTech. (conf: med–high.)

## 28.5 EP competitors — Abbott (St. Jude) EnSite & Boston Scientific Rhythmia

- **Abbott / St. Jude EnSite (Precision/X).** A competing EP mapping platform
  historically built on **impedance**-based localization, with later generations
  adding **magnetic** sensor localization (a hybrid impedance+magnetic approach).
  (conf: med — generational details vary; verify per product.)
- **Boston Scientific Rhythmia.** EP mapping using a combination of **magnetic and
  impedance** localization with a high-density mapping catheter. (conf: med.)

These illustrate a key ecosystem point: in EP, **pure-EM and impedance-based (and
hybrid)** localization compete, and "EM tracking" in the cath lab often means a
*fusion* of magnetic and impedance sensing rather than magnetic alone (links to
the fusion theme of Ch. 21). Exact architectures and performance require
per-product primary sources (flagged below).

**Why fuse magnetic with impedance?** The two localization principles are
complementary in exactly the way Ch. 21 fusion exploits:
- **Magnetic** (the subject of this book) is **absolute and geometrically
  accurate** — pose comes from the known dipole field (Ch. 5) — but a 6-DOF
  magnetic sensor on *every* electrode of a 64-electrode basket is impractical.
- **Impedance** localization injects a small current between body-surface patches
  and reads the resulting voltage at each catheter electrode; position follows
  from the voltage gradient. It needs **no magnetic sensor per electrode** (so it
  scales to many electrodes cheaply) but is **nonlinear and inhomogeneous** —
  tissue conductivity varies, so the impedance "space" is warped and drifts.
The clinical fusion uses a few **magnetically-tracked** points as ground truth to
**warp the impedance field into real geometry**, getting magnetic accuracy *and*
impedance's per-electrode scalability. It is the same absolute-reference-corrects-
a-cheap-dense-modality pattern as EM+IMU (Ch. 21 §21.5). (conf: med — principle is
standard; per-product implementation varies.)

## 28.6 Pulmonary, robotics, navigation platforms & emerging players

- **superDimension (ENB).** Electromagnetic **navigation bronchoscopy**: a CT-
  derived 3-D airway map plus an EM-tracked steerable catheter to reach
  peripheral lung lesions. Acquired by **Covidien (~\$300M, 2012)**; **Medtronic**
  closed its Covidien acquisition in **Jan 2015** [@covidien_superdimension2012]
  (Ch. 29). (conf: med — trade-press figures.)
- **Robotic bronchoscopy/navigation** (e.g. robotic platforms integrating EM or
  hybrid localization) and **ENT/IR navigation** systems increasingly embed EM
  tracking; specific vendors/architectures to be surveyed with primary sources.
- **Emerging startups & research spinouts** pursue chip-scale/array sensing
  (TMR/MR, Ch. 14.3), witness-sensor and ML distortion compensation
  [@cavaliere2023], and hybrid optical+EM/IMU systems (Ch. 30). The academic
  group behind the witness-sensor work (UCC/Tyndall) is one example bridging
  research and product [@cavaliere2023].

## 28.7 Cross-vendor comparison and how to read it

A defensible comparison rests on **standardized, independent** measurement, not
datasheets:

| Axis | AC lineage (Polhemus; NDI Aurora-class) | Pulsed-DC lineage (Ascension) | EP platforms (CARTO/EnSite/Rhythmia) |
|---|---|---|---|
| Excitation | continuous AC | pulsed-DC | magnetic and/or impedance (hybrid) |
| Conductive distortion | higher | lower | mitigated clinically + fusion |
| Ferromagnetic distortion | high | high | high |
| Sensor | pickup coils (sub-mm medical) | (quasi-)static field sensing | catheter sensor + electrodes |
| Primary market | VR/AR/biomech; OEM medical | research; OEM medical | cardiac EP |
| Independent assessment | [@hummel2005; @yaniv2009] | [@hummel2005] | clinical-outcome literature |

**How to compare fairly:** insist on the **measurement conditions** (working
volume, distance, distorter presence, static vs. dynamic), prefer **Hummel-
protocol** or peer-reviewed numbers [@hummel2005; @franz2014], and treat any
single accuracy figure without conditions as marketing (Ch. 25 §25.1). The
engineering chapters explain *why* two systems differ, and the **system link
budget (Ch. 8 eq. 8.1)** lets you reason about it quantitatively: a vendor's
accuracy is set by generator moment, sensor area-turns × frequency, AFE noise,
integration time, and PDOP — so a larger generator or a bigger sensor buys
accuracy, a smaller catheter coil costs it (the z⁴ penalty, Ch. 24), and the
excitation choice (Ch. 6, 8) sets the distortion term. Reading a datasheet
through eq. 8.1 and the three error classes (Ch. 25) turns "which is better?" into
"better *where*, and *why*."

---

## Open questions / to verify
- Corroborate all corporate dates/figures (Polhemus 1969; Ascension 1986 / Roper
  2012 / \$19M; J&J–Biosense 1997 / \$400M; Covidien–superDimension 2012 / \$300M;
  Medtronic–Covidien 2015) against a second independent source each; several are
  currently single-source trade press (conf: med).
- Replace qualitative EnSite/Rhythmia architecture notes with per-product primary/
  regulatory sources (510(k)/CE technical files).
- Build a sourced **performance table** using only standardized-protocol or
  peer-reviewed numbers with full conditions — explicitly *not* datasheet values.
- Add NDI founding year and Aurora first-release/first-510(k) dates from primary
  records (Ch. 1 open question).

## Sources cited
- [@polhemus_history; @polhemus_tech] Polhemus. [@ascension_roper2012] Ascension/
  Roper. [@ndi_history; @ndi_aurora] NDI/Aurora. [@globes_jnj_biosense;
  @gepstein1997] Biosense/CARTO. [@covidien_superdimension2012] superDimension.
  [@hummel2005; @yaniv2009; @franz2014] independent assessment. [@raab1979]
  AC foundation. [@cavaliere2023] emerging witness-sensor work.
