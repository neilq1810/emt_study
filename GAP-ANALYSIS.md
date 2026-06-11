# Definitive-Reference Gap Analysis & Review

> **Posture:** hostile/constructive peer review simulating a 20-seat expert board
> (system architects, sensor physicists, electromagnetics & estimation researchers,
> AFE/DSP designers, medical-device & regulatory engineers, interventional
> cardiologists, EP/bronchoscopy/robotics clinicians, calibration/manufacturing/
> reliability engineers, patent analysts, historians, founders, CTOs, academics).
> **Verdict gate:** the manuscript is *not yet definitive* until the Tier-1
> omissions are closed. Audited state: 37 chapters, 18 parts, ~66k words.
> The actionable, tiered closure plan derived from this lives in
> [`ROADMAP.md`](ROADMAP.md) under "Gap-closure plan."

The core engineering spine (Parts II–X) is strong and unusually quantitative. The
blocking problem is structural: **the manuscript models EMT as an absolute
measurement in the generator frame, whereas clinical/industrial EMT is a
differential, reference-compensated, registered, motion-gated measurement.** An
entire half of the deployed system is missing.

---

## SECTION C — Most dangerous omissions (ranked)

- **C1. Patient reference sensor & differential tracking — ABSENT (0 occurrences).**
  Every fielded clinical system (CARTO, EnSite, Rhythmia, superDimension, Aurora
  navigation) reports tool pose **relative to a patient-mounted reference**, making
  EMT a differential measurement that rejects patient/table motion and slow drift as
  common-mode. The book is single-frame absolute throughout. *Missing pillar.*
- **C2. Respiratory & cardiac gating / motion models — ABSENT.** The dominant
  *dynamic* clinical error (motion between imaging and action) is unmodeled.
- **C3. Registration methods & target-registration-error theory — ABSENT.**
  Registration appears only as an error magnitude; no paired-point/surface/ICP/
  deformable methods, no Fitzpatrick FLE→FRE→TRE theory (incl. FRE⊥TRE),
  no fiducial-configuration optimization. Plausibly the largest clinical error, with
  zero methodology.
- **C4. Metal *inside* the patient (implants, catheters, EMI with pacemakers/ICDs)
  — ABSENT.** Contradicts the book's "keep distorters out" doctrine; these sit at
  d_s→0 (the catastrophic case of eq. 6.4) and cannot be removed.
- **C5. Wireless resonant LC transponder tracking (Calypso-class) — ABSENT as a
  category.** A major FDA-cleared, wireless EM-tracking modality; its absence makes
  the EMT taxonomy incomplete (also backscatter/RFID-style).
- **C6. Reliability engineering — ABSENT (FMEA, FIT/MTBF, fault tree, single-fault,
  burn-in: 0).** Hard gap for a safety-critical device.
- **C7. The manuscript ships its own unverified claims** — dozens of self-flagged
  `(conf: med)`, "to-confirm," and "illustrative" items (mr_capsule authorship,
  corporate dates/$ figures, the Ch. 31/33/34/37 worked budgets). A definitive
  reference cannot contain author-flagged unverified citations and placeholder
  numbers.

## SECTION A — Top 50 missing / chapter-worthy under-developed chapters

**Tier 1 — blocking**
1. Patient Reference Sensor & Differential Tracking Architecture
2. Patient-Motion, Respiratory & Cardiac Gating; Motion Models
3. Registration: Algorithms (paired-point, surface/ICP, deformable)
4. Target-Registration-Error Theory (Fitzpatrick FLE/FRE/TRE; fiducial design)
5. Distortion from Metal Inside the Patient (implants, catheters, pacemaker/ICD EMI)
6. Wireless & Passive Tracking: Resonant LC Transponders (Calypso), backscatter, FM
7. Coordinate-Frame Management & the System Transform Graph
8. Reliability Engineering for EMT (FMEA, FIT/MTBF, fault trees, single-fault)
9. Risk Management (ISO 14971) Applied to EMT
10. Human Factors & Usability Engineering (IEC 62366)

