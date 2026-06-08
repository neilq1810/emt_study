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

(Other chapters remain DRAFT; will be scheduled next.)

## Flagged for upcoming chapter passes
- **Ch. 17 (AFE/EMC/safety) deep pass — ADD:** electrical-safety contrast between
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
