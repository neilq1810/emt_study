# Depth & Technical-Review Tracker

Collaborative deepen-and-review pass. Each chapter moves
`DRAFT → DEEPENED → REVIEWED (by user) → VERIFIED`. We are working through
**Part VII–IX (Ch. 19–25) first**, then by agreement.

## Conventions for the deep pass
- Add: full derivations, worked numerical examples (tie to `simulations/` where
  possible), failure-mode boxes, quantitative trade tables, and **new primary
  citations** (searched, not recalled).
- Keep the per-claim `(conf: …)` tags and the per-chapter open-questions list.
- After each chapter: commit, then summarize *what was added / what's uncertain*
  for user review.

## Status

| Ch | Title | State | Notes |
|---:|-------|-------|-------|
| 19 | Excitation & channel separation | 🟢 DEEPENED → review | +Anser FDM, harmonic/IMD crosstalk, Hadamard CDM, worked freq plan, multi-coil scaling, failure-mode box (1015→2376 w) |
| 20 | Synchronous detection & filtering | 🟢 DEEPENED → review | +ENBW derivation, output-SNR/processing-gain, matched-filter/CRLB optimality, reference phase/harmonic/Rician/dynamic-reserve, analog-vs-digital, pulsed-DC matched filter, Widrow adaptive/witness, worked SNR (974→2080 w) |
| 21 | State estimation & fusion | 🟢 DEEPENED → review | +EMT state vector, EKF Jacobian, full UKF sigma points, error-state/MEKF orientation (Solà), particle filter (Arulampalam), EM+IMU error-state fusion, NIS distortion detection, NIS/NEES consistency (1052→1787 w) |
| 22 | Real-time implementations | 🟢 DEEPENED → review | +quantified data-rate funnel, CIC decimation (Hogenauer, bit-growth), CORDIC (Volder), fixed-point word-length, SoC fixed/float split, WCET/fault-injection verification, resource sketch (973→1648 w) |

**Part VII (Ch. 19–22) fully deepened.**

| 23 | Inverse problem (solvers) | 🟢 DEEPENED → review | GN derived, LM trust-region/λ-update, **closed-form initializer derived + numerically verified (eig 1:1:4, machine-precision)**, MAP=KF, SO(3)/constraints, robust M-estimators/IRLS (Huber), basins/rank-deficiency (1107→1915 w) |
| 24 | Conditioning, observability, uncertainty | 🟢 DEEPENED → review | local-vs-global observability, SVD conditioning bound (eq 24.2) + preconditioning, **GNSS dilution-of-precision bridge (Groves)**, fuller CRLB/error-ellipsoid; preserves Phase-5 z^4/Monte-Carlo (→1830 w) |
| 25 | Error taxonomy & budgets | 🟢 DEEPENED → review | +GUM law of propagation (eq 25.1, Type A/B, combined/expanded uncertainty), **worked numeric position budget** (→0.84 mm @95%, top-down allocation), correlation cross-terms (1696→2411 w) |

**✅ Batch complete: Ch. 19–25 (Parts VII–IX) all deepened.** 14 new verified
citations added across the batch (Anser, Widrow, Solà, Arulampalam, Hogenauer,
Volder, Huber, Groves, GUM, …). All build clean (0 KaTeX errors).

