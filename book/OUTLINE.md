# Master Outline — *EM-Tracking-Definitive-Guide*

> Exhaustive table of contents. Section numbering is stable: cross-references
> in chapters point to these `§` anchors. Status tags per chapter live in
> [`../ROADMAP.md`](../ROADMAP.md).

## Front matter
- Preface — scope, audience, how to read, conventions
- Notation & symbols (SI units, vector/tensor conventions, coordinate frames)
- Glossary of acronyms (EMT, AC/DC/pulsed-DC, DOF, AFE, ADC, FDM/TDM/CDM, …)
- On evidence and citation (confidence tags, source hierarchy)

---

## PART I — FOUNDATIONS

### Ch. 1 — History of Electromagnetic Tracking
1.1 What "electromagnetic tracking" means and what it competes with
1.2 Pre-history: goniometers, mechanical linkages, and the motivation for
    line-of-sight-free tracking
1.3 Military and aerospace origins — helmet-mounted sight / cueing systems
1.4 The Polhemus lineage and AC magnetic tracking (Kuipers, SPASYN)
1.5 The 1979 Raab et al. formalization of 6-DOF magnetic tracking
1.6 Ascension Technology and pulsed-DC tracking (Blood)
1.7 Northern Digital (NDI) Aurora and medical-grade EMT
1.8 Biosense / CARTO and the electrophysiology breakthrough
1.9 Industrial, VR/AR, and motion-capture adoption
1.10 Commercial evolution & consolidation timeline
1.11 Key researchers, institutions, and labs

### Ch. 2 — Patent & Academic Genealogy
2.1 Patent genealogy: priority chains and claim evolution
2.2 The AC vs. pulsed-DC patent landscape
2.3 Academic genealogy: dissertation lineages and citation trees
2.4 How IP shaped commercial architectures

### Ch. 3 — Technology Timelines & Trees
3.1 Excitation-scheme technology tree (AC / pulsed-DC / hybrid)
3.2 Sensor technology tree — two branches:
    (a) induction pickups (wire-wound, PCB, thin-film coils; EMF ∝ ω·B);
    (b) direct field sensors (Hall, fluxgate, AMR, GMR, **TMR**, optically
        pumped/atomic magnetometers; respond to B including DC)
3.3 Capability timeline (volume, DOF, accuracy, update rate)

---

## PART II — ELECTROMAGNETIC THEORY

### Ch. 4 — Maxwell's Equations, Quasistatics & the Magnetic Dipole
4.1 Maxwell's equations and constitutive relations
4.2 The quasi-magnetostatic (near-field) regime and why EMT lives there
4.3 Wavelength, near/far field boundary, retardation neglect
4.4 The magnetic dipole field (derivation from vector potential)
4.5 Field of a finite circular loop; on-axis and off-axis forms
4.6 Dipole approximation error vs. distance/size
4.7 Worked example: field magnitude budget for a benchtop volume

### Ch. 5 — Coil Coupling, Mutual Inductance & Magnetic Moment
5.1 Magnetic moment of a multi-turn coil; effective area
5.2 Flux linkage and the induced EMF (Faraday)
5.3 Mutual inductance as the core observable; Neumann formula
5.4 The 3×3 coupling matrix between orthogonal triads
5.5 Reciprocity and its consequences for source/sensor symmetry
5.6 Superposition of multiple transmitter coils
5.7 Field gradients and their role in pose observability

### Ch. 6 — Distortion Physics
6.1 Conductive materials: induced eddy currents (Faraday + Ohm)
6.2 Skin depth, frequency dependence, and the AC penalty
6.3 Ferromagnetic materials: permeability, field concentration, hysteresis
6.4 Pulsed-DC rationale: settling of eddy currents
6.5 Field-perturbation theory; image-current models
6.6 Quantifying distortion: error vs. material/geometry/frequency

### Ch. 7 — Analytical & Numerical Methods
7.1 Closed-form dipole/loop models and their domain of validity
7.2 Finite element analysis (FEA): formulation, meshing, boundary conditions
7.3 Boundary element / method of moments for conductors
7.4 Verification & validation of EM models against measurement

---

## PART III — TRACKER ARCHITECTURE

