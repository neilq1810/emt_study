# Dashboard — Interactive Digital Textbook (Astro)

Static site that renders the `/book` manuscript as a browsable digital textbook,
with KaTeX-typeset mathematics. Built with **Astro + Tailwind**, deployable to
**GitHub Pages**.

## Architecture

- The Markdown in the repo-root `/book` directory is the **single source of
  truth**. This app reads it via an Astro content collection
  (`src/content.config.ts`, glob loader with `base: '../book'`); the book is
  *not* duplicated here.
- Titles are derived from each chapter's first `# H1`; parts are grouped from the
  `part-NN-*` directory names (`src/lib/toc.ts`).
- Math (`$…$`, `$$…$$`) is rendered at build time via `remark-math` +
  `rehype-katex`.

## Simulation link (figures & computed data)

The Python simulations (`simulations/run_all.py`) write to the repo-root
`/figures` and `/data`. Those are surfaced on the site by:

1. **`scripts/copy-assets.mjs`** — copies `/figures` and `/data` into
   `public/` (run automatically by the `predev`/`prebuild` npm hooks, or
   `npm run sync:assets`). The copies are gitignored; the originals are the
   source of truth.
2. **`/results`** (`src/pages/results.astro`) — renders the canonical computed
   numbers from `/data/summary.json` at build time (`src/lib/simdata.ts`).
3. **`/figures`** (`src/pages/figures.astro`) — gallery of the generated PNGs,
   each linked to the chapter it backs.
4. Interactive tools can **fetch the Python data** at runtime to overlay it on
   their JS curves — e.g. the CRLB explorer overlays `/data/crlb_vs_range.csv`,
   demonstrating the TypeScript `physics.ts` and the NumPy `emtrack` agree.

To refresh after changing the sims: `cd simulations && python3 run_all.py`,
commit the new `/figures` + `/data`, then rebuild (the copy step picks them up).

## Local development

```bash
cd dashboard
npm install
npm run dev        # http://localhost:4321/emt_study
npm run build      # static output -> dashboard/dist
npm run preview
```

## Deployment

`/.github/workflows/deploy.yml` builds this app and publishes `dashboard/dist`
to GitHub Pages on pushes to `main` (and via manual dispatch). To enable:
**Settings → Pages → Build and deployment → Source: GitHub Actions.**

The site is configured for a project page at
`https://neilq1810.github.io/emt_study` (`site`/`base` in `astro.config.mjs`).
Update those if the owner/repo changes.

## Roadmap (Phase 6)

This is the scaffold. Planned interactive modules (Astro islands using
D3/Plotly/Three.js) per the project brief:
dipole-field visualizer · coil-geometry explorer · 5/6-DOF demo · noise-budget
calculator · ADC explorer · DSP-pipeline & lock-in simulators · Kalman explorer ·
CRLB / Monte-Carlo uncertainty · distortion & eddy-current visualizers · solver
visualizer · working-volume optimizer · patent-timeline & vendor-ecosystem maps.