**Tier 2 — needed for definitive**
11. Planar/Under-Table Field Generator design & calibration (expand Ch. 9)
12. Multi-Tool / Simultaneous Multi-Catheter Tracking
13. Full 6-DOF Fisher Information & Orientation CRLB (expand Ch. 24)
14. Nonlinear Observability (Lie/Hermann–Krener) & dipole hemisphere/parity ambiguity
15. Production Test & End-of-Line Manufacturing (distinct from calibration)
16. Factory Calibration at Scale, Golden Units, Cal-Transfer & Traceability
17. Sterilization, Biocompatibility, Encapsulation & Single-Use Sensor Engineering
18. Catheter/Cable/Connector Reliability & Intermittency
19. Installation, Site Survey & Per-Room Environmental Characterization
20. Service, Field QA, Daily Verification & Drift Procedures
21. Post-Market Surveillance, Complaints, Vigilance & Recalls
22. Supply Chain, Component Obsolescence & Second-Sourcing
23. Cost, BOM, Unit Economics & Design-to-Cost
24. Cybersecurity for Networked Trackers (IEC 81001-5-1) — expand
25. V&V Master Plan; Design Controls (ISO 13485 / 21 CFR 820)
26. Regulatory Pathways in Depth (510(k)/De Novo/PMA; EU MDR/GSPR)
27. Clinical Evaluation, Preclinical (phantom/cadaver/animal) & Study Design
28. Deep-Learning Localization & Calibration (end-to-end, PINN, differentiable fields)
29. Magnetic Actuation + Tracking (Stereotaxis, magnetic capsule robots)
30. EM–Optical–Robot–Imaging Multi-Modal Fusion in Depth (expand Ch. 21)
31. Field Generator Thermal & Power-Electronics Co-Design (expand Ch. 9/37)
32. Tracking-Volume Extension & Multi-Generator Handoff
33. Cross-Modality Time Sync & Clock Domains in Clinical Integration
34. Uncertainty Communication & Navigation-Confidence Display
35. EMT in MRI / Hybrid OR / Image-Guided Radiotherapy
36. Pediatric, Bariatric & Deep-Volume Tracking Constraints
37. Standards Landscape & a Proposed Dynamic/Distortion Benchmark (extend Hummel)

**Tier 3 — completeness**
38. Inverse-Problem Global-Solution Theory (uniqueness, basins, multi-start)
39. Stochastic/Spatial Models of Distortion Fields (Gaussian-process field error)
40. Sensor Microfabrication, MEMS coils, PCB/thin-film, assembly tolerances
41. AFE Self-Test, Built-In-Test & In-Situ Health Monitoring
42. Data Logging, Black-Box Recording & Forensic Reconstruction
43. IP Strategy & Freedom-to-Operate (beyond genealogy Ch. 2)
44. Competitive Teardowns & Reverse-Engineering
45. Procedure-Specific Requirements Catalog (EP/ENB/ENT/IR/spine/robotics)
46. Training, Credentialing & Learning-Curve Effects
47. Sensor & System Aging, Lifetime & Multi-Year Drift
48. Environmental & Mechanical Qualification (shock/vibration/thermal/home-use)
49. Magnetic Field Safety & Exposure Limits (ICNIRP/IEEE C95.1)
50. Worked, *Verified*, End-to-End Reference Design with Measured Data (upgrade Ch. 31)

## SECTION B — Top 100 missing subtopics (grouped, prioritized)

- **Physics/fields:** front-back dipole ambiguity & disambiguation; near-field
  reactive/radiative boundary vs actual f; tissue µ≈µ₀ justification w/ citation;
  tissue conductivity dispersion at kHz; solid- vs spherical-harmonic field models &
  truncation conditioning; reciprocity limits under sensor loading; transmitter-coil
  mutual coupling; cored-generator nonlinearity/hysteresis; field-gradient methods;
  full rotating/nutating decode math; analytic 5/6-DOF closed forms (Paperno,
  Schneider); OR-table image theory; layered-conductor eddy fields; high-µ core
  saturation.
- **Sensors:** self-heating; microphonic transfer fn; PCB-coil reproducibility
  statistics; ferrite-grade temp curves; potting-stress drift; cross-axis matrix
  cal; orthogonality tolerance budget; TMR set/reset transients in AC; flux-
  concentrator design; strain relief; min detectable moment vs volume; 3-axis
  co-location error; aging/remanence; sterilization-induced parameter shift.
- **AFE/power:** input-protection vs noise; ESD/defib survival; MUX charge injection
  (TDM); reference-band PSRR curves; chopper residual ripple; ground-loop
  quantification; shield-termination strategy; current-sense noise for ratiometric;
  class-D spur planning vs FDM grid; transformer interwinding capacitance/CM noise;
  Q stability vs temperature; drive-amp SOA into reactive load.
- **DSP/estimation:** orientation CRLB & pose covariance cross-terms; nonlinear
  observability proof; multi-start global solver & basin maps; robust estimation
  under non-Gaussian distortion; innovation-gating tuning theory; IMM motion models;
  RTS smoothing; latency-optimal prediction; FDM crosstalk cancellation; Hadamard/CDM
  decode SNR proofs; adaptive integration-time control; jitter→phase-error spectral
  model; FIM conditioning near singular poses; finite-window bias; multi-rate fusion
  alignment; NEES/NIS field practice.
- **Calibration:** cal-uncertainty→stated-accuracy propagation; optimal spatial
  sampling; basis selection & regularization; online/self-cal; cal transfer between
  units; temperature-dependent cal; cal-data versioning/integrity; ground-truth-robot
  qualification; cored/planar non-dipole cal; recalibration-trigger detection.
