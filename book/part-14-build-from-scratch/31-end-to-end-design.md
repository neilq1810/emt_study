# Chapter 31 — Building a System From Scratch: An End-to-End Worked Design

> **Status:** DRAFT · **Part XIV — Building a System From Scratch** (the whole of
> Part XIV) — the capstone. Synthesizes Parts II–X into one design loop. Citation
> keys resolve to [`../../citations/bibliography.json`](../../citations/bibliography.json).

This chapter is the payoff: a single worked example that walks the full design of
a 6-DOF AC electromagnetic tracker from requirements to validation, **carrying
numbers through** so each decision is traceable to the physics and budgets of the
preceding parts. It is deliberately concrete — a benchtop/OEM-medical-class
tracker — but the *method* generalizes. Numbers here are illustrative design
targets consistent with the worked examples earlier in the book (Ch. 4 §4.7,
Ch. 15, Ch. 24); they are *not* product specifications, and every "≈" invites the
reader to redo the arithmetic for their own requirement.

---

## 31.1 Requirements capture and architecture selection

**Step 1 — write the requirement as numbers.** Suppose:

| Spec | Target | Drives… |
|---|---|---|
| Working volume | 0.5 m cube | generator moment (Ch. 9) |
| Static position accuracy | ≤ 1 mm RMS (mid-volume) | noise budget + CRLB (Ch. 24, 25) |
| Orientation | 6-DOF, ≤ 0.5° | sensor geometry (Ch. 13) |
| Update rate | ≥ 100 Hz | multiplexing + integration (Ch. 10, 12) |
| Latency | ≤ 20 ms | latency budget (Ch. 12) |
| Environment | lab/IR room, some metal | excitation choice + compensation (Ch. 6, 27) |
| Sensor size | catheter-compatible option | sensor tech (Ch. 14) |

**Step 2 — choose the architecture** against the AC/pulsed-DC fork (Ch. 8 §8.2).
For a small passive catheter-scale sensor with high update rate, **AC excitation
with pickup coils** is the natural choice (sensitivity ∝ ω buys SNR, Ch. 5;
smallest passive sensors, Ch. 14) — accepting greater conductive-distortion
sensitivity (Ch. 6) to be managed by compensation/fusion (Ch. 27, 21). If the
dominant threat were *conductive* clutter and the sensor could be a magnetometer,
pulsed-DC would compete. We proceed AC, **FDM** excitation (three axes
simultaneous for update rate, Ch. 10/19), large-transmitter/small-sensor topology
(reciprocity, Ch. 5 §5.5).

**Step 3 — pre-build feasibility via CRLB.** Before committing, evaluate the
Cramér–Rao bound (Ch. 24 eq. 24.1) over the volume for the candidate
generator/sensor — this predicts whether ≤1 mm is even achievable at the noise
budget below, and *where* in the volume it degrades (edges, Ch. 24 §24.2). This is
the cheapest design iteration; do it first.

## 31.2 Field generator design

**Moment from the range law.** The worst-case (far, equatorial) field must clear
the sensor/AFE noise floor. From Ch. 4 §4.7, a moment $m_t = 1\,\text{A·m}^2$
gives $|\mathbf B|\approx 0.8\,\mu\text{T}$ at $r=0.5\,\text{m}$ equatorial. Take
$m_t \approx 1$–$5\,\text{A·m}^2$ as the starting point and refine against the SNR
budget (§31.4–31.5). Realize it with $m_t=N_tI_tA_t$ (Ch. 9 §9.1): e.g. $N_t=100$,
$A_t=10^{-3}\,\text{m}^2$, $I_t=10\,\text{A}$ → $m_t=1$; a **ferrite core**
multiplies moment but adds the cored-radiator modeling burden (Ch. 7 §7.2,
calibrate it).

**Geometry.** Orthogonal transmitter triad (Ch. 9 §9.2) for the clean $3\times3$
coupling (Ch. 5 §5.4), or a **planar multi-coil generator** for the under-table
medical form factor (calibrate the non-dipole field, Ch. 7/26). Keep the sensor
beyond ~5–10 coil radii so the dipole model holds (Ch. 4 §4.6), or commit to a
mapped forward model.

**Drive.** DDS reference → power amplifier into the (optionally resonant) coil
(Ch. 9 §9.4), three FDM frequencies $f_1,f_2,f_3$ in a low-distortion band (a few
to ~15 kHz) with guard bands (Ch. 10/19). **Monitor the drive current** for
ratiometric rejection of generator-side noise (Ch. 25 §25.4).

