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
| 22 | Real-time implementations | ⬜ DRAFT | next |
| 23 | Inverse problem (solvers) | ⬜ DRAFT | |
| 24 | Conditioning, observability, uncertainty | ⬜ DRAFT | partly backed by Phase-5 sims |
| 25 | Error taxonomy & budgets | ⬜ DRAFT | |

(Other chapters remain DRAFT; will be scheduled after this batch.)

## User-review queue
- [ ] Ch. 19 — awaiting review
