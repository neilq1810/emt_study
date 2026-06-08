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

/** On-axis field of an N-turn circular loop [T] (Ch. 4, eq. 4.3). */
export function loopFieldOnAxis(current: number, radius: number, z: number, turns = 1): number {
  return (MU0 * turns * current * radius * radius) / (2 * Math.pow(radius * radius + z * z, 1.5));
}

/** Magnetic skin depth [m] (Ch. 6, eq. 6.1): δ = 1/√(π f μ₀ μ_r σ). */
export function skinDepth(freq: number, sigma: number, muR = 1): number {
  return 1 / Math.sqrt(Math.PI * freq * MU0 * muR * sigma);
}

/** Magnetic moment of an N-turn loop [A·m²]. */
export function momentOfLoop(turns: number, current: number, radius: number): number {
  return turns * current * Math.PI * radius * radius;
}

// --- ADC figures of merit (Ch. 18) ---
/** Ideal quantization SNR for an N-bit converter [dB] (eq. 18.1). */
export function adcSnrIdeal(bits: number): number {
  return 6.02 * bits + 1.76;
}
/** ENOB from a measured SINAD [dB] (eq. 18.2). */
export function enobFromSinad(sinad: number): number {
  return (sinad - 1.76) / 6.02;
}
/**
 * Quantization-SNR gain from oversampling + L-th-order noise shaping [dB]:
 * (6L+3) dB per octave of OSR. L=0 gives plain oversampling (~3 dB/octave).
 */
export function oversamplingGainDb(osr: number, order: number): number {
  return (6 * order + 3) * Math.log2(Math.max(osr, 1));
}

/**
 * Inverse of the on-axis CRLB law: maximum range where position σ stays below a
 * target (Ch. 24 / working-volume optimizer). target in metres, returns metres.
 */
export function crlbMaxRange(targetSigma: number, sigmaB: number, moment: number): number {
  const C = 1.0628e7;
  return Math.pow((targetSigma * moment) / (C * sigmaB), 0.25);
}

// --- Position-only forward model & 3×3 Fisher/CRLB (Ch. 23/24) ---
// Measurement = the three transmit dipoles' field vectors at p (sensor
// orientation = identity), i.e. a 9-vector. Position is the 3-DOF unknown.

export function fieldMeasurement(p: Vec3, moment = 1): number[] {
  return [
    ...dipoleField([moment, 0, 0], p),
    ...dipoleField([0, moment, 0], p),
    ...dipoleField([0, 0, moment], p),
  ];
}

/** Numerical 9×3 Jacobian dh/dp (rows = 9 measurements, cols = x,y,z). */
export function jacobian9x3(p: Vec3, moment = 1, eps = 1e-7): number[][] {
  const J: number[][] = [];
  const h0 = fieldMeasurement(p, moment);
  for (let i = 0; i < 9; i++) J.push([0, 0, 0]);
  for (let k = 0; k < 3; k++) {
    const pp: Vec3 = [...p] as Vec3;
    pp[k] += eps;
    const hk = fieldMeasurement(pp, moment);
    for (let i = 0; i < 9; i++) J[i][k] = (hk[i] - h0[i]) / eps;
  }
  return J;
}

/** Symmetric 3×3 from JᵀJ / σ². */
export function fisher3(J: number[][], sigma: number): number[][] {
  const F = [[0, 0, 0], [0, 0, 0], [0, 0, 0]];
  for (let a = 0; a < 3; a++)
    for (let b = 0; b < 3; b++) {
      let s = 0;
      for (let i = 0; i < 9; i++) s += J[i][a] * J[i][b];
      F[a][b] = s / (sigma * sigma);
    }
  return F;
}

/** Inverse of a 3×3 matrix (returns null if singular). */
export function invert3(M: number[][]): number[][] | null {
  const [a, b, c] = M[0], [d, e, f] = M[1], [g, h, i] = M[2];
  const A = e * i - f * h, B = -(d * i - f * g), C = d * h - e * g;
  const det = a * A + b * B + c * C;
  if (Math.abs(det) < 1e-300) return null;
  const id = 1 / det;
  return [
    [A * id, (c * h - b * i) * id, (b * f - c * e) * id],
    [B * id, (a * i - c * g) * id, (c * d - a * f) * id],
    [C * id, (b * g - a * h) * id, (a * e - b * d) * id],
  ];
}

export function matVec3(M: number[][], v: Vec3): Vec3 {
  return [
    M[0][0] * v[0] + M[0][1] * v[1] + M[0][2] * v[2],
    M[1][0] * v[0] + M[1][1] * v[1] + M[1][2] * v[2],
    M[2][0] * v[0] + M[2][1] * v[1] + M[2][2] * v[2],
  ];
}

/** Full 3×3 CRLB covariance at pose p for field-referred noise σ (Ch. 24). */
export function crlbCov3(p: Vec3, sigma: number, moment = 1): number[][] | null {
  return invert3(fisher3(jacobian9x3(p, moment), sigma));
}