### Ch. 8 — Complete System Architecture
8.1 Reference block diagram (generator → field → sensor → AFE → ADC → DSP → solver → host)
8.2 AC vs. pulsed-DC vs. hybrid system trades at the architecture level
8.3 Source-driven vs. sensor-driven topologies; transmit/receive roles

### Ch. 9 — Field Generators & Sensor Coils
9.1 Generator coil geometries and drive electronics
9.2 Field-shaping and uniformity strategies
9.3 Sensor coil topologies and the 3/5/6-DOF mapping

### Ch. 10 — Timing, Clocking & Synchronization
10.1 Coherent vs. non-coherent detection; reference distribution
10.2 Clock architecture, jitter budget
10.3 Channel multiplexing in time/frequency/code

### Ch. 11 — DSP Pipeline & Estimation
11.1 From samples to channel amplitudes
11.2 From amplitudes to the coupling matrix
11.3 From coupling matrix to pose (hand-off to Part VIII)

### Ch. 12 — Latency & Real-Time Constraints
12.1 End-to-end latency budget
12.2 Throughput vs. latency vs. accuracy trades
12.3 Real-time scheduling and determinism

---

## PART IV — SENSOR ENGINEERING

### Ch. 13 — Sensor Physics & Geometries
13.0 Two sensing principles: induction pickups (EMF ∝ ω·B) vs. direct
     field sensors (respond to B, including DC) — and what each implies for
     AC vs. pulsed-DC architectures (ties to Ch. 6, Ch. 8)
13.1 Single-element 5-DOF sensing (and the roll ambiguity)
13.2 Orthogonal triad 6-DOF sensing
13.3 Non-orthogonal and over-determined arrangements
13.4 Hybrid sensors (EM + IMU)

### Ch. 14 — Sensor Construction, Miniaturization & Technologies
14.1 Wire-wound vs. PCB vs. thin-film induction coils
14.2 Catheter and implantable sensors
14.3 Solid-state magnetic field sensors — the magnetoresistive family
     14.3.1 AMR, GMR, and **TMR (tunneling magnetoresistance)** — physics and
            comparison (sensitivity, MR ratio, size, power)
     14.3.2 **Wheatstone-bridge / push-pull TMR sensors** — offset & temperature
            compensation, full-bridge vs. half-bridge, reference layers
     14.3.3 Set/reset (flipping) schemes, linearization, hysteresis
     14.3.4 Noise in MR sensors: 1/f (flicker) noise floor and its impact on
            low-frequency/quasi-static resolution; detectivity (T/√Hz)
     14.3.5 Hall-effect and fluxgate sensors for context/comparison
     14.3.6 Why MR/TMR suits pulsed-DC, chip-scale, and array architectures
            (flat DC response where induction coils fail)
14.4 MEMS resonant/Lorentz-force magnetometers and other emerging approaches
14.5 Sensor selection matrix: coil vs. fluxgate vs. Hall vs. AMR/GMR/TMR vs.
     OPM — sensitivity, bandwidth, size, power, noise, cost, DC capability

### Ch. 15 — Manufacturing, Tolerance & Noise
15.1 Tolerance analysis (winding, alignment, area)
15.2 Sensitivity analysis
15.3 Sensor self-noise and SNR floor

---

## PART V — ANALOG FRONT ENDS

### Ch. 16 — Amplification & Noise Budgeting
16.1 Low-noise amplifiers; voltage/current noise, NEF
16.2 Instrumentation amplifiers and CMRR
16.3 Input impedance and coil loading
16.4 Dynamic range and the strong-near-field problem
16.5 End-to-end noise budget

### Ch. 17 — Filtering, EMC & Power
17.1 Anti-alias and band-select filtering
17.2 Shielding, grounding, guarding
17.3 EMC and medical-grade isolation/power requirements

---

## PART VI — DATA CONVERSION

### Ch. 18 — ADC Systems
18.1 Architectures: Σ-Δ, SAR, pipeline — trade space
18.2 SNR, ENOB, and the EMT-relevant figures of merit
18.3 Sampling theory, oversampling, decimation
18.4 Clock jitter and quantization error propagation

---

## PART VII — DIGITAL SIGNAL PROCESSING

### Ch. 19 — Excitation & Channel Separation
19.1 Frequency-division multiplexing
19.2 Time-division multiplexing
19.3 Code-division / orthogonal excitation
19.4 Trade space vs. update rate and distortion