## 31.3 Sensor design

**DOF → geometry (Ch. 13).** For 6-DOF, either an **orthogonal coil triad** (rigid
instruments) or **two askew coils** (catheter); for the smallest 5-DOF option, a
single elongated ferrite-cored coil (length 10–20× diameter, Ch. 14.1).

**Sensitivity.** Maximize $N_sA_{s,\text{eff}}$ within the size budget; a
ferrite core boosts effective area. Self-resonance with parasitic + cable
capacitance bounds the upper frequency (Ch. 15 §15.3) — keep $f_3$ safely below
it.

**Noise floor (Ch. 15).** For an example coil $R_s=100\,\Omega$ at 300 K, Johnson
noise ≈ 1.3 nV/√Hz (Ch. 15 eq. 15.1). This is the number the AFE must preserve. If
instead a **TMR-bridge** sensor were chosen (DC-capable, chip-scale), the floor is
the 1/f/Barkhausen detectivity with a stable bias reference (Ch. 14.3, Ch. 25
§25.2) — a different budget, evaluated the same way.

## 31.4 Analog front end (AFE) design

**Noise budget (Ch. 16).** With an inductive source $Z_s=R_s+j\omega L_s$, the
$i_n|Z_s|$ term often dominates (Ch. 16 §16.1), so pick the first-stage LNA to
add ≲ 0.6 nV/√Hz input-referred at the operating frequency — keeping the system
**sensor-limited** (the design goal). Choose bipolar (low $e_n$) vs. JFET (low
$i_n$) by comparing $R_{s,\text{opt}}=e_n/i_n$ to $|Z_s|$ at $f$ (Ch. 16 §16.1).

**Dynamic range (Ch. 16 §16.4).** The $1/r^3$ law gives ~60 dB across the volume;
budget ~100–120 dB end-to-end with **PGA/auto-ranging** + a high-ENOB ADC, and
**never clip** the strong near-field axis (a clip corrupts the whole coupling
matrix, Ch. 11).

**Differential + CMRR (Ch. 16 §16.2).** Instrumentation-amp front end with high AC
CMRR at the excitation band to reject mains and capacitive pickup.

**EMC/safety (Ch. 17).** Slotted electrostatic shield (shield E, not B);
star ground; guarded high-impedance inputs; for a patient sensor, **galvanic
isolation** meeting IEC 60601-1 Type CF leakage (10/50 µA) [@iec60601_1], inside
the IEC 60601-1-2 EMC envelope with pose-defined essential performance
[@iec60601_1_2].

## 31.5 Data conversion and DSP implementation

**ADC (Ch. 18).** A **Σ-Δ** converter, 20–24 bit, oversampled and coherently
clocked to the excitation (Ch. 10/18) — covering most of the dynamic range
digitally, relaxing the anti-alias filter, and giving exact single-bin
amplitudes. Budget the decimation group delay into latency (Ch. 12). (For very
fast TDM one might prefer SAR, but we chose FDM.) [@walden1999; @ieee1241]

**DSP pipeline (Ch. 11, 19–22).**
1. **Channel separation + amplitude estimation:** an **FFT** (or three lock-ins)
   recovers all nine $M_{ij}$ from the FDM tone set in one transform (Ch. 19/20);
   integration time $\tau$ set by the SNR-vs-rate trade — e.g. $\tau\approx
   5$–10 ms to hit ≥100 Hz with margin (Ch. 12). [@scofield1994]
2. **Calibration:** apply per-channel gain/phase, sensor constants, frequency-
   dependent corrections, and the field/distortion map (Ch. 26–27).
3. **Solve:** closed-form $\mathbf M^\top\mathbf M$ initializer → **Levenberg–
   Marquardt** refine on $SO(3)$ (Ch. 23), bounded iterations (Ch. 22).
   [@marquardt1963]
4. **Estimate/fuse:** **EKF/UKF** with a motion model (Ch. 21); add IMU for
   low-latency/roll and **distortion detection** via EM/IMU disagreement (Ch. 21,
   27). [@kalman1960; @julier2004]
Output **timestamped pose + covariance** (Ch. 11, 24).

**Hardware partition (Ch. 22).** FFT/lock-in + decimation on **FPGA** (fixed-point,
deterministic); calibration + LM + filter on an **embedded CPU** (floating-point);
GPU only if many sensors/particles. Verify worst-case latency ≤ 20 ms and
bit-exact datapath (Ch. 22 §22.6).

