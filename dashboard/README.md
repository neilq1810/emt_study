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