### Ch. 20 — Synchronous Detection & Filtering
20.1 Lock-in amplification / synchronous detection (math + implementation)
20.2 Matched filtering and FFT-based amplitude estimation
20.3 Adaptive filtering for interference rejection

### Ch. 21 — State Estimation & Fusion
21.1 Kalman filtering (EKF/UKF) for pose tracking
21.2 Particle filtering
21.3 EM + IMU + optical sensor fusion

### Ch. 22 — Real-Time Implementations
22.1 FPGA pipelines
22.2 GPU acceleration
22.3 Embedded/DSP-core implementations

---

## PART VIII — POSITION SOLVERS

### Ch. 23 — The Inverse Problem
23.1 Forward model recap and the measurement equation
23.2 Linear and nonlinear least squares
23.3 Levenberg–Marquardt; Gauss–Newton
23.4 Maximum likelihood and Bayesian estimation
23.5 Constraint handling and outlier rejection

### Ch. 24 — Conditioning, Observability & Uncertainty
24.1 Observability and identifiability of pose parameters
24.2 Conditioning and numerical stability
24.3 Convergence analysis and initialization
24.4 Covariance/CRLB and uncertainty quantification

---

## PART IX — ERROR SOURCES

### Ch. 25 — Error Taxonomy & Budgets
25.1 Stochastic: sensor/ADC/thermal noise
25.2 Deterministic: tolerances, model mismatch, calibration residual
25.3 Environmental: distortion, interference, cabling, motion
25.4 Synchronization & numerical errors
25.5 Building an error budget; sensitivity matrices; Monte Carlo

---

## PART X — CALIBRATION

### Ch. 26 — Calibration of Sensors, Generators & Systems
26.1 Sensor and generator characterization
26.2 System-level field mapping
26.3 Verification procedures and long-term stability

### Ch. 27 — Distortion Compensation
27.1 Lookup/polynomial field-distortion correction
27.2 Adaptive/online calibration
27.3 Machine-learning compensation (and its pitfalls)

---

## PART XI — COMMERCIAL ECOSYSTEM

### Ch. 28 — Vendor Survey
For each: history · technology · architecture · strengths · weaknesses ·
patents · clinical adoption · reported performance · market position.
28.1 Polhemus
28.2 Ascension Technology / TrakSTAR / driveBAY (and post-acquisition)
28.3 Northern Digital Inc. (NDI) / Aurora
28.4 Biosense Webster / CARTO
28.5 St. Jude / Abbott EnSite; Boston Scientific Rhythmia
28.6 Robotics & navigation platforms; emerging startups
28.7 Cross-vendor comparison (standardized assessment)

---

## PART XII — MEDICAL APPLICATIONS

### Ch. 29 — Clinical Applications & Workflows
29.1 Cardiac electrophysiology and ablation
29.2 Electromagnetic navigation bronchoscopy
29.3 ENT and skull-base navigation
29.4 Interventional radiology and biopsy
29.5 Robotic surgery and image-guided therapy
29.6 AR-assisted navigation; future applications
29.7 Regulatory requirements & integration architectures

---

## PART XIII — RESEARCH FRONTIERS

### Ch. 30 — State of the Art & Open Problems
30.1 Recent advances and leading laboratories
30.2 Hybrid optical + EM systems
30.3 AI-assisted calibration and ML distortion compensation
30.4 Novel sensors: high-detectivity TMR and MR sensor arrays; quantum/atomic
     (optically pumped, NV-diamond) magnetometry possibilities and their
     noise-floor vs. bandwidth trade for EMT
30.5 Open problems and research opportunities

---

## PART XIV — BUILDING A SYSTEM FROM SCRATCH

### Ch. 31 — End-to-End Design Worked Example
31.1 Requirements capture and architecture selection
31.2 Field generator design
31.3 Sensor design
31.4 AFE design
31.5 DSP implementation
31.6 Calibration & validation/verification
31.7 Manufacturing & regulatory pathway
31.8 Reference implementation & open-source ecosystem

---

## Back matter
- Appendix A — Vector identities & coordinate transforms
- Appendix B — Physical constants & material properties
- Appendix C — Derivations deferred from the main text
- Appendix D — Standardized assessment protocols (Hummel & successors)
- Appendix E — Symbol index
- Full bibliography (generated from `citations/bibliography.json`)
