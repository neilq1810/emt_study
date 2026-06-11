# Project Roadmap & Progress Tracker

This document is the single source of truth for *what exists*, *what is in
progress*, and *what remains*. Update it in the same commit as any content
change.

## Execution phases

| Phase | Description                                              | Status        |
|-------|----------------------------------------------------------|---------------|
| 1     | Repository structure + master outline + roadmap          | ✅ Done        |
| 2     | Bibliography & source database (seed → comprehensive)    | 🟡 In progress |
| 3     | Chapter-by-chapter content (Parts I–XIV)                 | ✅ Drafted (review pending) |
| 4     | Figures & visualizations                                 | 🟡 7 computed figures (Ch.4/6/20/24); schematic diagrams pending |
| 5     | Simulations                                              | 🟡 Suite done (emtrack lib + 7 sims incl. eddy/skin-depth) |
| 6     | Interactive website (digital textbook + tools)           | ✅ Scaffold + 21 interactive tools; sim↔site linked (/results, /figures, 6 tools overlay Python data) |
| 7     | Cross-referencing pass                                   | ⬜ Not started |
| 8     | Technical review                                         | ⬜ Not started |
| 9     | Publication-ready version                                | ⬜ Not started |

## Chapter lifecycle

Each chapter carries a status header: `RESEARCH → DRAFT → REVIEWED → VERIFIED`.

- **RESEARCH** — sources gathered, outline of claims drafted.
- **DRAFT** — prose written, citations attached.
- **REVIEWED** — technical correctness, equations, and history checked against
  sources; open questions logged.
- **VERIFIED** — every claim cites a verifiable source; contradictions noted.

## Chapter progress

### Part I — Foundations
- [x] Ch. 1 History of electromagnetic tracking — **DRAFT**
- [x] Ch. 2 Patent genealogy & academic genealogy — **DRAFT**
- [x] Ch. 3 Technology timeline & trees — **DRAFT**

> **ALL prose chapters (Parts I–XIV, Ch. 1–31) now drafted.** Next phases:
> figures (4), simulations (5), website (6), cross-ref (7), technical review (8),
> final (9). Patent refs added: Kuipers 1975, Blood 1990, Ben-Haim 1995.

### Part II — Electromagnetic Theory
- [x] Ch. 4 Maxwell's equations, quasistatics & the magnetic dipole — **DRAFT**
- [x] Ch. 5 Coil coupling, mutual inductance & magnetic moment — **DRAFT**
- [x] Ch. 6 Distortion physics: conductors, ferromagnetics, eddy currents — **DRAFT**
- [x] Ch. 7 Numerical methods (FEA, BEM) & analytical models — **DRAFT**

### Part III — Tracker Architecture
- [x] Ch. 8 System architecture overview — **DRAFT**
- [x] Ch. 9 Field generators & sensor coils — **DRAFT**
- [x] Ch. 10 Timing, clocking, synchronization — **DRAFT**
- [x] Ch. 11 DSP pipeline & estimation — **DRAFT**
- [x] Ch. 12 Latency & real-time constraints — **DRAFT**

> **Parts II and III now fully drafted.** Next: Part IV (sensor engineering,
> incl. the TMR/MR §14.3 treatment), or a Phase-5 simulation pass to back the
> figures these chapters reference.

