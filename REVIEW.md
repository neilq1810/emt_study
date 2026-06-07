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
| 10 | Timing, clocking, sync | ⬜ DRAFT | |
| 11 | DSP pipeline & estimation | ⬜ DRAFT | |
| 12 | Latency & real-time | ⬜ DRAFT | |

(Other chapters remain DRAFT; will be scheduled next.)

## User-review queue
- [ ] Ch. 19–25 — awaiting review (batch)