### Part II — Electromagnetic Theory (current batch)
| Ch | Title | State | Notes |
|---:|-------|-------|-------|
| 4 | Maxwell, quasistatics & the dipole | 🟢 DEEPENED → review | +oscillating-dipole 3-term expansion (near/induction/radiation), **tissue-transparency quantified** (skin depth ~7 m ≫ body, Gabriel), Jackson/Griffiths added (→1915 w) |
| 5 | Coil coupling & mutual inductance | 🟢 DEEPENED → review | +demagnetizing-factor limit (μ_app→1/D, why catheter coils are long/thin), coupling coefficient k & reflected impedance, open-circuit-vs-loaded voltage divider, reciprocity proof, (5.4)→(5.3) sketch, worked induced-voltage example (0.47 mV–50 µV); Grover added (1268→1895 w) |
| 6 | Distortion physics | 🟢 DEEPENED → review | +ferromagnetic sphere polarizability (eq 6.2), eddy-decay τ_e=μ₀σa²/π² (eq 6.3, worked: 5cm Cu→18ms→11Hz pulsed-DC cap), conducting-sphere AC limits (∝ω then saturate), distortion-fraction scaling a³r³/(d_t³d_s³) (eq 6.4) (→1879 w) |
| 7 | Numerical methods (FEA/BEM) | 🟢 DEEPENED → review | +A-formulation PDE & A-V eddy formulation, Nédélec edge elements, open-boundary (infinite elements/Kelvin/FEM-BEM), **spherical-harmonic online field model (eq 7.1)**, reluctance intermediate, MMS + Phase-5 V&V ties; Jin added (1119→1694 w) |

**✅ Part II (Ch. 4–7) fully deepened.** +6 verified citations (Jackson, Griffiths,
Gabriel, Grover, Jin; Huber/Groves/GUM from prior batch). All build clean.

### Part III — Tracker Architecture (current batch)
| Ch | Title | State | Notes |
|---:|-------|-------|-------|
| 8 | System architecture | 🟢 DEEPENED → review | +architecture parameter space, **system link budget eq 8.1 (master design relation)**, wireless/active-passive/sync architecture, worked architecture selection + commercial mapping (1031→1945 w) |
| 9 | Field generators & sensor coils | 🟢 DEEPENED → review | +coil electrical model (L,R,V,P eq 9.1), worked resonant-drive (500V→2.4V, Q≈210, BW≈48Hz → per-coil FDM freqs), spherical-harmonic field-shaping synthesis, sensor self-resonance (1059→1681 w) |
| 10 | Timing, clocking, sync | 🟢 DEEPENED → review | +quantified sync budget (δφ=ωδt → ~2µs @10kHz; wireless Crowley 2023 1.61mm), coherent-sampling integer-ratio condition, three-distinct-jitters clarification, FDM spacing bounded by 1/τ AND resonant BW (1087→1480 w) |
| 11 | DSP pipeline & estimation | 🟢 DEEPENED → review | +quantified Stage-3 amplification (cube-root near-field, z⁴ edge), **§11.6 covariance-propagation data contract (R_a→R_M→P=CRLB)** incl. calibration-induced correlations, per-stage failure modes; resolved both open Qs (866→1385 w) |
| 12 | Latency & real-time | 🟢 DEEPENED → review | +worked AC/pulsed-DC latency budgets (~8ms vs 12–100ms settling-dependent), **quantitative trilemma worked example** (catheter sensor fails 1mm@100Hz → escapes via moment/noise/volume), group-delay quantification (939→1449 w) |

**✅ Part III (Ch. 8–12) fully deepened.** +2 verified citations (Crowley 2023,
Anser/Grover reused). All build clean.

### Part IV — Sensor Engineering (current batch)
| Ch | Title | State | Notes |
|---:|-------|-------|-------|
| 13 | Sensor physics & geometries | 🟢 DEEPENED → review | exact roll-null derivation (Jacobian null space), **dual-coil 6-DOF roll observability ∝ sin θ — derived + Phase-5 validated (0 / 0.55 / 1.0 at 0/45/90°)**, Schneider patent; new sim9 + figure (→1433 w) |
| 14 | Construction & technologies (TMR) | 🟢 DEEPENED → review | +ferrite demag tie (why catheter coils long/thin), **Hooge 1/f law (bias²/A → constant detectivity)**, **MR-array tracking demo cited (capsule 3.3 mm)** resolving the key open Q, Barkhausen link (→2027 w). NB: mr_capsule authors/venue to re-confirm (search API down) |
| 15 | Manufacturing, tolerance & noise | 🟢 DEEPENED → review | +tolerance→error propagation rules (area→range ÷3, angle→orientation), **worked tolerance→pose table**, **thermal-drift coefficients** (Cu +0.39%/°C, ferrite μ_r, TMR) → recalibration interval (~1.5mm/5°C); resolved both open Qs (1109→1618 w) |

