# EM-Tracking-Definitive-Guide

**A doctoral-level reference work, engineering design guide, and interactive
educational platform for electromagnetic tracking (EMT) technology.**

This repository is being assembled by a multidisciplinary research effort
(EMT systems, analog/sensor electronics, DSP, RF/electromagnetics, medical
device systems, history of technology, and data visualization) with the goal
of producing the most comprehensive and technically rigorous open reference on
electromagnetic position-and-orientation tracking ever assembled.

The target end-state is a work detailed enough that an experienced engineer
could use it as the **primary reference for designing a state-of-the-art
electromagnetic tracking system from first principles**, spanning:

> *The Art of Electronics* + *Principles of GNSS* + *Medical Device
> Engineering* + a PhD dissertation — for electromagnetic tracking.

---

## ⚠️ Status: Early construction (Increment 1)

This is a long-horizon, multi-phase project. It is being built **iteratively**,
not in a single pass. See [`ROADMAP.md`](./ROADMAP.md) for the phased plan and
live progress tracker. Nothing here is "final"; chapters move through a
research → draft → review → verified lifecycle tracked per chapter.

**Research integrity policy (non-negotiable):** Every quantitative claim,
historical statement, specification, and architectural attribution must be
traceable to a verifiable primary or authoritative source recorded in
[`citations/bibliography.json`](./citations/bibliography.json). Where evidence
is uncertain or contested, the text says so explicitly. No fabricated
references, no invented performance numbers. See the per-claim confidence
conventions in [`ROADMAP.md`](./ROADMAP.md#research-quality-control).

---

## Repository layout

| Directory          | Purpose                                                             |
|--------------------|---------------------------------------------------------------------|
| `book/`            | The manuscript: Parts I–XIV, one Markdown file per chapter.         |
| `references/`      | Source notes, extracted figures, and reading summaries.             |
| `citations/`       | Machine-readable bibliography (JSON) + exporters to BibTeX/CSV.      |
| `data/`            | Datasets: extracted specs, measured/standard performance tables.    |
| `tables/`          | Canonical comparison tables (CSV) referenced by the book.           |
| `figures/`         | Generated static figures (SVG/PNG) and their source scripts.        |
| `visualizations/`  | Source for diagrams (block/signal-chain/timing/uncertainty).        |
| `simulations/`     | Physics & DSP simulations (Python/notebooks) that back the figures. |
| `notebooks/`       | Exploratory and worked-example Jupyter notebooks.                   |
| `scripts/`         | Tooling: bibliography export, build, cross-reference checks.        |
| `dashboard/`       | Interactive website source (digital textbook + tools).              |
| `assets/`          | Static assets for the book and site.                                |

## How to navigate

1. Start with [`book/OUTLINE.md`](./book/OUTLINE.md) — the exhaustive master
   table of contents (Parts I–XIV).
2. Read chapters under `book/part-XX-*/`.
3. Every `[@key]`-style citation in the text resolves to an entry in
   `citations/bibliography.json`.

## Building the bibliography exports

```bash
python3 scripts/export_bibliography.py
# writes citations/bibliography.bib, citations/bibliography.csv
```

## License & contributions

Intended as an open educational reference. Contribution conventions
(especially the citation/verification requirements) live in `ROADMAP.md`.
