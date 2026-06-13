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
  {
    file: 'ch29_deep_volume_crlb.png',
    title: 'Deep-volume CRLB & the moment lever',
    chapter: 'Ch. 29 §29.10',
    chapterSlug: 'part-12-medical-applications/29-clinical-applications-workflows',
    caption: 'Usable depth vs transmit moment: σ ∝ 1/m_t so z_max ∝ m_t^0.25 — a 16× moment buys only ~2× depth.',
  },
  {
    file: 'ch33_distortion_flag_roc.png',
    title: 'Dynamic-distortion flag ROC',
    chapter: 'Ch. 33 §33.9',
    chapterSlug: 'part-16-performance-characterization/33-characterization-benchmarking',
    caption: 'Single-residual flag vs pose error as a distorter approaches; the detection margin can go negative for pose-mimicking distortion.',
  },
  {
    file: 'ch08_system_block_diagram.png',
    title: 'EMT system signal chain (schematic)',
    chapter: 'Ch. 8',
    chapterSlug: 'part-03-tracker-architecture/08-system-architecture',
    caption: 'Schematic: field generator → sensor → AFE/ADC → DSP → pose solver → fusion → display, with clock/sync and the detect-and-flag path.',
  },
  {
    file: 'ch05_coupling_geometry.png',
    title: 'Transmitter–sensor coupling geometry (schematic)',
    chapter: 'Ch. 5',
    chapterSlug: 'part-02-electromagnetic-theory/05-coupling-mutual-inductance',
    caption: 'Schematic: dipole field, the position vector r, the field B(r), the sensor axis n̂, and the angle θ; V ∝ n̂·B, |B| ∝ m_t/r³.',
  },
  {
    file: 'ch06_distortion_mechanism.png',
    title: 'Eddy-current distortion mechanism (schematic)',
    chapter: 'Ch. 6',
    chapterSlug: 'part-02-electromagnetic-theory/06-distortion-physics',
    caption: 'Schematic: the primary field induces eddy currents in a conductor whose secondary field adds to the sensor reading (the distortion).',
  },
  {
    file: 'ch19_excitation_schemes.png',
    title: 'Excitation / channel-separation schemes (schematic)',
    chapter: 'Ch. 19',
    chapterSlug: 'part-07-dsp/19-excitation-channel-separation',
    caption: 'Schematic waveforms: TDM (one axis at a time), FDM (simultaneous tones), and pulsed-DC (energize, wait for eddy settling, sample).',
  },
  {
    file: 'ch24_hemisphere_ambiguity.png',
    title: 'Dipole hemisphere / parity ambiguity (schematic)',
    chapter: 'Ch. 24 §24.7',
    chapterSlug: 'part-08-position-solvers/24-conditioning-observability-uncertainty',
    caption: 'A sensor at +r and its mirror at −r give identical measurements (K ∝ r̂r̂ᵀ is invariant under r̂→−r̂); resolved by an asymmetric generator, a half-space prior, continuity, or fusion.',
  },
  {
    file: 'ch13_roll_null.png',
    title: 'The 5-DOF roll null and its dual-coil fix (schematic)',
    chapter: 'Ch. 13',
    chapterSlug: 'part-04-sensor-engineering/13-sensor-physics-geometries',
    caption: 'Roll about a single coil axis is unobservable (rank-deficient J); a second askew element makes it observable ∝ sin θ.',
  },
  {
    file: 'ch48_design_controls.png',
    title: 'Design controls: the V&V V-model (schematic)',
    chapter: 'Ch. 48',
    chapterSlug: 'part-20-dependability-compliance/48-regulatory-pathways-quality-systems',
    caption: 'User needs → inputs → outputs → implementation → verification → validation → released device + DHF; verification = "built it right", validation = "built the right thing".',
  },
  {
    file: 'ch46_error_ellipsoid.png',
    title: 'Navigation-confidence error ellipsoid (schematic)',
    chapter: 'Ch. 46 §46.6',
    chapterSlug: 'part-20-dependability-compliance/46-human-factors-usability',
    caption: 'Display the 95% ellipsoid from the marginalized 6-DOF covariance (×2.95 the naive block, §24.6), a tool-axis cone, and a τ-relative GREEN/AMBER/RED state.',
  },
  {
    file: 'ch55_twin_identification.png',
    title: 'Calibration as twin identification',
    chapter: 'Ch. 55',
    chapterSlug: 'part-23-digital-twin/55-twin-identification-calibration',
    caption: 'Pose-error histogram before/after identifying ±5% gain errors from known golden-fixture poses: 14.9 mm → 0.11 mm (132×) — the calibration cliff, closed as method.',
  },
];
