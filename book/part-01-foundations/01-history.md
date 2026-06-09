# Chapter 1 — History of Electromagnetic Tracking

> **Status:** DEEPENED (awaiting review) · **Part I — Foundations**
> Citation keys `[@key]` resolve to [`../../citations/bibliography.json`](../../citations/bibliography.json).
> Confidence tags follow [`../../ROADMAP.md`](../../ROADMAP.md#research-quality-control).

---

## 1.1 What "electromagnetic tracking" means, and what it competes with

Electromagnetic tracking (EMT) determines the **position** (three translational
coordinates) and, in most systems, the **orientation** (up to three rotational
coordinates) of one or more small sensors relative to a reference frame, by
measuring the coupling of low-frequency magnetic fields between a set of
*generator* (transmitter) coils and a set of *sensor* (receiver) coils. The
defining engineering virtue — the property that no competing modality matches —
is that **it does not require line of sight**. Magnetic fields at the
frequencies used (typically a few hundred Hz to tens of kHz) pass essentially
unperturbed through soft tissue, plastic, and the human body, so a sensor can be
embedded at the tip of a catheter, a biopsy needle, or a flexible bronchoscope
and still be localized in real time [@franz2014].

This single property frames the entire history of the field. Optical tracking
(stereo cameras tracking retroreflective markers, or structured light) is more
accurate and drift-free but is blocked the instant the marker leaves the
camera's view — which is precisely what happens when an instrument enters the
body. Inertial tracking (accelerometers and gyroscopes) needs no external
infrastructure but drifts without bound. Mechanical linkages and goniometers are
accurate but tether the tracked object to a kinematic chain. EMT occupies the
niche of **small, untethered, hidden sensors localized through opaque media** —
and that niche turned out to be enormously valuable in image-guided medicine.
The dominant trade EMT accepts in return is sensitivity to **field distortion**
from nearby conductors and ferromagnetic materials, a theme that recurs through
Parts II, IX, and X.

## 1.2 Pre-history: the motivation for line-of-sight-free tracking

The intellectual prerequisites for EMT were complete by the late nineteenth
century: Faraday's law of induction (1831) and Maxwell's unification of
electromagnetism (1865) give, in principle, everything needed to relate a
time-varying magnetic dipole source to the voltage induced in a distant pickup
coil (Part II develops this rigorously). What was missing for nearly a century
was not the physics but the **electronics**: stable oscillators, low-noise
amplification, phase-sensitive (lock-in) detection, and — decisively — the
digital computation needed to invert the nonlinear field equations fast enough
to be useful. EMT is, in this sense, a child of mid-twentieth-century
electronics rather than of nineteenth-century physics.

## 1.3 Military and aerospace origins: helmet-mounted sighting

The practical impetus for 6-DOF magnetic tracking came from **military aviation**
and the problem of the *helmet-mounted sight* (HMS): to slave a weapon or sensor
to where a pilot is looking, the system must continuously know the orientation
(and ideally position) of the pilot's helmet inside the cockpit. The cockpit is
a cluttered, line-of-sight-hostile environment, which made magnetic coupling an
attractive solution. (conf: high — this application context is documented
throughout the early EMT literature, including the foundational paper's framing
[@raab1979].)

The canonical engineering statement of the problem and its solution is the 1979
paper by **Frederick H. Raab, Ernest B. Blood, Terry O. Steiner, and Herbert R.
Jones**, *"Magnetic Position and Orientation Tracking System,"* in *IEEE
Transactions on Aerospace and Electronic Systems* [@raab1979]. The authors'
institutional affiliation (the Polhemus Navigation Sciences lineage) and the
journal of publication (Aerospace and Electronic Systems) both reflect the
military/aerospace origin. This paper is the single most important historical
document in the field and is treated in detail in §1.5.

## 1.4 The Polhemus lineage and AC magnetic tracking

The earliest commercial magnetic trackers grew out of work associated with
**Polhemus** (founded 1969 by Bill Polhemus, Colchester, Vermont, USA)
[@polhemus_history]. Polhemus systems are built on **AC (alternating
current) electromagnetic tracking**: the transmitter continuously drives a
triad of mutually orthogonal coils with sinusoidal currents (in early systems by
*frequency-* or *time-multiplexing* the three axes), and a triad of sensor coils
measures the induced voltages, from which the 3×3 coupling matrix — and hence
pose — is recovered. Polhemus describes its core technology as proprietary AC
electromagnetic tracking delivering true 6-DOF (position in x, y, z plus pitch,
roll, yaw) (conf: med — vendor self-description) [@polhemus_tech].

The IP root of this lineage is **Jack Kuipers**' 1975 patent (US 3,868,565,
"Object tracking and orientation determination means, system and process")
[@kuipers1975] — work sometimes referred to by the acronym **SPASYN**. A
historically important nuance, now verified against the patent record (Ch. 2
§2.1) and *resolving the SPASYN attribution flagged in earlier drafts*: the
Kuipers patent describes a **nutating** field (a DC signal on one coil plus an
AC-modulated carrier on the others), *not* a clean continuous-AC scheme — the
continuous-AC quasi-static dipole formulation was the **1979 Raab et al.**
academic contribution (§1.5). The full priority chain is developed in the patent
genealogy of Chapter 2. (conf: high — patent verified.)