**✅ Part IV (Ch. 13–15) fully deepened.** +Schneider, mr_capsule citations
(mr_capsule authors/venue to re-confirm). Build clean.

### Part V — Analog Front Ends (current batch)
| Ch | Title | State | Notes |
|---:|-------|-------|-------|
| 16 | Amplification & noise budgeting | 🟢 DEEPENED → review | +worked bipolar-vs-JFET noise table (operating vs near-resonance), tuned-pickup option, worked 120 dB gain plan, **§16.6 AC-coil vs biased-sensor AFE (chopper for baseband MR/DC) + forward-ref to Ch.17 safety** (1299→1985 w). NB: NEF-origin (Steyaert-Sansen 1987) to add when search up |
| 17 | Filtering, shielding, EMC, power | 🟢 DEEPENED → review | +MOPP/MOOP, **biased-sensor vs passive-coil patient-power/leakage/heating safety contrast (user-requested)**, OR threat list (ESU/C-arm/defib-proof) (1224→1732 w) |

**✅ Part V (Ch. 16–17) fully deepened.** Build clean.

### Part VI — Data Conversion (current batch)
| Ch | Title | State | Notes |
|---:|-------|-------|-------|
| 18 | ADC systems | 🟢 DEEPENED → review | +NTF/stability/MASH (Schreier-Temes), **worked Σ-Δ plan (1-bit, L=2, OSR 256 → 120 dB/20-bit)**, simultaneous-vs-muxed multi-channel conversion (phase coherence), CIC decimation tie (1333→1651 w) |

**✅✅ TECHNICAL CORE COMPLETE: Parts II–IX (Ch. 4–25) all deepened.**

### Part X — Calibration (current batch)
| Ch | Title | State | Notes |
|---:|-------|-------|-------|
| 26 | Sensor/generator/system calibration | 🟢 DEEPENED → review | +sampling density (h⁻³ cost/h² residual), **spherical-harmonic compact field model (Ch.7 tie)**, bias-variance/overfitting (Phase-6 tool), worked recalibration interval (~1.5mm/5°C) (1015→1350 w) |
| 27 | Distortion compensation | 🟢 DEEPENED → review | +witness-sensor induced-dipole physics & placement (eq 6.4), **unification with Ch.20 adaptive cancellation (Widrow)**, NIS χ² distortion-alarm threshold, compensation reduces ~5-10× not to zero (1091→1446 w). **+§27.6 pulsed-DC source-level rejection, quantified** (suppression S=e^(t_s/τ_e), eq 27.1; worked table 20/150/1100× vs rate; Amdahl asymmetry — 0 dB on ferromagnetic; stacks-with-compensation table; budget-transfer cost) [user-requested]. **+§27.7 transmitter-side sensing** (generator reflected-impedance eq 27.2; conductive/ferro phase discrimination; Jaeger 2018 generator transmit+receive mutual-inductance distorter characterisation; Dumoulin US6201987 drive pre-emphasis; observability limits — global-but-coarse, blind at d_s→0; dual of §27.3) [user-requested]. +2 verified cites (jaeger2018, dumoulin2001) |

**✅ Part X (Ch. 26–27) fully deepened.** Build clean.

### Part I — Foundations (current batch)
| Ch | Title | State | Notes |
|---:|-------|-------|-------|
| 1 | History | 🟢 DEEPENED → review | resolved conf:low SPASYN (Kuipers nutating-field US3868565), firmed founding/acquisition dates from verified Ch.2/3 patents; timeline + sources cleaned (→2275 w) |
| 2 | Patent & academic genealogy | 🟢 DEEPENED → review | already had verified patents; +patent-expiry→open-source IP-cycle note (Kuipers ~1992, Blood ~2010 → Anser/wireless) |
| 3 | Technology timelines & trees | 🟢 DEEPENED → review | already had sourced timeline; +open-source/wireless era rows (Anser 2017, FM-wireless 2023) |

**✅ Part I (Ch. 1–3) fully deepened.**