- **Clinical:** reference-patch placement & motion; respiratory gating workflows;
  CT-to-body divergence (ENB); wrong-breathing-phase failure; contact-force vs
  localization (EP); multi-catheter EP workflow; fluoro-dose evidence depth; setup
  time/drape/sterility; implant/EMI interactions; pediatric/bariatric limits;
  navigation-confidence display & trust; automation-bias/over-trust; learning curve &
  operator variability; at-table failure recovery.
- **Manufacturing/industry:** yield drivers & test coverage; golden-unit strategy;
  ICT/flying-probe/functional test; burn-in & infant mortality; connector mating-cycle
  life; cable flex-life; lot traceability; DfM for coil winding; cost-of-quality;
  obsolescence/last-time-buy.
- **Regulatory/quality:** ISO 14971 hazard catalog; IEC 62366 use-error analysis;
  essential-performance test methods; predicate/substantial-equivalence argument; EU
  MDR clinical evaluation & PMCF; cybersecurity SBOM/threat model; SOUP dossier; DHF
  structure; complaint/MDR vigilance; standards cross-map matrix.

## SECTION D — Topics likely to draw expert criticism
"Definitive" without reference-sensor differential tracking; position-only CRLB
beside 6-DOF claims; distortion doctrine assuming removable distorters; vendor/
clinical numbers still single-source `conf: med`; illustrative worked budgets in a
quantitative book; pulsed-DC eq. 27.1 unquantified O(1) prefactor; Hummel-as-standard
without a dynamic/distortion standard; Calypso/transponder omission; in-chapter
open-questions reading as unfinished; bolt-on Parts XV–XVIII lacking an integrating
pass.

## SECTION E — Deeper mathematics required
Full 6-DOF FIM (position–orientation coupling) & orientation CRLB; nonlinear
observability (Lie/Hermann–Krener); global uniqueness/hemisphere ambiguity; manifold
optimization on SO(3)/SE(3) in the solver; stochastic/GP distortion-field models;
phase-noise→pose-error spectral propagation; registration TRE theory & fiducial
optimization; IMM/RTS error analysis; conditioning/regularization of field-model
fits; information-theoretic excitation (code) design.

## SECTION F — More practical engineering required
Reference-sensor + common-mode rejection; multi-tool scaling/bandwidth; connector/
cable flex-life & intermittency; sterilization/encapsulation parameter effects;
production/end-of-line test; per-room install/site survey; built-in-test/field QA;
drive-amp SOA/stability into the tank (ppm/THD budgets); warm-up/drift procedures;
black-box logging.

## SECTION G — More clinical treatment required
Patient reference + gating; registration workflow & breathing-phase failure;
in-patient metal & implant interaction; procedure-specific requirements catalog;
navigation confidence/trust & automation bias; setup/sterility/ergonomics;
pediatric/bariatric/deep-volume; fluoro-dose evidence; learning curve; at-table
failure recovery.

## SECTION H — More historical treatment required
Calypso/Varian transponder lineage; Stereotaxis magnetic navigation; military/DARPA
helmet-tracking & SPASYN depth; AHRS/inertial cross-lineage; standards-development
history; failed/abandoned approaches (folklore); IGS-toolkit provenance; RF/transponder
vs coil bifurcation; doctoral-thesis genealogy; verified M&A dates (retire conf:med).

## SECTION I — More regulatory treatment required
ISO 14971 end-to-end; IEC 62366 usability; FDA pathway strategy; EU MDR GSPR/CER/PMCF;
design controls/DHF/ISO 13485; V&V method catalog w/ acceptance criteria; cybersecurity
dossier (IEC 81001-5-1); post-market surveillance/vigilance/recalls; essential-
performance test methods; standards cross-map matrix (60601 family incl. -1-2/-1-6/-1-11,
62304, 62366, 80001).

## SECTION J — Final verdict
An excellent engineering-physics and DSP text on EMT; **not yet the definitive
reference on EMT systems as built, deployed, regulated, and used.** Three blocking
failures: (1) it models the wrong measurement (absolute, not differential/registered/
gated — C1–C3); (2) its distortion/reliability/safety doctrines are contradicted by
clinical reality and lack reliability/risk/human-factors rigor (C4, C6); (3) it is not
yet internally trustworthy (self-flagged unverified citations and illustrative numbers
— C7). Secondary: missing wireless-transponder & actuation lineages (C5/H),
position-only mathematics where 6-DOF is claimed (E), and an un-run integrating
cross-reference pass over Parts XV–XVIII. **The hard quantitative spine is done; the
gaps are overwhelmingly additive.** Highest-leverage move: the patient-reference /
registration / motion pillar (C1–C3).
