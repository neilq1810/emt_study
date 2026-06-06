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
| 4     | Figures & visualizations                                 | 🟡 5 computed figures (Ch.4/20/24); diagrams pending |
| 5     | Simulations                                              | 🟡 Core suite done (emtrack lib + run_all.py) |
| 6     | Interactive website (digital textbook + tools)           | 🟡 Scaffold done (Astro+Tailwind+KaTeX, Pages CI); tools pending |
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

> **All technical Parts (II–XIV) now drafted.** Remaining prose: Part I Ch.2
> (patent/academic genealogy) & Ch.3 (timelines/trees). Then non-prose phases:
> figures (4), simulations (5), website (6), cross-ref (7), review (8), final (9).

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