### Parts XI–XIV — Ecosystem, Medical, Frontiers, Capstone (final batch)
| Ch | Title | State | Notes |
|---:|-------|-------|-------|
| 28 | Vendor survey | 🟢 DEEPENED → review | +"why fuse magnetic with impedance" explainer (absolute-accurate vs scalable-warped, EM+IMU pattern); cross-vendor table tied to system link budget (eq 8.1) + 3 error classes; fixed pre-existing KaTeX \$-amount/J&J bug |
| 29 | Clinical applications & workflows | 🟢 DEEPENED → review | **+clinical-accuracy-chain RSS** σ_clin=√(track²+reg²+tip²+motion²+distort²), worked (1mm tracker behind 2mm reg+0.9mm tip → 2.4mm) → halving tracker barely moves it → attack dominant term |
| 30 | Research frontiers & open problems | 🟢 DEEPENED → review | **+frontier-readiness scorecard** (binding-constraint/maturity/hardest-issue: fusion near-term, quantum far/niche), **+worked quantum dynamic-range mismatch** (~106 dB needed; SERF lacks range+BW not sensitivity) |
| 31 | End-to-end design (capstone) | 🟢 DEEPENED → review | **+SNR number chain** (coil 1.3nV/√Hz → 13nV@100Hz ENBW → σ_B≈0.1–1nT matching CRLB sim); **+worked error budget by class × location** (RSS 0.50/0.62/0.92mm near/mid/far — calib+distortion dominate mid, z⁴ CRLB dominates far); **+worked latency budget** (≈8.7ms, τ dominates, vs 20ms spec) |

**✅ Parts XI–XIV (Ch. 28–31) fully deepened.** Capstone Ch. 31 now carries numbers
end-to-end (moment→field→σ_B→CRLB→RSS error budget→latency budget), grounded in the
`crlb_vs_range` sim. Build clean (0 KaTeX errors).

**✅✅✅ DEEPEN PASS COMPLETE: all 31 chapters (Parts I–XIV) DEEPENED.**

### Part XV — Interactive Capstone (new, web-embedded)
| Ch | Title | State | Notes |
|---:|-------|-------|-------|
| 32 | Interactive system-design lab | 🟢 DEEPENED → review | New companion to Ch. 31: four integrated **dashboards embedded live** on the web edition (system-design/link-budget+trilemma, error-budget by class×location, clinical accuracy chain, distortion+compensation). Manuscript documents each so the prose is complete; dedicated Astro route renders the .md + embeds the islands |