## 31.6 Calibration, validation & verification

**Calibrate (Ch. 26).** Per-unit sensor characterization (area-turns, axes,
geometry; TMR bias/sensitivity if used); cored-generator field mapping; system
field map over the volume against CMM/robot/optical ground truth; choose
representation (interpolation vs. polynomial vs. NN) by the residual-vs-sampling
trade [@kindratenko2000; @kindratenko2005].

**Compensate distortion (Ch. 27).** Map static installation distortion; add
witness sensors and/or EM-IMU fusion for moving distorters; **detect-and-flag**
when compensation is exceeded (never trust a distorted reading silently)
[@cavaliere2023].

**Validate/verify (Ch. 26 §26.5).** Measure residual accuracy with the **Hummel
protocol** (and a dynamic/distortion extension), on data **independent of the
calibration set** [@hummel2005]. Build the **error budget** (Ch. 25): stochastic
(coil/AFE/ADC, incl. Barkhausen/bias-reference if MR), deterministic (tolerance/
mismatch/calibration residual), environmental (distortion/generator/ambient/
motion), summed by class and mapped across the volume — then confirm it predicts
the measured residual. If the measured error exceeds the budget, the budget is
wrong or incomplete; reconcile before shipping.

## 31.7 Manufacturing and regulatory pathway

**Manufacturing (Ch. 15 §15.5).** Design for reproducibility (so factory
calibration scales) and thermal/mechanical stability (so calibration stays
valid); characterize and document variation for the error budget and regulatory
file.

**Regulatory (Ch. 29 §29.7).** Define **essential performance** in pose terms
("≤ X mm or flag"); meet IEC 60601-1 / -1-2 [@iec60601_1; @iec60601_1_2]; assemble
V&V, risk management, and standardized-assessment evidence [@hummel2005] for FDA
510(k)/PMA or CE/MDR. The fault behavior (flag-and-degrade, Ch. 22/27) is part of
the safety case, not an add-on.

## 31.8 Reference implementation & open-source ecosystem

A teaching/reference build (and a target for this repository's `simulations/` and
`dashboard/`):

- **Forward model** (dipole + cored/mapped) and **CRLB map** (Ch. 5, 7, 24).
- **DSP**: FDM synth, lock-in/FFT amplitude estimation, LM solver, EKF/UKF
  (Ch. 19–23).
- **Monte Carlo error/uncertainty** harness (Ch. 24–25) feeding the planned
  interactive modules (dipole visualizer, noise-budget calculator, solver/Kalman
  explorers, distortion/eddy simulators).
- Open building blocks exist (e.g. open-source EM-tracker projects, Ch. 5
  references); a fully open, validated medical-grade stack remains an
  opportunity (Ch. 30). (conf: low — ecosystem maturity; survey to be sourced.)

## 31.9 The design loop, in one paragraph

Write the requirement as numbers → pick the architecture (AC/pulsed-DC, sensor
type, multiplexing) → size the **generator moment** from the range law and the
**noise budget** so the system is sensor-limited → check feasibility with the
**CRLB** before building → design AFE/ADC to preserve the sensor floor across
~100 dB → implement coherent **lock-in + LM + Kalman/fusion** within the latency
budget → **calibrate, compensate, and verify** against an independent standard and
the **error budget** → wrap in **safety/EMC/regulatory** with honest, flagged
uncertainty. Every arrow is a chapter; every number traces to physics. *That* is
designing an electromagnetic tracker from first principles.

---

## Open questions / to verify
- Turn this chapter into an **executable** reference design (Phase 5 notebooks +
  Phase 6 interactive tools) and back-annotate the numbers with simulation
  outputs (CRLB maps, Monte Carlo residuals).
- Source a survey of open-source EMT implementations for §31.8 (currently conf:
  low).
- Provide a fully worked numeric error budget + latency budget for this example
  (ties Ch. 12, 25) as a table once the simulations exist.

## Sources cited
- [@iec60601_1; @iec60601_1_2] safety/EMC. [@walden1999; @ieee1241] ADC.
  [@scofield1994] lock-in. [@marquardt1963] LM. [@kalman1960; @julier2004]
  filtering. [@kindratenko2000; @kindratenko2005; @cavaliere2023] calibration/
  compensation. [@hummel2005] verification. All subsystem physics from Parts II–X.
