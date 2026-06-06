// Client-side physics for the interactive tools. Mirrors the validated
// `simulations/emtrack` library (Ch. 4, 5, 15, 20, 24) so the web modules and
// the Python results agree. Pure functions, no dependencies.

export const MU0 = 4e-7 * Math.PI; // [H/m]
export const KB = 1.380649e-23; // Boltzmann [J/K]

export type Vec3 = [number, number, number];

/** Point magnetic-dipole field B(r) [T] (Ch. 4, eq. 4.1). */
export function dipoleField(m: Vec3, r: Vec3): Vec3 {
  const rr = Math.hypot(r[0], r[1], r[2]);
  if (rr === 0) return [NaN, NaN, NaN];
  const rh: Vec3 = [r[0] / rr, r[1] / rr, r[2] / rr];
  const mdotr = m[0] * rh[0] + m[1] * rh[1] + m[2] * rh[2];
  const c = MU0 / (4 * Math.PI) / (rr * rr * rr);
  return [
    c * (3 * mdotr * rh[0] - m[0]),
    c * (3 * mdotr * rh[1] - m[1]),
    c * (3 * mdotr * rh[2] - m[2]),
  ];
}

export function bMag(b: Vec3): number {
  return Math.hypot(b[0], b[1], b[2]);
}

/**
 * On-axis CRLB position uncertainty (Ch. 24). Closed-form law fitted to (and
 * matching) the full Fisher-information computation in `simulations/run_all.py`:
 * sigma_pos = C * sigma_B * z^4 / m, with C calibrated at z=0.3 m.
 * Returns metres. (Triad/triad geometry, on-axis.)
 */
const CRLB_C = 1.0628e7;
export function crlbPositionSigma(z: number, sigmaB: number, moment: number): number {
  return (CRLB_C * sigmaB * Math.pow(z, 4)) / moment;
}

/** Johnson–Nyquist voltage-noise density [V/sqrt(Hz)] (Ch. 15, eq. 15.1). */
export function johnsonNoise(R: number, T: number): number {
  return Math.sqrt(4 * KB * T * R);
}

/** Induced-EMF amplitude on a pickup coil [V] (Ch. 5, eq. 5.2). */
export function inducedEmf(turns: number, area: number, freq: number, bField: number): number {
  return turns * area * 2 * Math.PI * freq * bField;
}

/** Quadrature lock-in amplitude estimate from samples (Ch. 20, eq. 20.1). */
export function lockIn(samples: number[], f0: number, fs: number): { amp: number; phase: number } {
  let X = 0;
  let Y = 0;
  for (let k = 0; k < samples.length; k++) {
    const w = (2 * Math.PI * f0 * k) / fs;
    X += samples[k] * Math.cos(w);
    Y += samples[k] * Math.sin(w);
  }
  X = (2 * X) / samples.length;
  Y = (2 * Y) / samples.length;
  return { amp: Math.hypot(X, Y), phase: Math.atan2(Y, X) };
}

/** Box–Muller Gaussian sample. */
export function gauss(rng: () => number = Math.random): number {
  const u = 1 - rng();
  const v = rng();
  return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
}