### Part IV — Sensor Engineering
- [x] Ch. 13 Sensor physics & geometries (induction vs. field sensors; 3/5/6 DOF) — **DRAFT**
- [x] Ch. 14 Construction & technologies — coils + solid-state MR (AMR/GMR/**TMR**
      bridge), Hall, fluxgate, MEMS; sensor-selection matrix — **DRAFT**
- [x] Ch. 15 Manufacturing, tolerance & noise analysis — **DRAFT**

> **Parts II, III, IV now fully drafted** (Part I partial). Next sequential: Part V
> (analog front ends). TMR/MR content (Ch. 14.3) now backed by verified sources
> (Lenz & Edelstein 2006; Davies et al. 2021).

### Part V — Analog Front Ends
- [x] Ch. 16 LNAs, instrumentation amps, noise budgeting — **DRAFT**
- [x] Ch. 17 Filtering, shielding, grounding, EMC, medical-grade power — **DRAFT**

> **Parts II–V now fully drafted** (Part I partial). Next sequential: Part VI
> (Data Conversion, Ch. 18). Standards now in bibliography: IEC 60601-1,
> IEC 60601-1-2; analog reference: Horowitz & Hill.

### Part VI — Data Conversion
- [x] Ch. 18 ADC architectures, ENOB/SNR, sampling & jitter — **DRAFT**

> **Parts II–VI now fully drafted** (Part I partial). Next sequential: Part VII
> (DSP, Ch. 19–22). ADC refs added: Walden 1999, IEEE Std 1241.

> **Parts II–VII now fully drafted** (Part I partial). Next sequential: Part VIII
> (Position Solvers, Ch. 23–24). Refs added: Scofield 1994, Kalman 1960,
> Julier & Uhlmann 2004, Bar-Shalom et al. 2001.

### Part VII — Digital Signal Processing
- [x] Ch. 19 Excitation/multiplexing (FDM/TDM/CDM/orthogonal) — **DRAFT**
- [x] Ch. 20 Lock-in / synchronous detection; matched & adaptive filtering — **DRAFT**
- [x] Ch. 21 Kalman/particle filtering & sensor fusion — **DRAFT**
- [x] Ch. 22 Real-time implementations (FPGA/GPU/embedded) — **DRAFT**

### Part VIII — Position Solvers
- [x] Ch. 23 Inverse problem, LM, MLE, Bayesian — **DRAFT**
- [x] Ch. 24 Observability, conditioning, convergence, uncertainty — **DRAFT**

> **Parts II–VIII now fully drafted** (Part I partial). The full signal chain
> (physics → … → pose + uncertainty) is now continuous. Next sequential: Part IX
> (Error Sources, Ch. 25). Refs added: Marquardt 1963, Kay 1993, Nocedal & Wright 2006.

### Part IX — Error Sources
- [x] Ch. 25 Error taxonomy, budgets, sensitivity matrices, Monte Carlo — **DRAFT**
      (incl. Barkhausen, generator, ambient/EM-susceptibility, TMR bias-reference noise)

> **Parts II–IX now fully drafted** (Part I partial). Next sequential: Part X
> (Calibration, Ch. 26–27). Refs added: Poulin & Amiot 2002, Monteblanco et al. 2021.

### Part X — Calibration
- [x] Ch. 26 Sensor/generator/system calibration & field mapping — **DRAFT**
- [x] Ch. 27 Distortion compensation & ML approaches — **DRAFT**

> **Parts II–X now fully drafted** (Part I partial). Remaining: Part I (Ch. 2–3),
> and Parts XI–XIV (ecosystem, medical, frontiers, build-from-scratch). Refs added:
> Cavaliere & Cantillon-Murphy 2023, Kindratenko & Sherman 2005.

### Part XI — Commercial Ecosystem
- [x] Ch. 28 Vendor survey (Polhemus, Ascension, NDI/Aurora, Biosense/CARTO,
      Abbott EnSite, Boston Sci Rhythmia, superDimension, emerging) — **DRAFT**

> **Parts II–XI now drafted** (Part I partial: Ch.1 done, Ch.2–3 pending). Next
> sequential: Part XII (Medical Applications, Ch. 29). Refs added: Polhemus &
> NDI history, Ascension/Roper, J&J/Biosense, Covidien/superDimension.

### Part XII — Medical Applications
- [x] Ch. 29 EP, bronchoscopy, ENT, IR, robotics, IGT + workflows & regulatory — **DRAFT**

> **Parts II–XII now drafted** (Part I partial). Remaining: Part I (Ch.2–3),
> Part XIII (frontiers, Ch.30), Part XIV (build-from-scratch, Ch.31). Ref added:
> Folch 2019 (NAVIGATE).

### Part XIII — Research Frontiers
- [x] Ch. 30 SOTA, hybrid optical+EM, ML compensation, quantum sensing — **DRAFT**

> **Parts II–XIII now drafted** (Part I partial). Remaining prose: Part I (Ch.2–3),
> Part XIV (build-from-scratch, Ch.31). Refs added: Budker & Romalis 2007,
> Barry et al. 2020.

### Part XIV — Building a System From Scratch
- [x] Ch. 31 End-to-end design worked example — **DRAFT**

### Part XV — Interactive Capstone
- [x] Ch. 32 Interactive system-design lab — **DEEPENED** (web edition embeds four
      live dashboards beneath the prose; manuscript documents each)

### Part XVI — Performance Characterization
- [x] Ch. 33 Performance characterization & benchmarking (system/pair) — **DEEPENED**
      (metrics/figures of merit, trueness-vs-precision, cross-volume/cross-pair
      comparison & eq-8.1 normalization, ground-truth hierarchy, worked rig error
      budget, rig build considerations, reporting honesty)
- [x] Ch. 34 Sensor & component characterization — **DEEPENED** (per-class parameter
      lists coil vs biased; the vendor-data gap; **hysteresis & Barkhausen** as
      un-calibratable floors; reference-field bench & methods; worked reference-field
      budget; FoM→system mapping; coil-vs-TMR on one bench)

### Part XVII — Software, Integration & Deployment
- [x] Ch. 35 Software architecture, integration & lifecycle — **DEEPENED** (software
      stack; pose-engine threading/timestamping/state machine; integration & API
      layer — OpenIGTLink/PLUS/3D Slicer/IGSTK/ROS, pose+covariance contract, frame
      handoff; IEC 62304 lifecycle — safety classes A/B/C, SOUP, V&V, cybersecurity;
      numerical determinism/reproducibility; open-source ecosystem). Cross-refs
      Parts VII–VIII/Ch.22 for algorithms rather than repeating
- [x] Ch. 36 Compute platform & processor selection — **DEEPENED** (selection
      drivers; silicon taxonomy FPGA/SoC/SoM/MCU/DSP/GPU/host; **Cortex-M vs R vs A**
      + AMP; worked stage→silicon mapping & compute budget; RTOS pairing; form-factor/
      power/thermal vs Ch.17 patient-heating; build-vs-buy/lifecycle). Cross-refs
      Ch.22 for implementation techniques

### Part XVIII — Power Architecture & Design
- [x] Ch. 37 Power architecture & design — **DEEPENED** (EMT-specific, not generic:
      system power tree; **generator drive** power — inductive/resonant load,
      spectral-purity = field error, ratiometric & its limit, class-AB vs class-D
      spurs, stability into reactive load, transient settling, current-mode/thermal;
      **low-noise AFE rails** — PSRR/LDO budget, partitioned returns; **remote
      biased-sensor bias/reference tree** — reference-stability = measurement-
      stability, Type-CF isolation, tip self-heating). Cross-refs Ch.9/16/17/25

> **All technical Parts (II–XIV) now drafted.** Remaining prose: Part I Ch.2
> (patent/academic genealogy) & Ch.3 (timelines/trees). Then non-prose phases:
> figures (4), simulations (5), website (6), cross-ref (7), review (8), final (9).

## Gap-closure plan (Definitive-Reference Review)

Derived from the hostile expert-board gap analysis in
[`GAP-ANALYSIS.md`](GAP-ANALYSIS.md). The book's quantitative spine (Parts II–X)
is strong; the gaps are **additive**. We work **tier by tier**. Each item lists a
**proposed placement** (new Part letter, or "expand Ch. X"); final chapter numbers
are assigned when each is created (as for Ch. 32–37). State: ⬜ todo · 🟡 in progress
· 🟢 drafted/deepened · ✅ reviewed.

### Tier 1 — BLOCKING (must close before any "definitive" claim)
The single highest-leverage cluster is the **differential/registration/motion
pillar** (T1.1–T1.4): clinical EMT is a *differential, registered, motion-gated*
measurement and the book currently models only absolute generator-frame tracking.

> Proposed **Part XIX — Differential Tracking, Registration & Motion** (T1.1–T1.5, T1.7)
> and **Part XX — Dependability & Compliance** (T1.8–T1.10).

- [ ] **T1.1** Patient Reference Sensor & Differential Tracking Architecture *(Part XIX)* — common-mode rejection math; reference placement; dropout handling. **[start here]**
- [ ] **T1.2** Registration: Algorithms (paired-point, surface/ICP, deformable) *(Part XIX)*
- [ ] **T1.3** Target-Registration-Error Theory (Fitzpatrick FLE/FRE/TRE; FRE⊥TRE; fiducial-config optimization) *(Part XIX)*
- [ ] **T1.4** Patient-Motion, Respiratory & Cardiac Gating; Motion Models *(Part XIX)*
- [ ] **T1.5** Distortion from Metal *Inside* the Patient — implants, catheters, pacemaker/ICD EMI *(Part XIX; ties Ch. 6/27)*
- [ ] **T1.6** Wireless & Passive Tracking: Resonant LC Transponders (Calypso), backscatter, FM *(new chapter; ties Part IV/XIII)*
- [ ] **T1.7** Coordinate-Frame Management & the System Transform Graph *(Part XIX; ties Ch. 35)*
- [ ] **T1.8** Reliability Engineering (FMEA, FIT/MTBF, fault trees, single-fault, burn-in) *(Part XX)*
- [ ] **T1.9** Risk Management (ISO 14971) Applied to EMT *(Part XX; ties Ch. 17/29/35)*
- [ ] **T1.10** Human Factors & Usability Engineering (IEC 62366) *(Part XX)*

### Tier 2 — needed for "definitive"
- [ ] **T2.1** Planar/Under-Table Field Generator design & calibration *(expand Ch. 9)*
- [ ] **T2.2** Multi-Tool / Simultaneous Multi-Catheter Tracking *(new)*
- [ ] **T2.3** Full 6-DOF Fisher Information & Orientation CRLB *(expand Ch. 24 + 6-DOF sim)*
- [ ] **T2.4** Nonlinear Observability (Lie/Hermann–Krener) & dipole hemisphere/parity ambiguity *(expand Ch. 24)*
- [ ] **T2.5** Production Test & End-of-Line Manufacturing *(new; ties Ch. 15)*
- [ ] **T2.6** Factory Calibration at Scale, Golden Units, Cal-Transfer & Traceability *(expand Ch. 26)*
- [ ] **T2.7** Sterilization, Biocompatibility, Encapsulation & Single-Use Sensors *(new; ties Ch. 14/17)*
- [ ] **T2.8** Catheter/Cable/Connector Reliability & Intermittency *(new; ties T1.8)*
- [ ] **T2.9** Installation, Site Survey & Per-Room Environmental Characterization *(new; ties Ch. 27/33)*
- [ ] **T2.10** Service, Field QA, Daily Verification & Drift Procedures *(new; ties Ch. 26.6)*
- [ ] **T2.11** Post-Market Surveillance, Complaints, Vigilance & Recalls *(Part XX)*
- [ ] **T2.12** Supply Chain, Component Obsolescence & Second-Sourcing *(new; ties Ch. 36)*
- [ ] **T2.13** Cost, BOM, Unit Economics & Design-to-Cost *(new)*
- [ ] **T2.14** Cybersecurity for Networked Trackers (IEC 81001-5-1) *(expand Ch. 35)*
- [ ] **T2.15** V&V Master Plan; Design Controls (ISO 13485 / 21 CFR 820) *(Part XX)*
- [ ] **T2.16** Regulatory Pathways in Depth (510(k)/De Novo/PMA; EU MDR/GSPR) *(Part XX; ties Ch. 29)*
- [ ] **T2.17** Clinical Evaluation, Preclinical (phantom/cadaver/animal) & Study Design *(new; ties Ch. 29/33)*
- [ ] **T2.18** Deep-Learning Localization & Calibration (end-to-end, PINN, differentiable fields) *(expand Ch. 27/30)*
- [ ] **T2.19** Magnetic Actuation + Tracking (Stereotaxis, capsule robots) *(expand Ch. 30)*
- [ ] **T2.20** EM–Optical–Robot–Imaging Multi-Modal Fusion in Depth *(expand Ch. 21)*
- [ ] **T2.21** Field-Generator Thermal & Power-Electronics Co-Design *(expand Ch. 9/37)*
- [ ] **T2.22** Tracking-Volume Extension & Multi-Generator Handoff *(new)*
- [ ] **T2.23** Cross-Modality Time Sync & Clock Domains in Clinical Integration *(expand Ch. 10/35)*
- [ ] **T2.24** Uncertainty Communication & Navigation-Confidence Display *(new; ties Ch. 24/T1.10)*
- [ ] **T2.25** EMT in MRI / Hybrid OR / Image-Guided Radiotherapy *(new)*
- [ ] **T2.26** Pediatric, Bariatric & Deep-Volume Tracking Constraints *(new; ties Ch. 29)*
- [ ] **T2.27** Standards Landscape & a Proposed Dynamic/Distortion Benchmark *(expand Ch. 33; ties Ch. 30)*

### Tier 3 — completeness
- [ ] **T3.1** Inverse-Problem Global-Solution Theory (uniqueness, basins, multi-start) *(expand Ch. 23)*
- [ ] **T3.2** Stochastic/Spatial (GP) Models of Distortion Fields *(expand Ch. 6/27)*
- [ ] **T3.3** Sensor Microfabrication, MEMS coils, PCB/thin-film, assembly tolerances *(expand Ch. 14)*
- [ ] **T3.4** AFE Self-Test, Built-In-Test & In-Situ Health Monitoring *(expand Ch. 16/35)*
- [ ] **T3.5** Data Logging, Black-Box Recording & Forensic Reconstruction *(new; ties Ch. 35)*
- [ ] **T3.6** IP Strategy & Freedom-to-Operate *(expand Ch. 2)*
- [ ] **T3.7** Competitive Teardowns & Reverse-Engineering *(expand Ch. 28)*
- [ ] **T3.8** Procedure-Specific Requirements Catalog (EP/ENB/ENT/IR/spine/robotics) *(expand Ch. 29)*
- [ ] **T3.9** Training, Credentialing & Learning-Curve Effects *(new)*
- [ ] **T3.10** Sensor & System Aging, Lifetime & Multi-Year Drift *(expand Ch. 15/26)*
- [ ] **T3.11** Environmental & Mechanical Qualification (shock/vibration/thermal/home-use) *(new)*
- [ ] **T3.12** Magnetic Field Safety & Exposure Limits (ICNIRP/IEEE C95.1) *(new; ties Ch. 17)*

### Cross-cutting workstreams (not chapters — run alongside the tiers)
- [ ] **X1 — Credibility/verification pass.** Retire every self-flagged
  `(conf: med)`, "to-confirm," and "illustrative" item: verify or remove. Priority:
  mr_capsule authorship; corporate dates/$ figures (Ch. 28/3); pulsed-DC eq. 27.1
  prefactor; the Ch. 31/33/34/37 illustrative budgets (back with sim or measurement).
- [ ] **X2 — Mathematics-depth upgrades (Section E)** woven into the owning chapters
  (6-DOF FIM, nonlinear observability, TRE theory, manifold solve, GP distortion).
- [ ] **X3 — Simulation/figure backing.** Implement the deferred sims (below) +
  a 6-DOF CRLB sim; raise figure coverage (Phase 4) beyond the current 8.
- [ ] **X4 — Consolidation & cross-reference pass (Phase 7).** Integrate Parts
  XV–XX into the narrative; audit every `Ch. X §Y` and `[@key]`; convert in-chapter
  "open questions" from a to-do list into resolved text or a single tracked appendix.

### Recommended working sequence
1. **T1.1 → T1.3 → T1.4** (the differential/registration/motion pillar — the verdict-breaking gap), then **T1.5, T1.7**.
2. **T1.8 → T1.9 → T1.10** (dependability/compliance) + **T1.6** (wireless transponders).
3. **X1 credibility pass** (cheap, high-trust-yield) once Tier 1 lands.
4. Tier 2 by cluster (math T2.3–T2.4; clinical T2.16–T2.17, T2.24–T2.26; industry T2.5–T2.13).
5. **X4 consolidation/cross-ref**, then Tier 3, then Phases 4–9.



Captured from working sessions so they are not lost; none of these are built yet.

1. **Characterization rig — accuracy map & explorer (Ch. 33).** Phase-5 sim of an
   accuracy-vs-position map over the working volume; Phase-6 "characterization
   explorer" tool with a rig-floor calculator (GT ⊕ registration ⊕ thermal vs the
   DUT spec, the 5–10× rule), tying to the CRLB / working-volume tools.
2. **Pulsed-DC settling (Ch. 27 §27.6).** Phase-5 sim of the step-vs-AC eddy
   amplitude for a sphere to pin the eq. 27.1 O(1) prefactor; a "pulsed-DC settling"
   dashboard slider (wait t_s → suppression S = e^(t_s/τ_e) vs update rate).
3. **Transmitter-side sensing (Ch. 27 §27.7).** Phase-5 sim of the reflected-
   impedance signature (eq. 27.2) vs distorter size/distance/material; a toggle in
   the distortion dashboard to show the transmitter-side observable alongside the
   receiver-side error.
4. **Error-budget grounding (Ch. 31 / error-budget dashboard).** Tolerance
   Monte-Carlo + a measured/simulated distortion-residual map to replace the
   illustrative deterministic & environmental columns with sim-backed defaults.
5. **Witness-sensor compensation (Ch. 27).** Interactive demo + Phase-5 sim of
   residual vs. witness count/placement (pre-existing Ch. 27 open item).

## Research quality control

**Citation keys.** In-text citations use `[@key]` where `key` matches an `id`
in `citations/bibliography.json`.

**Confidence tags.** Claims that are not textbook-standard carry an inline
confidence marker:
- `(conf: high)` — multiple independent peer-reviewed/primary sources agree.
- `(conf: med)` — single authoritative source, or vendor-reported.
- `(conf: low)` — inferred, contested, or based on secondary reporting; treat
  as provisional.

**Source-type tags** recorded per bibliography entry: `journal`, `conference`,
`dissertation`, `standard`, `patent`, `regulatory`, `vendor`, `lab`, `gov`.

**Open questions.** Each chapter ends with an "Open questions / to verify"
section. Items there are *not yet* `VERIFIED`.

## Known scope risks / honesty notes
- Many vendor performance numbers are self-reported and measured under
  non-standardized conditions; they are tagged `(conf: med)` or lower and
  cross-checked against independent assessment studies (e.g., Hummel protocol).
- Patent priority dates vs. publication dates are distinguished where known.
- Some early/military history is documented only in secondary sources; flagged.
