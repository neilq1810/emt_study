# Chapter 3 — Technology Timelines & Trees

> **Status:** DRAFT · **Part I — Foundations** (closes Part I)
> Synthesizes the history (Ch. 1) and genealogy (Ch. 2) into structured timelines
> and technology trees. Citation keys resolve to
> [`../../citations/bibliography.json`](../../citations/bibliography.json).

This chapter organizes the field's evolution into three reference structures: an
**excitation-scheme technology tree**, a **sensor technology tree**, and a
**capability timeline**. They are navigational aids — every node points to the
chapter that develops it — and they make explicit the branching choices
(established physically in Parts II–IV) that distinguish one tracker from another.

---

## 3.1 Excitation-scheme technology tree

How the transmitted field is structured in time is the primary architectural
fork (Ch. 6, 8, 19). The tree:

```
Quasi-static magnetic excitation (Ch. 4)
│
├── Continuous AC  (Polhemus lineage; Kuipers→Raab, Ch. 2)            [Ch. 8, 28.1]
│     ├── multiplexing of the 3 axes:
│     │     ├── FDM  (simultaneous, high rate)                        [Ch. 19.2]
│     │     ├── TDM  (sequential, clean decode)                       [Ch. 19.3]
│     │     └── CDM / orthogonal codes                                [Ch. 19.4]
│     ├── rotating-field excitation (2-axis → phase/amplitude decode) [Paperno, Ch. 9.2]
│     └── transmitter arrays (many uniaxial coils, subarray tracking) [Plotkin, Ch. 9.2]
│
├── Pulsed / transient DC  (Ascension lineage; Blood, Ch. 2)          [Ch. 6.4, 28.2]
│     └── energize → wait for eddy settling → sample static field
│
└── Hybrid / mixed excitation
      ├── nutating field (DC + AC carrier) — the Kuipers 1975 origin  [Ch. 2.1]
      ├── quadratic/quadrature & distortion-aware modulations         [Ch. 8.2]
      └── EM + IMU / EM + optical fusion (system-level hybrid)        [Ch. 21, 30.2]
```

The **root insight** (Ch. 6): every excitation choice is a position on the
*sensitivity-vs-distortion* spectrum. Continuous AC maximizes rate/sensitivity but
pays an eddy-current penalty that grows with frequency; pulsed-DC trades rate for
conductive-distortion immunity; hybrids and fusion try to get both. The tree's
branches are therefore not arbitrary — they are the discrete answers to one
continuous physical trade.

## 3.2 Sensor technology tree

How the field is transduced is the second fork (Ch. 13, 14). The decisive split is
**what physical quantity is measured** — rate-of-change of flux (induction) vs.
the field itself (direct):

```
Magnetic field transduction (Ch. 13.0)
│
├── Induction pickups  (EMF ∝ ω·B; blind at DC → AC architectures)    [Ch. 14.1]
│     ├── wire-wound coils (often ferrite-cored; clinical gold std)   [Ch. 14.1, 14.2]
│     │     └── elongated catheter coils (L ≈ 10–20× dia.)            [Ch. 14.2]
│     ├── PCB / planar spiral coils (reproducible, lower sensitivity) [Ch. 14.1]
│     └── thin-film / MEMS microcoils                                 [Ch. 14.1]
│
└── Direct field sensors  (respond to B incl. DC → pulsed-DC, chip-scale)
      ├── Hall (DC, low sensitivity)                                  [Ch. 14.3.5]
      ├── Fluxgate (very low DC noise, larger)                        [Ch. 14.3.5]
      ├── Magnetoresistive family                                     [Ch. 14.3]
      │     ├── AMR (mature, low-ish 1/f)
      │     ├── GMR (higher sensitivity, smaller range)
      │     └── TMR / MTJ (highest sensitivity; bridge; chip-scale)   [Ch. 14.3.1–4]
      └── Quantum / atomic
            ├── optically pumped / SERF (fT, near-zero-field)         [Ch. 30.4]
            └── NV-diamond (solid-state, microscale)                  [Ch. 30.4]
```

The tree's **trajectory** (Ch. 14, 30): the clinical mainstream remains
induction coils (smallest passive AC sensors), but the growth edge is
**direct-field, chip-scale TMR/MR** (DC capability, arrays) and, at the research
frontier, **quantum sensors** — whose relevance to EMT is bounded by dynamic-range/
bandwidth needs, not sensitivity (Ch. 30.4).

## 3.3 Capability timeline

