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
| 4     | Figures & visualizations                                 | 🟢 23 figures: 15 computed + 8 schematic; all in gallery + rendered inline |
| 5     | Simulations                                              | 🟡 Suite done (emtrack lib + 18 sims incl. 6-DOF FIM, flag-ROC, twin suite, triangle/square demod, quadrature-distortion signature) |
| 6     | Interactive website (digital textbook + tools)           | ✅ Scaffold + 21 tools; sim↔site linked (/results, /figures); **figures now render inline in chapters** (remark-figures plugin) |
| 7     | Cross-referencing pass                                   | 🟢 §-ref integrity verified (849 §-refs → 349 sections, 0 dangling) + permanent verifier guard |
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

### Part XXIII — Model-Based Engineering & the Digital Twin *(new initiative)*
- [x] Ch. 53 The digital twin: concept & credibility — **DRAFT** (forward vs identified vs
      reconciled twin; why EMT suits a twin — one cheap, differentiable, over-determined
      model serves design/calibration/monitoring; **the credibility problem** — ASME V&V 40
      COU/QOI/model-risk + FDA CM&S guidance; the **"sixth way to fail"** = unvalidated twin;
      credibility ladder). +asme_vv40, fda_cms2023, glaessgen2012
- [x] Ch. 54 The forward twin — **DRAFT** (pose→(mean, Jacobian, **covariance**) map; field fidelity ladder dipole→harmonic surrogate (Ch.7, sim1); differentiability (§30.6); **the noise layer closes gap 2** — σ_B=1nT is a placeholder, the twin composes R from the measured chain (Ch.16/18/25/37); **sim 14: at equal noise power, R's STRUCTURE shifts CRLB 0.076→0.067mm (12%) + anisotropy 30→37**; per-layer credibility). +sim14
- [x] Ch. 55 Twin identification = calibration — **DRAFT** (calibration = fitting the twin's params to known-pose data, eq. 55.1; **identifiability = Ch. 24 observability on the calibration Jacobian** — the gain-product rank-5 degeneracy; **sim 13: ±5% gain errors → 14.9 mm uncalibrated → 0.11 mm calibrated, 132×, identifiable from 1 known pose**; parameter hierarchy + factory amortization answering Ch. 50 §50.2; differentiable/PINN inverse; held-out validation per Ch. 53). +sim13, ch55 figure
- [x] Ch. 56 The environment twin & distortion — **DRAFT** (θ_env = the uncontrolled, time-varying room parameter; per-room identification = Ch.52 §52.1 install; **divergence-as-flag** unifies detect-and-flag/fault detection; **sim 15: the §33.9 blind spot closed by a witness sensor — tracked residual margin -0.23% → witness +0.07%, flags first**; dynamic C-arm track-vs-flag; least-credible layer). +sim15
- [x] Ch. 57 The system twin & twin-in-the-loop V&V — **DRAFT** (compose registration/motion/sync → TARGET uncertainty; **sim 16: tracker = 0.2% of target-error variance, registration+motion = 93%, σ_target 1.87mm vs 0.086mm tracker** — 'built the tracker not the system' quantified; twin as evidence engine — in-silico V&V/fault-injection/V&V-40 in-silico evidence; **Part synthesis scorecard** gaps 1/2/4 closed-as-method, 5 partial, 3 not). +sim16

> **Digital-twin Part COMPLETE (Ch. 53–57).** Emerged from the "5 of 10 companies fail" gap analysis:
> the twin is the **integrative methodology** that converts the book's *understanding* into
> a build → calibrate → validate → monitor workflow, closing (as *method*, not values) the
> calibration, noise-floor, and in-situ-distortion gaps and partially the system-integration
> gap. Ch. 53 is the proof-of-concept opener; Ch. 54–57 are scoped, not yet drafted.

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

- [x] **T1.1** Patient Reference Sensor & Differential Tracking Architecture *(Part XIX, Ch. 38)* — 🟢 DEEPENED: differential transform eq. 38.1; common-mode rejection proof eq. 38.2; differential covariance eq. 38.3 (reference adds noise; gradiometer distortion cancellation); reference placement; global silent failure modes; amended clinical accuracy chain. +borgert2006 cite. **[done]**
- [x] **T1.2** Registration: Algorithms (paired-point, surface/ICP, deformable) *(Part XIX, Ch. 40)* — 🟢 DEEPENED: taxonomy by available data; paired-point Procrustes SVD eq. 40.1 (Arun) + reflection/scale fix (Umeyama) + quaternion form (Horn); ICP (Besl–McKay, local/init); deformable (TPS/FFD/FEM, overfitting); robustness (RANSAC/Huber for the silent bad correspondence); EMT workflow & failure modes; weighted Procrustes for anisotropic FLE. +arun1987/horn1987/umeyama1991/beslmckay1992. **[done]**
- [x] **T1.3** Target-Registration-Error Theory (Fitzpatrick FLE/FRE/TRE; FRE⊥TRE; fiducial-config optimization) *(Part XIX, Ch. 39)* — 🟢 DEEPENED: FLE/FRE/TRE distinction; TRE formula eq. 39.1; ⟨FRE²⟩=FLE²(1−2/N); the FRE⊥TRE result; anisotropic/spatially-varying EMT FLE; superficial-fiducial/deep-target geometry; worked ENB TRE 2.3 mm vs FRE 1.06 mm. +fitzpatrick1998/2009. **[done]**
- [x] **T1.4** Patient-Motion, Respiratory & Cardiac Gating; Motion Models *(Part XIX, Ch. 41)* — 🟢 DEEPENED: target-relative (not bulk) motion the reference can't reach; respiratory vs cardiac; 3 strategies (gate / surrogate-correspondence model / 4D); hysteresis + drift failure modes; ECG-gating in EP; prediction under latency; worked budget 20 mm → 2–5 mm (σ_motion was the missing dominant term). +borgert2006/mcclelland2013/keall2006. **[done]**
- [x] **T1.5** Distortion from Metal *Inside* the Patient — implants, catheters, pacemaker/ICD EMI *(Part XIX, Ch. 42; ties Ch. 6/27)* — 🟢 DEEPENED: doctrine breakdown (eq. 42.1 ~(a/d_s)³ at d_s→0); taxonomy (passive implants / instrument self-metal / other tools / active devices); static-vs-moving + registered-static-distortion; **catheter-braid self-distortion** (order-unity → engineer not compensate); **active implants bidirectional** (ICD can ~20% distortion + EMT→CIED EMI per IEC 60601-1-2); CT metal-artifact irony (hurts FLE too); detect-bound-flag-primary hierarchy; spine-screw self-defeating case. +tiikkaja2013. **[done]**
- [x] **T1.6** Wireless & Passive Tracking: Resonant LC Transponders (Calypso), backscatter, FM *(Part XXI, Ch. 47)* — 🟢 DEEPENED: passive LC transponder principle (excite→ring-down→re-radiate, dipole inverse from external array via reciprocity); resonant freq/time-selective clutter rejection (ring-down τ~Q/πf₀ vs eddy settling); Calypso (3 beacons, 10 Hz, ~1–2 mm, radiotherapy); active-vs-passive-vs-backscatter; physics-already-here (Ch.5/6/19/23/27.7); reliability win (no wire/connector, Ch.44) vs 1/d⁶ signal cost & position-only. +balter2005/willoughby2006. **[done — TIER 1 COMPLETE]**
- [x] **T1.7** Coordinate-Frame Management & the System Transform Graph *(Part XIX, Ch. 43; ties Ch. 35)* — 🟢 DEEPENED: the frame zoo (G/T/tip/R/I/Rob/D); transform graph + path composition eq. 43.1 (tip→T→G→R→I); per-edge source/rate/uncertainty table; convention traps (Hamilton/JPL, LPS/RAS, active/passive, time); single-owned-source + tf pattern; SE(3) uncertainty propagation = the clinical accuracy chain (lever-arm amplification, weakest-edge dominance), worked 2.3 mm path; silent-global frame failure modes (flag-never-fabricate). Reuses sola2017/groves2013. **[done — Part XIX complete]**
- [x] **T1.8** Reliability Engineering (FMEA, FIT/MTBF, fault trees, single-fault, burn-in) *(Part XX, Ch. 44)* — 🟢 DEEPENED: EMT failure landscape (connectors/cables #1, fine coil, generator); bathtub/FIT/MTBF; FMEA/FMECA (IEC 60812) + FTA + single-fault (IEC 60601-1); **the silent-partial-failure reframing → detection coverage** eq. 44.1 λ(1−DC) (IEC 61508 DC/SFF; detect-and-flag = the reliability strategy); life-testing/burn-in; availability/maintainability via self-health. +iec60812/iec61508. **[done]**
- [x] **T1.9** Risk Management (ISO 14971) Applied to EMT *(Part XX, Ch. 45; ties Ch. 17/29/35/44)* — 🟢 DEEPENED: harm-based risk (hazard→hazardous-situation→harm sequences); EMT hazard table (undetected pose error = master hazard); control hierarchy (inherently-safe > protective > labeling-last, "can't warn your way out"); **detection coverage = highest-leverage control** (breaks the silent harm-sequence link); benefit-risk + the radiation dividend; the RMF as integrating spine; worked ENB >3mm hazard. +iso14971. **[done]**
- [x] **T1.10** Human Factors & Usability Engineering (IEC 62366) *(Part XX, Ch. 46)* — 🟢 DEEPENED: human-in-the-loop (correct pose can still harm via use error); EMT use-error table (automation bias, mode confusion, accepted mis-registration, missed dropout, alarm fatigue, setup, workaround); **trust calibration** (Parasuraman misuse/disuse; over-trust→wrong-site, under-trust→fluoro/radiation); **display uncertainty not false precision** (error ellipsoid/TRE; detect-and-flag works only if the human perceives it); IEC 62366 process + summative validation; use error = design defect. +iec62366/parasuraman1997. **[done — Part XX complete]**

### Tier 2 — needed for "definitive" (consolidated 27→~18; clustered, sequenced A→F)

**Cluster A — Mathematical rigor** *(do first; retires the estimation-reviewer objection)*
- [x] **T2.3** Full 6-DOF Fisher Information & Orientation CRLB *(Ch. 24 §24.6 + sim10)* — 🟢 DONE: 6×6 FIM blocked; Schur-complement marginalized position CRLB eq. 24.4; **coupling penalty a pose-invariant ≈2.95×** (var ≈8.7×; reported position CRLB IS the honest marginalized value); **orientation CRLB ∝ z³** (0.01–0.15°). +sim10/crlb_6dof.json
- [x] **T2.4** Nonlinear observability (Lie/Hermann–Krener) & dipole hemisphere/parity ambiguity *(Ch. 24 §24.7)* — 🟢 DONE: Hermann–Krener rank condition / Lie derivatives; local-vs-global; **hemisphere/parity ambiguity** (r̂→−r̂ invariance → global un-identifiability) + resolutions (asymmetric generator/half-space prior/continuity/fusion). +hermann1977

**Cluster B — Clinical & safety completers**
- [x] **T2.24** Uncertainty communication & navigation-confidence display *(Ch. 46 §46.6)* — 🟢 DONE: χ²₃,₀.₉₅ ellipsoid/cone on the **orientation-marginalized** §24.6 covariance (optimistic block under-draws ~2.95×), TRE quadrature, τ-relative GREEN/AMBER/RED state; +fda_hf2016, iec60601_1_6
- [x] **T2.16+T2.15** Regulatory pathways & quality systems *(NEW Ch. 48)* — 🟢 DONE: intended-use→classification; US 510(k)/De Novo/PMA; EU MDR GSPR/Rule 11/CER; ISO 13485 + 21 CFR 820/QMSR design controls; **V&V master plan** (design-input→standard→test→acceptance matrix); standards-to-evidence map. +iso13485,cfr820,eu_mdr,fda_510k,fda_denovo
- [x] **T2.17** Clinical evaluation & preclinical study design *(NEW Ch. 49)* — 🟢 DONE: evidence V-model (bench→phantom→cadaver→animal→human→PMCF); preclinical-model trade table; **surrogate-vs-clinical endpoint** (NAVIGATE); GCP study design/powering/bias; navigation-specific pitfalls (GT circularity, surrogate trap, learning curve). +iso14155
- [x] **T2.2** Multi-tool / simultaneous multi-catheter tracking *(Ch. 29 §29.8)* — 🟢 DONE: passive sensors don't contend (one field, many receivers) → cost is channels×compute not signal; active-beacon case → FDM/TDM/CDM (Ch.19); identity/frame management + N-vs-latency trade
- [x] **T2.25** EMT in MRI / hybrid OR / image-guided radiotherapy *(Ch. 29 §29.9)* — 🟢 DONE: MRI bore incompatible (B0 saturation/force, gradient+RF+eddy) → micro-coil tracking instead; hybrid-OR dynamic C-arm distortion; IGRT beam-on motion tracking/gating w/ fail-safe
- [x] **T2.26** Pediatric, bariatric & deep-volume constraints *(Ch. 29 §29.10)* — 🟢 DONE: pediatric (small tools/targets, no-radiation driver); bariatric/deep = z⁴ SNR/conditioning limit (not tissue distortion); mitigations (moment/multi-gen/integration/under-table); usable-volume = region under clinical tolerance

**Cluster C — Industry/operations (consolidated 9→3)**
- [x] **T2.C1** Manufacturing & Production *(NEW Ch. 50)* — 🟢 DONE: end-of-line test layering (functional→parametric→cal→accuracy go/no-go, guard-banded golden fixture, SPC/Cpk); factory cal at scale (amortize volumetric physics → per-unit varying-DOF only; golden-units/cal-transfer/ISO 17025 traceability; on-board cal coeff); design-to-cost (BOM, channel-vs-PDOP, NRE-vs-recurring). +iso17025
- [x] **T2.C2** Mechanical & Sensor Durability *(NEW Ch. 51)* — 🟢 DONE: sterilization (EO/radiation/steam tradeoffs), biocompat (ISO 10993), encapsulation (geometry=calibration → mech drift IS accuracy fault), single-use vs reusable; **connector/cable intermittency = #1 field failure** (µV signals, pass-at-rest/fail-under-flex, silent glitch → detect-and-flag + flex/contact screening). +iso10993,iso11135
- [x] **T2.C3** Deployment & Lifecycle Operations *(NEW Ch. 52)* — 🟢 DONE: install/site-survey + per-room baseline characterization (sets flag thresholds); daily field-QA/drift/scheduled-connector service → availability; post-market surveillance/MDR vigilance (21 CFR 803/EU MDR)/CAPA/recalls/PMCF (highest-N evidence → design loop); supply-chain/obsolescence (2nd-source→re-qual). +cfr803

**Cluster D — Compliance expansions**
- [x] **T2.14** Cybersecurity for networked trackers *(Ch. 35 §35.7)* — 🟢 DONE: security-IS-safety (spoofed pose/tampered cal → patient harm → ISO 14971 file); IEC 81001-5-1 secure lifecycle + FDA §524B/guidance (SBOM/threat model/SPDF mandatory); EMT defense-in-depth (authenticate pose stream + cal integrity; detect-and-flag as security control). +iec81001_5_1,fda_cyber2023
- [x] **T2.27** Standards landscape & proposed dynamic/distortion benchmark *(Ch. 33 §33.4/§33.9)* — 🟢 DONE: landscape (Hummel/ASTM F2554/ISO5725/GUM all STATIC); **proposed benchmark** (standardized trajectory+moving distorter+GT) whose decisive metric is **detect-and-flag latency/false-alarm ROC** — converts the load-bearing safety control from asserted to measured. +astm_f2554

**Cluster E — Engineering-depth expansions** *(cheap; fold into parents)*
- [x] **T2.1** Planar/under-table field generator *(Ch. 9 §9.7)* — 🟢 DONE: distributed coil board under-table (out of sterile field); harmonic-synthesized shaping; mapped/calibrated forward model (Ch.7/26); **asymmetry breaks the §24.7 hemisphere ambiguity for free** + shorter range improves z⁴ CRLB
- [x] **T2.21** Generator thermal & power co-design *(Ch. 37 §37.5)* — 🟢 DONE: moment is THERMALLY capped (P∝I² vs B∝I; patient-contact temp IEC 60601-1); duty/conductor/heat-sink levers; thermal drift IS a calibration/accuracy term; can't brute-force deep volume → multi-generator
- [x] **T2.23** Cross-modality time sync & clock domains *(Ch. 10 §10.6)* — 🟢 DONE: per-device clocks; skew error v·Δt (10ms→0.5–2mm = millimetre-class); timestamp-at-source, PTP/1588/hardware-trigger, latency calibration, async/out-of-sequence fusion
- [x] **T2.20** Multi-modal fusion in depth *(Ch. 21 §21.9)* — 🟢 DONE: complementary failure modes table (EM no-LoS/distortion vs optical LoS/distortion-immune vs IMU drift vs robot flex vs imaging); fusion resolves BOTH 5-DOF roll null (§24.1) AND hemisphere ambiguity (§24.7); integrated navigator (groves) + honest fused covariance → §46.6 display
- [x] **T2.22** Tracking-volume extension & multi-generator handoff *(Ch. 9 §9.8)* — 🟢 DONE: tile overlapping generators; common-frame inter-gen registration (cross-calibrated in overlap); fuse-through-overlap (lower PDOP) not hard-switch (avoids re-acq); TDM/FDM mutual-interference separation; architectural alt to brute moment

**Cluster F — Frontier** ✅ DONE
- [x] **T2.18** Deep-learning localization & calibration *(Ch. 30 §30.6; Ch. 27 §27.5 link)* — 🟢 DONE: three levels (learned cal-map → end-to-end regression black-box → **PINN/differentiable-field hybrids**); the honest direction = learn the residual on a differentiable physics model & preserve covariance/detect-and-flag, not opaque regression. +raissi2019
- [x] **T2.19** Magnetic actuation + tracking *(Ch. 30 §30.7)* — 🟢 DONE: one field actuates (τ=m×B, F=∇(m·B)) AND localizes; two regimes (tesla actuation field as interference → time-share/spectral-sep; OR sense the actuation magnet = reciprocal MR-array, Ch.14); closed control loop (tracking latency=loop delay, covariance=control uncertainty). +abbott2020

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
- 🟢 **X1 — Credibility/verification pass.** *Largely done.* Built a runnable
  verifier (`scripts/verify_manuscript.py`): citation integrity, figure/data reference
  existence, chapter cross-ref range, placeholder scan, and a curated **sim↔prose number
  contract** — **PASS** (100/100 citations resolve, 0 broken, 0 dangling, 0 placeholders,
  7/7 sim numbers in sync). Web-corroborated and corrected: **mr_capsule** (Wang/Meng/Hu,
  *EMBS'06* pp. 2522–2525, PMID 17946518 — **year fixed 2008→2006**); **birkfellner1998**
  (Med Phys 25(11):2242–2248, DOI 10.1118/1.598425, PMID 9829253; 9-author list fixed);
  and the **Ch. 28 acquisitions** (Roper–NDI Jun 2011, NDI–Ascension 2012, J&J–Biosense
  29 Sep 1997 ~\$400M, Covidien–superDimension ~\$300M 2012, Medtronic–Covidien
  26 Jan 2015 ~\$50B). Confirmed the **Ch. 31/33/34/37 illustrative budgets are honestly
  labeled** (conf-tagged; back-with-sim is X3, not X1). Remaining (minor): Ascension \$19M
  & Biosense-1993 founding (single-source); pulsed-DC eq. 27.1 prefactor; §33.5 metrology
  vendor specs — each appropriately hedged.
- [ ] **X2 — Mathematics-depth upgrades (Section E)** woven into the owning chapters
  (6-DOF FIM, nonlinear observability, TRE theory, manifold solve, GP distortion).
- 🟡 **X3 — Simulation/figure backing.** Done: 6-DOF FIM (sim10), **deep-volume CRLB +
  moment lever** (sim11: σ∝1/m_t, z_max∝m_t^0.25 → 16× moment = 2× depth), **dynamic-
  distortion flag-ROC** (sim12: detection margin geometry-dependent +0.56%…−0.26%, NEGATIVE
  for pose-mimicking distortion → single residual flag necessary-but-not-sufficient). 12 sims,
  9 computed figures, sim↔prose contract at 9 assertions. Remaining: schematic diagrams; more
  figure coverage.
- [ ] **X4 — Consolidation & cross-reference pass (Phase 7).** Integrate Parts
  XV–XX into the narrative; audit every `Ch. X §Y` and `[@key]`; convert in-chapter
  "open questions" from a to-do list into resolved text or a single tracked appendix.

### Front/back matter (✅ added)
- **Reader's Guide** (`part-00-front-matter/`): scope, the 8 reading arcs, role-based reader
  pathways, the computed **dependency map** (`figures/readers_dependency_map.png`,
  `scripts/chapter_graph.py`), conventions, and the methodology/honesty contract.
- **Reference part** (`part-24-reference/`): **Notation** (symbols table), **Glossary**
  (acronyms + terms of art), **Appendix — Derivations** (ENBW [the promised "Appendix C"],
  dipole field, the 4:1:1 eigenstructure, the 6-DOF FIM/Schur marginalization), and
  **Decision Frameworks** (excitation-mode table; standards→evidence quick-reference).

### Planned structural revision (Phase 8 — deliberate, scripted, verifier-guarded)
The 23 parts grew iteratively: 8 are single-chapter, related themes are split across
non-adjacent parts, and one numbering wart exists (wireless **Ch. 47** reads after Ch. 48/49).
**Target: re-home all 57 chapters into 8 thematic Parts and renumber 1→57 monotonically.**
- I Foundations & History (1–3) · II Electromagnetic Theory (4–7) · III The Instrument
  (8–18, 35–37, 47) · IV Signal Processing & Pose Estimation (19–24) · V Accuracy: Errors,
  Calibration & Characterization (25–27, 33–34) · VI The Clinical System (29, 38–43) ·
  VII Product, Dependability & Lifecycle (28, 44–46, 48–52) · VIII Synthesis & Frontiers
  (30–32, 53–57).
- **Why deferred / scripted:** a full renumber touches **~850 §-references** and every
  `Ch. N`; it must be one scripted pass (renumber high→low to avoid double-mapping, update
  filenames + headers + cross-refs + contract assertions + gallery slugs + ROADMAP/REVIEW),
  with `scripts/verify_manuscript.py` as the before/after gate. The lone Ch. 47 wart is
  intrinsic to this reorg (it cannot be fixed "minimally" without the cascade renumber).
- **Done now instead (low-risk):** the front/back matter above, plus the consolidation tables
  (Decision Frameworks). The reorg awaits an explicit go-ahead.

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
