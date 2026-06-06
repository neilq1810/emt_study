# Chapter 25 — Error Taxonomy, Budgets & Monte Carlo

> **Status:** DRAFT · **Part IX — Error Sources** (the whole of Part IX)
> Assembles the per-stage error contributions established across Parts II–VIII
> into one quantitative model. Citation keys resolve to
> [`../../citations/bibliography.json`](../../citations/bibliography.json).

Every preceding part introduced error: physics (distortion, Ch. 6), sensors
(noise/tolerance, Ch. 15), AFE/ADC (Ch. 16, 18), DSP (crosstalk/leakage,
Ch. 19–20), and the solver's geometric amplification (Ch. 24). This chapter is
where they are **named, classified, propagated, and summed** into a single error
budget — the scorecard (with the latency budget of Ch. 12) by which a design is
judged. We organize errors into **stochastic**, **deterministic**, and
**environmental** classes, give explicit lines for the often-overlooked
mechanisms (including **Barkhausen noise, generator noise, ambient/EM
susceptibility, and bias-reference noise in biased sensors such as TMR**), then
show how to combine them via **sensitivity matrices** and **Monte Carlo**.

---

## 25.1 The three error classes

| Class | Behavior | Removable by… | Enters budget as |
|---|---|---|---|
| **Stochastic** | random, zero-mean, averages with √τ | longer integration, lower-noise design | variance (RSS) |
| **Deterministic** | repeatable bias (tolerance, model mismatch, calibration residual) | calibration | bias (often signed, may not cancel) |
| **Environmental** | depends on surroundings (distortion, interference, motion) | mitigation, mapping, fusion, flagging | bias + variance, context-dependent |

The distinction is operational: **stochastic** error sets the precision floor and
shrinks with averaging; **deterministic** error sets accuracy and must be
*calibrated* (Part X), not averaged; **environmental** error is the wild card that
defeats both unless detected and handled (Ch. 21, 27). A budget that lumps them
together is misleading — the same RMS number means very different things depending
on class.

## 25.2 Stochastic error sources (the noise floor)

These propagate to pose via `noise / (√τ · signal) × ‖J⁻¹‖` (Ch. 15 §15.4,
Ch. 24):

1. **Sensor self-noise.** Coil Johnson noise (Ch. 15 eq. 15.1) or MR/TMR 1/f noise
   (Ch. 14.3.4) [@davies2021; @lenz2006].
2. **Barkhausen noise (magnetic sensors & ferrite cores).** Discrete, irreversible
   domain-wall jumps as magnetization changes produce a *low-frequency, often
   non-Gaussian* noise (and a hysteresis/repeatability component). In GMR/TMR free
   layers this is a principal origin of the **magnetic 1/f noise** — "thermally
   excited hopping of magnetic domain walls" — and it also afflicts
   **ferrite-cored pickup coils** [@davies2021; @lenz2006]. It is distinct from
   electronic/Johnson noise and *cannot* be designed away by the AFE; it is
   mitigated at the *device* level (single-domain or vortex-state free layers,
   longitudinal bias, set/reset flipping, Ch. 14.3.3). Because it is partly
   hysteretic, it straddles the stochastic/deterministic boundary. (conf: high —
   mechanism standard; EMT-specific magnitude to be sourced, see *Open questions*.)
3. **Bias-reference noise in biased sensors (TMR).** Unlike a passive coil, an MTJ
   is **voltage-biased**, and both its sensitivity *and* its noise scale with the
   bias voltage; noise on the **bias/reference** therefore multiplies directly
   into the signal. A notable empirical result is that TMR **detectivity stays
   roughly constant with bias** because sensitivity and noise scale together
   [@monteblanco2021] — so chasing sensitivity via higher bias does *not* by
   itself improve the field-referred floor, and an *unstable* bias injects
   correlated multiplicative error. The practical lesson: a biased sensor needs a
   **low-noise, stable voltage/current reference**, and its noise must appear as
   an explicit budget line absent for passive coils. (conf: med — per
   [@monteblanco2021]; magnitudes device-specific.)
4. **AFE noise.** LNA $e_n$ and $i_n|Z_s|$ (Ch. 16 eq. 16.1), kept below the
   sensor floor [@horowitz_hill].
5. **ADC quantization + thermal.** Below the floor with adequate ENOB/oversampling
   (Ch. 18); dithered to stay white [@walden1999; @ieee1241].
