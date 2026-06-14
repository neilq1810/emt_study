# Reader's Guide

> **Front matter.** What this book is, how it is organized, how to read it for your role,
> and the conventions and methodology behind it. The notation table, glossary, appendices,
> and decision frameworks are in the **Reference** part at the end.

## What this book is

This is intended as a *definitive* technical reference on **electromagnetic tracking (EMT)**:
the determination of a sensor's position and orientation from the coupling of quasistatic
magnetic fields, with an emphasis on the medical context where it is most demanding. It runs
the full chain — **physics → hardware → signal processing → estimation → accuracy → the
clinical system → the product and its lifecycle → frontiers** — and tries to be honest at
every step about what is known, what is assumed, and where the published record (this book
included) stops and a vendor's proprietary engineering begins.

It is written to be useful at two altitudes: read linearly, it is a course; consulted by
section, it is a reference. Equations carry derivations, claims carry citations, and the
quantitative results are backed by a runnable simulation suite (below).

## How it is organized — the reading arcs

The chapters were developed iteratively and are grouped into Parts, but they form **eight
thematic arcs**:

1. **Foundations & history** (Parts I–II) — where EMT came from and the electromagnetic
   theory it rests on (Maxwell/quasistatics, the dipole, coupling, distortion).
2. **The instrument** (Parts III–VI, XVII, XVIII, XXI) — system architecture, field
   generators, sensors, analog front ends, data conversion, compute/software, power, and
   wireless/alternative architectures.
3. **Signal processing & pose estimation** (Parts VII–VIII) — excitation/channel separation,
   synchronous detection, real-time implementation, the inverse problem, observability, and
   uncertainty (the CRLB).
4. **Accuracy** (Parts IX–X, XVI) — error sources and budgets, calibration, distortion
   compensation, and performance characterization.
5. **The clinical system** (Parts XII, XIX) — medical applications, and the registration,
   motion, frame-management, and in-body-metal effects that usually dominate the *target*
   accuracy a clinician sees.
6. **Product, dependability & lifecycle** (Parts XI, XX, XXII) — the commercial ecosystem,
   reliability, risk, human factors, regulatory pathways and quality systems, clinical
   evaluation, manufacturing, durability, and field operations.
7. **Building it & frontiers** (Parts XIII–XV, XXIII) — an end-to-end design worked example,
   the interactive capstone, research frontiers, and the **digital-twin** methodology.

*(A planned structural revision will re-home the existing chapters into these eight Parts and
renumber them monotonically; see the roadmap. The chapter numbers are stable identifiers in
the meantime.)*

## Reader pathways

You do not have to read all 57 chapters. Suggested entry paths by role:

| If you are… | Read, in order |
|---|---|
| **An EM physicist / modeler** | Parts II → IV (4–7, 13–15), then 24 (observability) |
| **A firmware / DSP engineer** | Parts III, VII (8–12, 19–22), then 35–37 |
| **An estimation / algorithms reader** | 23–24, 21, 25, 26–27 (the inverse problem → uncertainty → calibration) |
| **A clinical-systems engineer** | 29, 38–43, 33–34, 46 (the system accuracy & workflow story) |
| **A regulatory / quality lead** | 45, 48, 49, 44, 50–52 (risk → pathways/QMS → clinical evidence → lifecycle) |
| **A researcher / architect** | 30, 53–57, 31–32 (frontiers, the digital twin, the build example) |

**The load-bearing foundations.** Derived from the manuscript's own cross-references
(`figures/readers_dependency_map.png`), the most-depended-on Parts — the ones nearly every
later chapter leans on — are **Part II (electromagnetic theory, ~240 inbound references),
Part III (architecture), Part VII (DSP), Part VIII (solvers), Part X (calibration), and
Part IV (sensors)**. If you read only a foundation, read Part II.

## Conventions

- **Cross-references.** `Ch. N` points to a chapter; `§N.M` to a section. These are verified
  to resolve (see *methodology*).
- **Citations.** `[@key]` resolves to [`../../citations/bibliography.json`](../../citations/bibliography.json);
  the exported `.bib`/`.csv` accompany it.
- **Confidence tags.** Inline `(conf: high / med / low)` marks how well-supported a specific
  claim is — *high* means derived or primary-sourced; *med/low* flags vendor-class numbers,
  illustrative figures, or open questions. **Where the book is uncertain, it says so.**
- **Figures from simulations.** Most plots are *computed* by `simulations/run_all.py`
  (Phase-5), not drawn; a few are schematic diagrams (`simulations/make_diagrams.py`). Each
  figure is tied to the chapter it backs and the [results](../../simulations/RESULTS.md).
- **Reference apparatus.** Symbols → the **Notation** table; acronyms/terms → the
  **Glossary**; deferred derivations → the **Appendices**; recurring design choices → the
  **Decision Frameworks** (all in the Reference part).

## Methodology & the honesty contract

This manuscript is built to be *checkable*, not merely asserted:

- **A runnable simulation suite** (an `emtrack` library + 18 simulations) computes the
  quantitative results — the CRLB and the $z^4$ law, the 6-DOF coupling penalty, the
  detect-and-flag ROC, calibration-as-identification, the triangle→square demodulator, the
  eddy quadrature signature, and more — so the numbers in the prose are reproducible, not
  recalled.
- **A credibility verifier** (`scripts/verify_manuscript.py`) checks, on every change, that
  citations resolve, figures/data referenced exist, chapter and §-references are valid, no
  placeholder markers remain, and the headline simulation numbers still match the prose. It
  passes.
- **Citations are searched, not remembered**, and several corporate and standards facts were
  web-corroborated; items that remain single-source or vendor-class are tagged `conf: med`.
- **The method-vs-measurements boundary is stated explicitly.** The book will keep you from
  every error of *understanding*; it cannot hand you the *measured* noise floor, the
  proprietary calibration, or a robust connector. The digital-twin part (53–57) is the most
  complete statement of where that line falls — it supplies the method, the structure, and
  the experiment that validates it, never the vendor's tuned values.

That posture — *show the uncertainty, never manufacture false precision* — is the same one
the book argues for in the systems it describes (Ch. 46). It is the contract between this
text and its reader.