A compressed timeline of *capability* milestones, each tagged to its source and
confidence (dates are issue/publication dates unless noted; corporate dates from
Ch. 28, conf: med):

| Year | Milestone | Significance | Source |
|---|---|---|---|
| 1969 | Polhemus founded | AC EM tracking commercialization begins | [@polhemus_history] (conf: med) |
| 1975 | Kuipers patent US3,868,565 | foundational pose-tracking IP (nutating field) | [@kuipers1975] |
| 1979 | Raab et al. formalize 6-DOF AC dipole method | the field's theoretical cornerstone | [@raab1979] |
| 1986 | Ascension founded (Scully & Blood) | pulsed-DC commercialization | [@ascension_roper2012] (conf: med) |
| 1990 | Blood patent US4,945,305 (DC, metal immunity) | pulsed-DC IP cornerstone | [@blood1990] |
| 1993 | Biosense founded (Ben-Haim) | medical catheter localization | [@globes_jnj_biosense] (conf: med) |
| 1995 | Ben-Haim catheter-localization patent US5,391,199 | CARTO IP basis | [@benhaim1995] |
| 1997 | Gepstein/Ben-Haim nonfluoroscopic mapping; J&J acquires Biosense | EP breakthrough + consolidation | [@gepstein1997; @globes_jnj_biosense] |
| 1998 | Birkfellner systematic-distortion characterization | rigorous distortion study | [@birkfellner1998] |
| ~2000s | NDI Aurora medical-grade EMT | OEM/research medical standard | [@ndi_history; @yaniv2009] (conf: med) |
| 2005 | Hummel standardized assessment protocol | comparable accuracy measurement | [@hummel2005] |
| 2009 | CARTO 3 | mature EP electroanatomical mapping | [@globes_jnj_biosense] (conf: med) |
| 2011–12 | Roper acquires NDI; NDI acquires Ascension | OEM medical-tracking consolidation | [@ascension_roper2012] |
| 2012 | Covidien acquires superDimension (ENB) | pulmonary navigation scales | [@covidien_superdimension2012] (conf: med) |
| 2014 | Franz et al. definitive medical-EMT review | field consolidation | [@franz2014] |
| 2019 | NAVIGATE ENB one-year results (~73% yield) | large-scale clinical evidence | [@folch2019] |
| 2020–23 | NV-diamond review; TMR detectivity/bias; witness-sensor ML compensation | sensor & compensation frontier | [@barry2020; @davies2021; @monteblanco2021; @cavaliere2023] |

Reading the timeline by **capability axis**:
- **Working volume & moment** — steady engineering improvement (Ch. 9), not a
  single breakthrough.
- **DOF** — 6-DOF established at the 1975/1979 origin; the later story is
  *miniaturizing* 5/6-DOF sensors (Ch. 13–14).
- **Accuracy** — the leap was *measurability/comparability* (Hummel 2005,
  [@hummel2005]) as much as raw accuracy; in-situ accuracy is still gated by
  distortion/registration (Ch. 25, 29).
- **Update rate / latency** — improved with electronics and DSP (Parts VI–VII);
  still bounded by the trilemma (Ch. 12).
- **Robustness** — the *current* frontier (distortion compensation, fusion;
  Ch. 27, 30), and where the patent activity has migrated (Ch. 2.2).

## 3.4 How to use these trees
These structures are the book's **map**: choosing an excitation branch (§3.1) and
a sensor branch (§3.2) fixes most downstream design constraints (Parts III–X),
and the timeline (§3.3) situates any system in the field's evolution. The
build-from-scratch chapter (Ch. 31) is, in effect, a guided walk down one path of
each tree.

---

## Open questions / to verify
- Firm up corporate founding/product dates (conf: med) with second sources
  (shared with Ch. 28 open questions).
- Add quantitative capability curves (volume, accuracy, update rate vs. year) once
  sourced numbers exist — a Phase-4 figure / Phase-6 interactive "technology
  timeline explorer" (project brief).
- Add NDI founding year and Aurora first-release date (shared Ch. 1/28 open item).

## Sources cited
- [@polhemus_history; @kuipers1975; @raab1979; @ascension_roper2012; @blood1990;
  @globes_jnj_biosense; @benhaim1995; @gepstein1997; @birkfellner1998;
  @ndi_history; @yaniv2009; @hummel2005; @covidien_superdimension2012; @franz2014;
  @folch2019; @barry2020; @davies2021; @monteblanco2021; @cavaliere2023;
  @paperno2001; @plotkin2003].