The key physical limitation of AC excitation, recognized early, is its
**sensitivity to eddy currents**: a continuously varying magnetic field induces
circulating currents in any nearby conductor (a metal table, an instrument, the
fluoroscope's C-arm), and those eddy currents radiate secondary fields that
corrupt the measurement. The magnitude of this effect grows with frequency
(Part II, §6.2). This limitation directly motivated the next architectural
branch.

## 1.5 The 1979 Raab et al. formalization

The Raab et al. paper [@raab1979] did three things that defined the field:

1. **It posed the problem precisely.** Three-axis generation and three-axis
   sensing of *quasi-static magnetic-dipole fields* provide information
   sufficient to determine both the position and the orientation of the sensor
   relative to the source. This "three-axis source / three-axis sensor"
   architecture remains the template for the majority of 6-DOF systems today.

2. **It gave a tractable solution algorithm.** Rather than blindly inverting a
   highly nonlinear system, the authors applied **linear rotation
   transformations based on the previous measurement** to both the source
   excitation and the sensor output vectors, producing quantities *linearly*
   proportional to small changes in position and orientation. These increments
   are then separated by linear combinations, transformed to the desired
   coordinate frame, and used to update the prior estimate — a
   predictor/corrector structure that anticipates the modern recursive
   estimators of Part VII. (conf: high — this is the explicit method described
   in the paper's abstract and body.)

3. **It established the quasi-static (near-field) regime** as the operating
   domain: the working volume is small compared with a wavelength, so radiation
   and retardation are negligible and the field is well approximated by a static
   magnetic dipole that simply varies slowly in time. Part II, Chapter 4 derives
   this regime and its limits.

A useful pedagogical point: the 1979 paper is *aerospace*-framed, but every
modern *medical* tracker is a direct descendant of its mathematics. The physics
did not change when the application moved from cockpit to catheter lab — only
the working volume, the coil sizes, and the distortion environment did.

## 1.6 Ascension Technology and pulsed-DC tracking

**Ernest B. Blood** — a co-author of the 1979 paper [@raab1979] — co-founded
**Ascension Technology Corporation** (with Jack Scully, 1986, Vermont, USA)
[@ascension_roper2012] and is closely associated with the second great
architectural idea in EMT: **pulsed-DC (transient) magnetic tracking**, patented
in Blood's US 4,945,305 (1990, "…in the presence of metals…", Ch. 2 §2.1)
[@blood1990]. Instead of continuous sinusoidal excitation,
each transmitter axis is energized with a *DC pulse*; the system then **waits**
for the transient eddy currents in surrounding conductors to **decay** before
sampling the (now eddy-current-free) static field at the sensor (conf: high — the
pulsed-DC eddy-current-settling rationale is standard and described in the review
literature [@franz2014]). Because the measurement is taken after the conductive
transients have died away, pulsed-DC systems are substantially less sensitive to
**non-ferromagnetic conductive** distortion than AC systems — at the cost of
needing magnetometer-type sensors that respond to (quasi-)static fields and of a
different noise/bandwidth trade. Ascension's product lines (e.g., the *Bird*,
*microBIRD*, *trakSTAR*/*driveBAY* families) became reference systems in both
research and OEM medical integration. (conf: med — product naming from vendor and
secondary literature; the *microBIRD* with dipole transmitter is among the
systems characterized by the Hummel assessment protocol [@hummel2005].)

The **AC-vs-pulsed-DC dichotomy** — continuous excitation with synchronous
detection and eddy-current sensitivity, versus pulsed excitation with transient
settling and ferromagnetic (but reduced conductive) sensitivity — is the single
most important architectural fork in EMT history and is analyzed physically in
Chapter 6 and architecturally in Chapter 8.

## 1.7 Northern Digital (NDI) Aurora and medical-grade EMT

**Northern Digital Inc. (NDI)** of Waterloo, Canada — already established in
*optical* surgical navigation with its Polaris systems — introduced the
**Aurora** electromagnetic tracking system aimed squarely at *medical* use:
small (sub-millimeter-diameter) sensor coils suitable for integration into
catheters, needles, and flexible endoscopes, with a field generator and system
electronics engineered for the operating-room environment. The Aurora became one
of the most widely used research and OEM EMT platforms and is one of the two
systems (with the Ascension microBIRD) used to establish the **Hummel
standardized assessment protocol** [@hummel2005], which reported sub-millimeter
to ~1 mm position error and sub-0.2 mm positional jitter under controlled
laboratory conditions (conf: med — these figures are condition-dependent; see
§1.11 and Chapter 28 for the caveats on comparing vendor and laboratory numbers).

## 1.8 Biosense / CARTO and the electrophysiology breakthrough

The application that turned EMT from a niche aerospace/VR technology into a
high-value medical industry was **cardiac electrophysiology (EP)**. In 1997,
**Lior Gepstein, Gal Hayam, and Shlomo A. Ben-Haim** published in *Circulation*
a "novel method for nonfluoroscopic catheter-based electroanatomical mapping of
the heart," using a locatable catheter with a miniature **passive magnetic field
sensor**, an external low-field emitter ("location pad"), and a processing unit —
the system that became commercialized as **CARTO** by **Biosense** (later
Biosense Webster, a Johnson & Johnson company) [@gepstein1997]. The clinical
significance was profound: it allowed electrophysiologists to build a 3-D map of
a heart chamber, color-coded with electrical activation, and to navigate an
ablation catheter to arrhythmia substrates **without continuous fluoroscopy**,
reducing ionizing-radiation exposure to patient and staff. (conf: high — the
nonfluoroscopic, 6-DOF magnetic basis and in vitro/in vivo accuracy validation
are stated explicitly in the paper [@gepstein1997].)

CARTO and its competitors (St. Jude/Abbott **EnSite**, which uses a different —
partly impedance-based — localization principle; Boston Scientific **Rhythmia**)
are surveyed in Chapter 28; the clinical workflows in Chapter 29.

## 1.9 Industrial, VR/AR, and motion-capture adoption

In parallel with the medical trajectory, AC magnetic trackers (Polhemus,
Ascension) became staples of **virtual reality, head tracking, biomechanics, and
motion capture** through the 1990s and 2000s, precisely because they delivered
low-latency 6-DOF without line of sight in laboratory-scale volumes. This market
drove miniaturization and update-rate improvements that later fed back into
medical products. (conf: med — broadly documented across the VR and biomechanics
literature; specific product-by-product adoption is developed in Chapter 28.)

## 1.10 Commercial evolution & consolidation (timeline)

A compressed timeline (the full, sourced version is Chapter 3 §3.3):

- **1969** — Polhemus founded [@polhemus_history]. (conf: med)
- **1975** — Kuipers patent (US 3,868,565), the AC-lineage IP root [@kuipers1975].
  (conf: high)
- **1979** — Raab et al. formalize 6-DOF magnetic dipole tracking [@raab1979].
  (conf: high)
- **1986** — Ascension founded (Scully & Blood) [@ascension_roper2012]. (conf: med)
- **1990** — Blood patent (US 4,945,305), pulsed-DC "in the presence of metals"
  [@blood1990]. (conf: high)
- **1997** — Gepstein/Ben-Haim nonfluoroscopic electroanatomical mapping;
  basis of CARTO; J&J acquires Biosense [@gepstein1997; @globes_jnj_biosense].
  (conf: high / med)
- **early 2000s** — NDI Aurora brings medical-grade EMT to broad OEM/research
  use [@ndi_history]. (conf: med)
- **2005** — Hummel standardized assessment protocol enables apples-to-apples
  accuracy comparison [@hummel2005]. (conf: high)
- **2011–12** — Roper acquires NDI; NDI acquires Ascension
  [@ascension_roper2012]. (conf: med)
- **2012** — superDimension electromagnetic navigation bronchoscopy acquired by
  Covidien (→ Medtronic 2015) [@covidien_superdimension2012]. (conf: med)
- **2014** — Franz et al. consolidate the field in the definitive medical EMT
  review [@franz2014]. (conf: high)

## 1.11 Key researchers, institutions, and a note on performance claims

**People.** F. H. Raab (system theory, also prolific in RF power-amplifier
theory); E. B. Blood (AC and pulsed-DC, Ascension); Jack Kuipers (the nutating-
field US 3,868,565, the AC-lineage root, Ch. 2 [@kuipers1975]); S. Ben-Haim and
L. Gepstein (clinical EP / CARTO);
W. Birkfellner, K. Cleary, T. M. Peters, L. Maier-Hein, J. Hummel, T. Haidegger
(medical EMT validation and review) [@franz2014; @hummel2005].

**Institutions.** Polhemus; Ascension Technology; Northern Digital (NDI);
Biosense Webster (J&J); plus academic centers active in EMT validation
(Medical University of Vienna; Robarts Research Institute / Western University;
and others surveyed in Chapter 30).

**A standing caution on performance numbers.** Throughout this book, accuracy
figures are meaningless without their measurement conditions: working volume,
distance from the generator, proximity to conductors/ferromagnetics, dynamic vs.
static measurement, and whether the number is RMS error, jitter, or
peak-to-peak. Vendor datasheets and laboratory assessments often differ by
large factors for exactly these reasons. We therefore prefer numbers from
**standardized protocols** [@hummel2005] and independent reviews [@franz2014],
and we tag every figure with its conditions and a confidence level. This
discipline is developed formally in Part IX (error budgets) and Chapter 28
(cross-vendor comparison).

---

## Open questions / to verify (gating VERIFIED status)
- ✅ **Resolved:** patent numbers/inventors (Kuipers US 3,868,565; Blood
  US 4,945,305; Ben-Haim US 5,391,199) and the SPASYN/nutating-field attribution
  are verified in Ch. 2 §2.1; founding years (Polhemus 1969, Ascension 1986) and
  acquisition timeline (Roper/NDI 2011–12, Covidien/Medtronic 2012/2015) in
  Ch. 3/28. Remaining: **priority (filing) dates** vs. issue dates for precedence.
- Aurora first-release year and first medical 510(k) clearance date (single-source).
- Confirm Hummel (2005) *Medical Physics* volume/issue/pages (32(7):2371–2379)
  and Raab (1979) DOI against the publisher records.

## Sources cited in this chapter
- [@raab1979] Raab, Blood, Steiner, Jones (1979), *IEEE T-AES* — verified.
- [@kuipers1975; @blood1990] foundational AC/pulsed-DC patents (Ch. 2).
- [@franz2014] Franz et al. (2014), *IEEE T-MI* 33(8):1702–1725 — verified.
- [@hummel2005] Hummel et al. (2005), *Medical Physics* — DOI verified.
- [@gepstein1997] Gepstein, Hayam, Ben-Haim (1997), *Circulation* 95(6) — verified.
- [@polhemus_history; @polhemus_tech; @ascension_roper2012; @ndi_history;
  @globes_jnj_biosense; @covidien_superdimension2012] corporate history/dates
  (vendor/trade-press, conf: med).