### Part XVI — Performance Characterization (new)
| Ch | Title | State | Notes |
|---:|-------|-------|-------|
| 33 | Performance characterization & benchmarking (system) | 🟢 DEEPENED → review | New chapter [user-requested]: characterization vs calibration vs budgeting; **figures of merit** (trueness/precision/resolution per ISO 5725, accuracy maps, dynamic, distortion robustness, drift); why single-number FoMs mislead + **eq-8.1 normalization** to compare designs not sizes; Hummel/Franz/Yaniv protocols; **ground-truth hierarchy** table (phantom/stage/CMM/robot/optical, 5–10× rule); **worked rig error budget** (0.16 mm floor; can't characterize 0.2 mm system → 28%); rig-build considerations (non-magnetic+non-conductive, registration dominates, thermal, sampling, dynamic, pitfalls); reporting honesty contract. +iso5725 cite |
| 34 | Sensor & component characterization | 🟢 DEEPENED → review | New chapter [user-requested]: the **vendor-data gap** (coil vendors give pair perf not parametrics; TMR omits Barkhausen/hysteresis for AC use); per-class parameter lists (coil: N·A_eff, L/R/Q/SRF, Johnson, cross-axis, **core hysteresis**, B_sat; biased: detectivity/1-f/**Barkhausen**, **hysteresis**, linearity/saturation, offset drift, cross-field); **hysteresis & Barkhausen as un-calibratable floors** (single-valued-map thread); reference-**field** bench (Helmholtz/solenoid, zero-gauss chamber, VNA, FFT) as the dual of Ch.33's reference pose; loop-tracing method; **worked reference-field budget** (0.36% floor); FoM→system (D→σ_B→CRLB) mapping; coil-vs-TMR on one bench. Cites lenz2006/davies2021/monteblanco2021 |

### Part XVII — Software, Integration & Deployment (new)
| Ch | Title | State | Notes |
|---:|-------|-------|-------|
| 35 | Software architecture, integration & lifecycle | 🟢 DEEPENED → review | New chapter [user-requested]: software **stack** (firmware→driver→pose engine→SDK→integration→app); pose-engine **threading/lock-free/timestamping/state-machine**; **integration & API layer** (OpenIGTLink [tokuda2009], PLUS [lasso2014], 3D Slicer [fedorov2012], IGSTK, ROS; pose+covariance+status+frame contract; registration handoff); **IEC 62304** lifecycle [iec62304] (safety classes A/B/C, SOUP, ISO 14971 tie, V&V, cybersecurity); numerical determinism/reproducibility; open-source ecosystem. Cross-refs Parts VII–VIII/Ch.22 (no duplication). +4 verified cites (tokuda2009, lasso2014, fedorov2012, iec62304) |
| 36 | Compute platform & processor selection | 🟢 DEEPENED → review | New chapter [user-requested]: selection **drivers** (data-rate funnel/determinism/numeric/safety-class/form-factor/volume); **silicon taxonomy** (FPGA/SoC/SoM/MCU/DSP/GPU/host); **Cortex-M vs R vs A** + the AMP pattern with a decision rule; **worked stage→silicon mapping** (8ch×1MSps≈128Mbit/s Stage-1→FPGA, sub-GFLOP solve→Cortex-A, lockstep R guard) + compute sanity check (streaming sizes the silicon); RTOS pairing (FreeRTOS/Zephyr/PREEMPT_RT/AMP); **form-factor/power/thermal vs Ch.17 patient-heating** (no hot SoC in a Type-CF part); build-vs-buy/lifecycle. Cross-refs Ch.22 (no duplication); reuses jaeger2017/iec62304 |

### Part XVIII — Power Architecture & Design (new)
| Ch | Title | State | Notes |
|---:|-------|-------|-------|
| 37 | Power architecture & design | 🟢 DEEPENED → review | New chapter [user-requested]: EMT-specific power (not generic). **System power tree** (domain+noise partition; keep drive/digital switching out of AFE rails & field band). **Generator drive** (the decisive case): inductive/resonant high-Q load; **spectral purity = field error** (δI/I→δB/B; harmonics→FDM crosstalk; phase noise→lock-in smear); ratiometric rescue & its limit (current-sense bounds it); class-AB vs class-D spur trade; stability/ringing into reactive load; bounded transient (pulsed-DC settling); current-mode drive; I²R thermal. **Low-noise AFE rails** (worked PSRR/LDO: 80 dB→13 µV/√Hz vs 1.3 nV coil floor; partitioned returns; spur-frequency placement). **Remote biased-sensor bias/reference tree** (reference-stability=measurement-stability, ~1e-4; Type-CF isolation/leakage; ratiometric+chopper; Kelvin sense; tip self-heating vs Ch.17). Cross-refs Ch.9/16/17/25; reuses horowitz_hill/iec60601_1 |

### Part XIX — Differential Tracking, Registration & Motion (new; Tier-1 gap-closure)
| Ch | Title | State | Notes |
|---:|-------|-------|-------|
| 38 | Patient reference sensor & differential tracking | 🟢 DEEPENED → review | **Tier-1 blocking gap (C1) closed.** Clinical EMT is differential not absolute: tool reported relative to a patient-mounted reference. **Differential transform** eq.38.1 (generator frame cancels); **common-mode rejection proof** eq.38.2 (rigid patient/table motion + common generator drift cancel exactly; limits: field-nonuniformity & non-rigid residual); **differential covariance** eq.38.3 (reference ADDS noise, worked 0.5⊕0.5→0.71mm, but rejects cm motion; **gradiometer** distortion cancellation when tool-ref close vs L_D); reference placement 4-way trade (rigidity/correlation/clean-field/workflow; skin-motion artifact); **global silent failure modes** (slip/dropout/reference-in-distortion → redundancy + flag-and-hold); amended Ch.29 clinical accuracy chain. +borgert2006 (sternal+needle sensors, 94% corr, 4× residual reduction) |
| 39 | Registration error theory (FLE/FRE/TRE) | 🟢 DEEPENED → review | **Tier-1 (C3) closed.** FLE/FRE/TRE distinction; **TRE prediction formula** eq.39.1 ⟨TRE²(r)⟩≈(FLE²/N)[1+⅓Σd_k²/f_k²] (Fitzpatrick-West-Maurer); ⟨FRE²⟩=FLE²(1−2/N); **the FRE⊥TRE result** (Fitzpatrick 2009 — displayed FRE is uncorrelated with target error → never use as confidence; overfitting trap); **anisotropic/spatially-varying EMT FLE** (z⁴+distortion → weighted Procrustes); **inherently adverse clinical geometry** (superficial fiducials/deep targets multiply the dominant term); worked ENB example TRE≈2.3mm (3× centroid) while FRE≈1.06mm reassuring-but-meaningless; TRE-reduction levers. +fitzpatrick1998, fitzpatrick2009 |
| 40 | Registration algorithms | 🟢 DEEPENED → review | **Tier-1 (C3) pair complete.** Taxonomy by data (points/surface/deformable); **paired-point closed form** eq.40.1 Procrustes/Kabsch — SVD of cross-covariance (Arun), **det-reflection fix + scale (Umeyama)**, quaternion form (Horn); **ICP** (Besl-McKay: alternate closest-point + paired solve; monotone but local → needs init; point-to-plane/trimmed variants); **deformable** (TPS/B-spline FFD/FEM; overfitting; regularization; EP field-warp tie Ch.28.5); **robustness** (RANSAC/trimmed/Huber for the single silent-global bad correspondence); **weighted Procrustes** for anisotropic EMT FLE (Ch.39); EMT workflow (fiducial/landmark/surface) + failure modes; validate by predicted TRE not FRE. +arun1987, horn1987, umeyama1991, beslmckay1992 |
| 41 | Respiratory & cardiac motion: gating & modeling | 🟢 DEEPENED → review | **Tier-1 (C2) closed.** The dynamic error the reference can't reach: target moves relative to patient. Respiratory (10–25mm, hysteretic) vs cardiac (ECG); **3 strategies** (gating to end-expiration low-residual/low-duty; **surrogate+correspondence model** full-duty/model-limited — Borgert affine, 94%/4×; **4D/biomechanical**); **correspondence-model failure modes** (hysteresis→need phase+velocity; baseline drift; intra-proc change; imperfect corr); **ECG-gating in EP** (avoid motion-blurred maps); **prediction under latency** (Ch.12/21); **worked budget** σ_motion 20mm→2–5mm (the missing dominant term — tracker irrelevant behind breathing); match phases image↔reg↔nav; detect-and-flag irregular breathing; over-trust/automation-bias guard. +borgert2006, mcclelland2013, keall2006 (AAPM TG-76) |

(All chapters now DEEPENED → awaiting user review/verification.)

## Flagged for upcoming chapter passes
- ✅ **DONE (Ch. 17 deepened):** electrical-safety contrast between
  **biased sensors (TMR/MR, Hall, fluxgate) and passive coils** in patient-applied
  EMT tools. A passive coil carries no power at the patient end (only the induced
  µV EMF), so leakage/shock risk and isolation are minimal. A *biased* sensor
  needs DC bias + a stable reference delivered to the sensor at/near the body →
  active conductors carrying power into a Type CF applied part: patient-leakage
  limits (10/50 µA), single-fault analysis of the bias rail, tip self-heating, and
  galvanic-isolation of the bias supply all become first-order (IEC 60601-1).
  Tie to Ch. 14.3 (TMR bias) and Ch. 25 (bias-reference noise). [user-requested]

## User-review queue
- [ ] Ch. 19–25 — awaiting review (batch)
