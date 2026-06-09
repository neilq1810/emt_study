# Chapter 31 — Building a System From Scratch: An End-to-End Worked Design

> **Status:** DEEPENED (awaiting review) · **Part XIV — Building a System From Scratch** (the whole of
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

**Carrying the SNR number through (the chain that sets σ_B).** The whole design
hinges on one number — the **field-referred noise** σ_B the DSP delivers per
measurement — so let us compute it end-to-end for the catheter sensor:
1. **Coil floor (Ch. 15 eq. 15.1):** $R_s=100\,\Omega$ → $e_n\approx
   1.3\,\text{nV}/\sqrt{\text{Hz}}$.
2. **Bandwidth from integration (Ch. 12, 20):** a boxcar/FFT window $\tau\approx
   5\,\text{ms}$ gives noise bandwidth ENBW $\approx 1/2\tau \approx 100\,\text{Hz}$,
   so the in-band voltage noise is $1.3\,\text{nV}/\sqrt{\text{Hz}}\times\sqrt{100}
   \approx 13\,\text{nV RMS}$ (keep the AFE sensor-limited, §31.4).
3. **Volts → tesla (Faraday, Ch. 5):** $B=V/(N A_\text{eff}\,\omega)$. For a small
   catheter coil $N A_\text{eff}\approx 2\times10^{-3}\,\text{m}^2$ and
   $\omega=2\pi\cdot10\,\text{kHz}$,
   $\sigma_B \approx 13\times10^{-9}/(2\times10^{-3}\cdot 6.28\times10^{4})\approx
   1\times10^{-10}\!-\!1\times10^{-9}\,\text{T}$ — i.e. **~0.1–1 nT**, the larger
   (1 nT) end for the smallest catheter coil, the smaller for a rigid triad.
This is exactly the σ_B the CRLB simulation assumes (Ch. 24, `crlb_vs_range`), so
its predicted accuracy is the one this hardware will deliver — closing the loop
between the design and the feasibility check of §31.1 Step 3.

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

**The worked error budget (carrying numbers through, by class and by location).**
With σ_B ≈ 1 nT from §31.5, the **stochastic** term *is* the CRLB the simulation
computes (Ch. 24): 0.017 mm near, 0.086 mm mid, 0.66 mm at the far edge — the z⁴
range law made concrete (`crlb_vs_range`, Monte-Carlo-confirmed to ~3%, Ch. 24).
The **deterministic** term comes from the Ch. 15 tolerance→pose propagation
(area-turns ÷3 to range, angle to orientation) plus the residual of the field map
(Ch. 26); the **environmental** term is the *post-compensation* distortion residual
(Ch. 27 says compensation buys ~5–10×, not zero) plus generator/ambient. The three
classes are independent, so they combine in root-sum-square (Ch. 25 §25.5):

| Error class (Ch. 25) | Source | Near (0.2 m) | Mid (0.3 m) | Far (0.5 m) |
|---|---|---:|---:|---:|
| Stochastic | coil/AFE/ADC at σ_B≈1 nT = **CRLB** | 0.017 | 0.086 | 0.66 |
| Deterministic | tolerance (Ch. 15) ⊕ calib. residual (Ch. 26) | 0.30 | 0.36 | 0.45 |
| Environmental | post-comp. distortion residual (Ch. 27) ⊕ ambient | 0.40 | 0.50 | 0.60 |
| **RSS total** | $\sqrt{\sigma_\text{sto}^2+\sigma_\text{det}^2+\sigma_\text{env}^2}$ | **0.50** | **0.62** | **0.92** |

(all values mm RMS, illustrative). Two lessons jump out, and both are the book's
recurring thesis:
- **Across most of the volume the tracker's own noise is *not* the limit.** At mid-
  volume the 0.086 mm CRLB is swamped by the 0.36 mm calibration and 0.50 mm
  distortion residuals — halving σ_B (better AFE) moves the 0.62 mm total to
  0.61 mm. *Attack the dominant term* (Ch. 12, 29): here, calibration and
  distortion, not electronics.
- **Only at the far edge does the CRLB take over** — the z⁴ law (Ch. 24) drives
  stochastic to 0.66 mm and the total to 0.92 mm, the binding case against the
  ≤ 1 mm spec. *That* is where generator moment or sensor area-turns (the eq. 8.1
  levers, Ch. 8) buy accuracy; everywhere else they are wasted.
The budget passes (≤ 1 mm everywhere) with margin, and tells you *where* each
design dollar should go. If the measured Hummel residual exceeds these numbers,
the budget is wrong or incomplete — reconcile before shipping.

**The worked latency budget (against the ≤ 20 ms spec).** Latency and accuracy pull
against each other through the integration time τ (the trilemma, Ch. 12): longer τ
lowers σ_B but adds delay. Summing the pipeline (Ch. 11, 18–22):

| Stage | Contribution | Latency |
|---|---|---:|
| Lock-in/FFT integration (τ) | sets σ_B (§31.5) — the dominant term | 5.0 ms |
| Σ-Δ + CIC decimation group delay | Ch. 18, 22 | 1.5 ms |
| FFT/calibration/distortion map | Ch. 11, 19, 26 | 0.5 ms |
| LM solve (closed-form init + bounded iters) | Ch. 23 | 0.5 ms |
| EKF/UKF fusion + covariance output | Ch. 21, 24 | 0.2 ms |
| Transport/display | Ch. 12 | 1.0 ms |
| **Total** | | **≈ 8.7 ms** |

Comfortably inside 20 ms, with the **integration time dominating** — exactly the
trilemma's prediction. The headroom (≈ 11 ms) is the design's *reserve*: it can be
spent on a longer τ (lower far-edge σ_B, helping the 0.92 mm corner above) or on
more solver/filter work, but not both — the budget makes the trade explicit and
quantitative rather than a matter of taste.

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
  outputs — the stochastic column now uses the `crlb_vs_range` sim directly; the
  deterministic/environmental columns are illustrative and should be backed by a
  tolerance Monte Carlo and a measured distortion-residual map.
- Source a survey of open-source EMT implementations for §31.8 (currently conf:
  low).
- ✅ **Done:** worked numeric error budget (by class, mapped across the volume,
  RSS) and latency budget (§31.6), tied to the CRLB sim (Ch. 24) and the trilemma
  (Ch. 12). Remaining: validate the two non-stochastic columns against measurement.

## Sources cited
- [@iec60601_1; @iec60601_1_2] safety/EMC. [@walden1999; @ieee1241] ADC.
  [@scofield1994] lock-in. [@marquardt1963] LM. [@kalman1960; @julier2004]
  filtering. [@kindratenko2000; @kindratenko2005; @cavaliere2023] calibration/
  compensation. [@hummel2005] verification. All subsystem physics from Parts II–X.