6. **Clock/jitter noise.** Aperture jitter (Ch. 10/18 eq. 18.3) — typically
   negligible at EMT frequencies.

These combine (when independent) in **root-sum-square**; the largest term is the
one to attack.

## 25.3 Deterministic error sources (the bias floor)

1. **Sensor/generator tolerances** — area-turns, axis, inter-element angle
   (Ch. 15 §15.1); mostly removed by per-unit calibration (Ch. 26).
2. **Forward-model mismatch** — dipole vs. real cored generator (Ch. 7 §7.2);
   residual after field-mapping is a bias.
3. **Calibration residual** — the part of (1)–(2) the calibration could not
   capture; the irreducible deterministic floor.
4. **Channel crosstalk / spectral leakage** — FDM filter/nonlinearity leakage
   (Ch. 19 §19.2), non-coherent-sampling leakage (Ch. 20) — *correlated* biases on
   $M_{ij}$.
5. **Thermal drift** — of coil area/core, MR offset, bias reference, and
   electronics gain; drift *after* calibration is the leading recalibration driver
   (Ch. 15 §15.5).
6. **Numerical error** — ill-conditioned solves, finite precision (Ch. 22 §22.4,
   Ch. 24 §24.2).

Deterministic errors do **not** average away and may not cancel across DOF; they
are budgeted as (often signed) biases and propagated through the same Jacobian.

## 25.4 Environmental error sources

1. **Field distortion** — eddy-current (conductors) and ferromagnetic (Ch. 6).
   The dominant environmental term: ferromagnetic/electrical devices in the OR
   can induce translation errors up to **8.4 mm RMS and rotation up to 166°**,
   though they can be identified and kept at distance [@poulin2002].
2. **Ambient EM interference / susceptibility.** Background EM noise from OR
   equipment. Reassuringly, measured *ambient-noise* error (as opposed to
   distortion) can remain **below ~0.15 mm RMS** even in an OR — i.e. broadband
   ambient noise is usually *not* the limiting term; **distorters and
   ferromagnetics are** [@poulin2002; @yaniv2009]. This is the in-situ counterpart
   to the IEC 60601-1-2 immunity requirements (Ch. 17 §17.3) [@iec60601_1_2].
3. **Generator (transmitter-side) noise.** Drive-current noise, power-amplifier
   noise, and excitation **frequency/phase/amplitude instability** modulate the
   *transmitted* field, so the error appears **correlated across all receive
   channels** (it scales the whole coupling matrix), unlike per-channel receiver
   noise. It is bounded by a low-noise, stable drive and a clean reference
   (Ch. 9 §9.4, Ch. 10) and partly cancelled in *ratiometric* schemes that
   normalize sensor output by a monitored drive sample. It deserves an explicit
   budget line because its correlation structure means it does **not** RSS like
   independent receiver noise. (conf: med — correlated-error reasoning is standard;
   EMT-specific magnitudes to be sourced.)
4. **Motion effects** — intra-frame TDM skew (Ch. 19 §19.6) and latency-induced
   dynamic error (Ch. 12 §12.3): ~1 mm at 0.1 m/s with 10 ms latency.
5. **Cable effects** — triboelectric/flex noise, capacitance shift (Ch. 16 §16.3,
   Ch. 17 §17.2).
6. **Synchronization errors** — phase-reference drift in coherent detection
   (Ch. 10).

## 25.5 Sensitivity matrices: propagating to pose

Each error source $p$ maps to pose error through the forward-model Jacobian
(Ch. 23–24):

$$
\delta\mathbf{x} \approx (\mathbf{J}^\top\mathbf{R}^{-1}\mathbf{J})^{-1}\mathbf{J}^\top\mathbf{R}^{-1}\,\frac{\partial h}{\partial p}\,\delta p .
$$

The matrix $\partial h/\partial p$ (the **sensitivity matrix**) tells you *which
error hurts which DOF and where in the volume*. Two structural facts recur:

- The mapping is **pose-dependent and conditioning-weighted** (Ch. 24): the same
  $\delta p$ produces far larger $\delta\mathbf{x}$ in weakly observable / poorly
  conditioned regions (volume edges, near ambiguities).
