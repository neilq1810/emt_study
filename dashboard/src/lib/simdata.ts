// Build-time loader for the Phase-5 simulation outputs (repo-root /data and
// /figures, produced by simulations/run_all.py). Read in .astro frontmatter only.
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

const DATA = resolve(process.cwd(), '..', 'data');

export function loadJson<T = unknown>(name: string): T | null {
  try {
    return JSON.parse(readFileSync(resolve(DATA, name), 'utf8')) as T;
  } catch {
    return null;
  }
}

/** Parse a simple CSV (header + numeric rows) into objects. */
export function loadCsv(name: string): Record<string, string>[] {
  try {
    const text = readFileSync(resolve(DATA, name), 'utf8').trim();
    const [head, ...rows] = text.split(/\r?\n/);
    const cols = head.split(',');
    return rows.map((r) => {
      const vals = r.split(',');
      return Object.fromEntries(cols.map((c, i) => [c, vals[i]]));
    });
  } catch {
    return [];
  }
}

export interface FigureMeta {
  file: string;
  title: string;
  chapter: string;
  chapterSlug: string; // book route id
  caption: string;
}

// Manifest of generated figures, each tied to the chapter it backs.
export const FIGURES: FigureMeta[] = [
  {
    file: 'ch04_dipole_field.png',
    title: 'Magnetic dipole field',
    chapter: 'Ch. 4 — Maxwell & the dipole',
    chapterSlug: 'part-02-electromagnetic-theory/04-maxwell-dipole',
    caption: 'Streamlines of the point-dipole field (m ∥ z); the 1/r³ falloff and 2:1 axis/equator anisotropy are visible.',
  },
  {
    file: 'ch04_dipole_vs_loop_error.png',
    title: 'Dipole-approximation error vs distance',
    chapter: 'Ch. 4 §4.6',
    chapterSlug: 'part-02-electromagnetic-theory/04-maxwell-dipole',
    caption: 'Max error of the point-dipole model vs the exact finite loop; log–log slope confirms the (a/r)² scaling.',
  },
  {
    file: 'ch06_skin_depth.png',
    title: 'Skin depth vs frequency',
    chapter: 'Ch. 6 §6.2',
    chapterSlug: 'part-02-electromagnetic-theory/06-distortion-physics',
    caption: 'δ = 1/√(πfμσ) for Cu/Al/stainless; Cu reaches 0.66 mm at 10 kHz (vs ~7 m in tissue).',
  },
  {
    file: 'ch06_pulsed_dc_settling.png',
    title: 'Pulsed-DC eddy settling',
    chapter: 'Ch. 6 §6.4',
    chapterSlug: 'part-02-electromagnetic-theory/06-distortion-physics',
    caption: 'Illustrative single-τ eddy-decay model: residual error vs sample delay (sets the pulsed-DC wait).',
  },
  {
    file: 'ch20_lockin_snr_vs_T.png',
    title: 'Lock-in error vs integration time',
    chapter: 'Ch. 20 §20.2',
    chapterSlug: 'part-07-dsp/20-synchronous-detection-filtering',
    caption: 'Amplitude error ∝ T^−0.49 (≈ 1/√T) even with the signal buried 5× under noise.',
  },
  {
    file: 'ch13_dual_coil_observability.png',
    title: 'Dual-coil roll observability vs axis angle',
    chapter: 'Ch. 13 §13.3',
    chapterSlug: 'part-04-sensor-engineering/13-sensor-physics-geometries',
    caption: 'Roll observability of a two-coil 6-DOF sensor: ~0 when the coil axes are parallel, maximal (∝ sin θ) at 90°.',
  },
  {
    file: 'ch24_crlb_map.png',
    title: 'CRLB position-uncertainty map',
    chapter: 'Ch. 24 §24.5',
    chapterSlug: 'part-08-position-solvers/24-conditioning-observability-uncertainty',
    caption: 'CRLB position σ over the working volume (σ_B = 1 nT); best near the generator, degrading toward the edges.',
  },
  {
    file: 'ch24_crlb_vs_range.png',
    title: 'CRLB vs range (z⁴ law)',
    chapter: 'Ch. 24 §24.5',
    chapterSlug: 'part-08-position-solvers/24-conditioning-observability-uncertainty',
    caption: 'On-axis CRLB σ vs range; fitted exponent 4.0 — accuracy degrades as the fourth power of distance.',
  },
];
