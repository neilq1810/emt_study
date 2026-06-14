# Glossary & Acronyms

> **Reference.** Acronyms and the book's recurring terms of art, each pointing to where it is
> developed.

## Acronyms
| | |
|---|---|
| **AC / DC** | alternating / direct current excitation |
| **ADC / AFE** | analog-to-digital converter / analog front end (Ch. 16/18) |
| **BEM / FEA** | boundary-element / finite-element method (Ch. 7) |
| **CDM / FDM / TDM** | code- / frequency- / time-division multiplexing (Ch. 19) |
| **CRLB** | Cramér–Rao lower bound (Ch. 24) |
| **COU / QOI** | context of use / question of interest — model credibility (Ch. 53) |
| **DHF** | design history file (Ch. 48) |
| **DOF** | degrees of freedom (5-DOF / 6-DOF sensors, Ch. 13) |
| **(P)DOP** | (position) dilution of precision (Ch. 24) |
| **ENBW** | equivalent noise bandwidth (Ch. 20) |
| **ENOB** | effective number of bits (Ch. 18) |
| **FIM** | Fisher information matrix (Ch. 24) |
| **FRE / TRE** | fiducial / target registration error (Ch. 39) |
| **HF** | human factors / usability engineering (Ch. 46) |
| **IMU** | inertial measurement unit (Ch. 21) |
| **LM / MLE / MAP** | Levenberg–Marquardt / maximum-likelihood / maximum-a-posteriori (Ch. 23) |
| **MDR** | EU Medical Device Regulation; also US Medical Device Reporting (Ch. 48/52) |
| **NIS / NEES** | normalized innovation- / estimation-error squared (Ch. 21) |
| **PFA / RF** | pulsed-field / radiofrequency ablation (Ch. 28/29) |
| **PINN** | physics-informed neural network (Ch. 30/55) |
| **QMS / QMSR** | quality management system / US Quality Management System Regulation (Ch. 48) |
| **SRF** | self-resonant frequency of a coil (Ch. 9) |
| **V&V / V&V 40** | verification & validation / ASME credibility standard (Ch. 48/53) |

## Terms of art
- **Coupling matrix ($\mathbf M$)** — the $3\times3$ transmit-axis × sense-axis signal matrix; the raw observable a 6-DOF tracker inverts (Ch. 5).
- **Detect-and-flag** — emit pose *with* a quality flag and degrade gracefully rather than report a confident wrong answer; the book's load-bearing safety control (Ch. 27/44/46).
- **Dynamic reserve** — a lock-in's tolerance to a large out-of-band interferer before overload (Ch. 20).
- **Golden unit / golden fixture** — an exhaustively characterized reference used to transfer calibration and gate production accuracy (Ch. 50).
- **Hemisphere (parity) ambiguity** — distinct poses ($+\mathbf r$ vs $-\mathbf r$) giving identical measurements under the dipole's $\hat{\mathbf r}\to-\hat{\mathbf r}$ symmetry; a *global* un-identifiability (Ch. 24 §24.7).
- **Lock-in / synchronous detection** — phase-sensitive demodulation at the excitation frequency; the matched filter for a known tone (Ch. 20).
- **Pulsed-DC** — energize, wait for eddy transients to decay, sample the settled static field; the conductive-distortion-tolerant excitation mode (Ch. 6/28).
- **Reconciled (digital) twin** — a model run alongside the system whose *divergence* from reality is the live distortion/fault signal (Ch. 53/56).
- **Roll null** — the unobservable rotation about a single sensor coil's own axis (the 5-DOF limit, Ch. 13).
- **Witness sensor** — an independent sensor at a *known* pose whose residual cannot absorb distortion into a pose fit, exposing it (Ch. 27/56).