- **Correlated** sources (generator noise, crosstalk) must be propagated with
  their cross-terms — they can add coherently across channels and so are *not*
  reduced by the channel averaging that tames independent noise.

Stochastic terms combine as variances (covariance addition, RSS); deterministic
terms combine as biases (signed, worst-case or RSS depending on independence);
the result is a per-pose error mean and covariance.

## 25.6 Monte Carlo uncertainty analysis

Linear sensitivity propagation (25.5) is a first-order approximation that breaks
down with strong nonlinearity, non-Gaussian noise (Barkhausen!), ambiguities, or
large distortion. The general tool is **Monte Carlo**:

1. Sample each error source from its modeled distribution (with correct
   correlations — e.g. generator noise common across channels).
2. Run the full forward model + solver (Parts VIII) per sample.
3. Accumulate the pose-error distribution over the working volume.

Monte Carlo captures the **non-Gaussian tails** (outliers from distortion,
ambiguity-induced bimodality) that the CRLB/covariance (Ch. 24) understates, and
validates the linear sensitivity analysis where it is valid. It directly backs the
"Monte Carlo uncertainty" and "error propagation" interactive modules of the
project brief (Phase 5).

## 25.7 Assembling the error budget

The deliverable of Part IX is a **table** with one row per source, each tagged by
class, with its magnitude, its pose-error contribution (via 25.5), and its
combination rule:

| Source | Class | Mechanism (chapter) | Combine as | Mitigation |
|---|---|---|---|---|
| Coil/MR sensor noise | stochastic | Ch. 15, 14.3 | RSS | moment, integration, area |
| Barkhausen / domain noise | stochastic(+hyst.) | Ch. 14.3, 25.2 | RSS (+bias) | single-domain/vortex layer, set/reset |
| Bias-reference noise (TMR) | stochastic(×bias) | 25.2 | RSS, multiplicative | stable low-noise reference |
| AFE / ADC noise | stochastic | Ch. 16, 18 | RSS | keep below sensor floor |
| Tolerance / model mismatch | deterministic | Ch. 7, 15 | bias | calibration (Ch. 26) |
| Crosstalk / leakage | deterministic | Ch. 19, 20 | bias (correlated) | TDM, guard bands, coherent sampling |
| Thermal drift | deterministic | Ch. 15 | bias (drifting) | stability, recalibration |
| Field distortion | environmental | Ch. 6 | bias + outliers | mapping, fusion, flagging (Ch. 27, 21) |
| Ambient EM / susceptibility | environmental | 25.4, Ch. 17 | RSS (usually small) | shielding/band-select, EMC (60601-1-2) |
| Generator noise | environmental | 25.4, Ch. 9 | correlated (not RSS) | low-noise drive, ratiometric |
| Motion / latency | environmental | Ch. 12, 19 | bias (dynamic) | simultaneity, prediction, fusion |
| Cable / sync | environmental | Ch. 16, 17, 10 | bias + noise | cable discipline, coherent ref |

The bottom line is a **per-pose pose-error mean and covariance**, summed by class,
mapped across the working volume — the quantitative answer to "how accurate is
this system, where, and why," and the input to the clinical requirements of
Ch. 29 and the from-scratch design of Ch. 31.

---

## Open questions / to verify
- Source EMT-specific *magnitudes* for Barkhausen, generator-side, and
  bias-reference noise (currently mechanism-cited; magnitudes device/system
  specific). Candidate: dedicated MTJ noise-vs-bias and Barkhausen/vortex
  free-layer studies (arXiv:2103.04750 published version; vortex-state spin-valve
  noise papers).
- Build the Phase-5 Monte Carlo notebook and produce a worked error-budget table
  with numbers for one concrete design (ties Ch. 24 CRLB maps).
- Confirm Poulin & Amiot figures (8.4 mm / 166°; 0.15 mm ambient) against the
  primary text and add the exact measurement conditions [@poulin2002].

## Sources cited
- [@davies2021; @lenz2006] MR/Barkhausen/1f noise mechanisms.
  [@monteblanco2021] TMR bias-voltage/detectivity (bias-reference term).
  [@poulin2002] OR interference & ambient-noise magnitudes. [@yaniv2009] clinical
  environment. [@iec60601_1_2] EMC immunity. [@horowitz_hill; @walden1999;
  @ieee1241] AFE/ADC noise. Propagation/CRLB from Ch. 24.
