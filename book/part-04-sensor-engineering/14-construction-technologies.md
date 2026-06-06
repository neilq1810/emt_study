# Chapter 14 — Sensor Construction, Miniaturization & Technologies

> **Status:** DRAFT · **Part IV — Sensor Engineering**
> Builds on Ch. 13 (sensing principles & DOF). Noise/tolerance detail in Ch. 15.
> Citation keys resolve to [`../../citations/bibliography.json`](../../citations/bibliography.json).

Chapter 13 settled *what* a sensor measures and *how many DOF* a given geometry
yields. This chapter is about *how the sensor is physically built* — the
technologies, their trade-offs, and the brutal miniaturization constraints of
medical use. We cover induction coils (the clinical workhorse), then the
**solid-state magnetoresistive family — AMR, GMR, and TMR — with particular
attention to TMR Wheatstone-bridge sensors**, their noise, and why direct field
sensors are reshaping the design space, especially for pulsed-DC and chip-scale
systems. We close with a sensor-selection matrix.

---

## 14.1 Induction coils: wire-wound, PCB, and thin-film

The induction coil's signal is $\varepsilon = N_s A_s\,\omega\,(\mathbf B\!\cdot\!\hat{\mathbf n}_s)$
(Ch. 5). The whole craft is maximizing the **sensitivity area-turns product
$N_sA_s$** within a size budget, while controlling self-resonance and noise
(Ch. 15).

- **Wire-wound coils.** Fine magnet wire on a former (often a high-$\mu_r$
  ferrite core to multiply effective $A_s$). The clinical standard: "miniature
  inductive coils are the gold standard" for passive sensing [@yaniv2009]. To
  fit a catheter, coils are **elongated** — typical length 10–20× the diameter —
  trading a long thin cross-section for usable area-turns at sub-millimeter
  diameter (conf: med — reported design ratio for elongated EMT sensors). A
  ferrite core both boosts signal and defines the sensitive axis.
- **PCB / planar coils.** Spiral traces on (multilayer) PCB. Highly
  reproducible, cheap at volume, and easy to make *orthogonal triads* by
  stacking/arranging layers — but limited area-turns and thus lower sensitivity
  than wire-wound for a given footprint. Common in larger sensors and reference
  coils.
- **Thin-film / MEMS-fabricated coils.** Wafer-level microcoils for extreme
  miniaturization and batch reproducibility; sensitivity is small (tiny $A_s$),
  so they suit short-range or high-field applications.

The core limitation of *all* coils for tracking is the $\omega$-dependence: they
are blind at DC, so they cannot serve pulsed-DC architectures, and at the low
AC frequencies chosen to limit eddy distortion (Ch. 6) the sensitivity penalty
must be recovered with area-turns or generator moment.

## 14.2 Catheter, needle, and implantable sensors

Medical integration imposes constraints unlike any other tracking domain:

- **Diameter** measured in fractions of a millimeter (to fit working channels /
  needle lumens); the smallest commercial 5-DOF coil sensors are ~0.3 mm
  diameter [@ndi_aurora] (conf: med — vendor-reported).
- **Biocompatibility & sterilization** (autoclave/EtO/gamma) — limits materials
  and adhesives.
- **Cable management.** A coil needs leads; cable flex, triboelectric noise, and
  cable-induced errors are real (flagged in Part IX). Wireless/passive sensing
  is attractive but constrained (Ch. 10 sync).
- **Tip offset.** The sensor is rarely *at* the functional tip; a known
  sensor-to-tip transform propagates sensor pose error to tip error — e.g. a
  ~115 mm offset turns ~1 mm/0.01 rad sensor accuracy into ~2.5 mm tip accuracy
  (conf: med — illustrative figure from catheter-sensor design literature). This
  is a systems-level lesson: *miniaturization and placement are accuracy
  decisions, not just mechanical ones.*

## 14.3 Solid-state magnetic field sensors — the magnetoresistive family

Magnetoresistive (MR) sensors change electrical resistance with applied field
and respond **down to DC**. They are silicon-compatible, tiny, low-power, and
arrayable — and increasingly relevant to EMT for pulsed-DC, chip-scale, and
multi-sensor architectures. The family, in order of historical and performance
development [@lenz2006; @davies2021]:

### 14.3.1 AMR, GMR, and TMR — physics and comparison
- **AMR (anisotropic magnetoresistance).** Resistance depends on the angle
  between current and magnetization in a ferromagnet; MR ratio a few percent.
  Mature, low noise, moderate sensitivity; needs set/reset (§14.3.3).
- **GMR (giant magnetoresistance).** Spin-dependent scattering in
  ferromagnet/spacer multilayers or spin valves; MR ratio ~10–20%. Higher
  sensitivity than AMR; smaller linear range.
- **TMR (tunneling magnetoresistance).** A **magnetic tunnel junction (MTJ)**:
  two ferromagnetic layers separated by a thin insulating barrier; tunneling
  conductance depends on the relative magnetization of free vs. pinned
  (reference) layers. **MR ratios of 100%+** give the highest sensitivity and
  output of the family, with excellent scalability and low power
  [@lenz2006; @davies2021].

The headline trade across the family: **higher MR ratio (TMR) buys
sensitivity/output, but low-frequency 1/f noise and linear-range limits set the
*usable* detectivity** (§14.3.4).

### 14.3.2 Wheatstone-bridge / push-pull TMR sensors
A single MTJ has large offset and strong temperature dependence. The standard
remedy is to wire four (or two) MTJ elements as a **Wheatstone bridge**:

- A **full bridge** with two "push" and two "pull" arms (achieved by opposing
  pinned-layer directions, or by shield/flux-guide layout) gives a
  **differential output that cancels common-mode temperature drift and
  nulls offset**, doubling sensitivity versus a half-bridge.
- The differential output suits instrumentation-amplifier front ends (Ch. 16)
  and rejects common-mode interference.

TMR bridge sensors thus combine high sensitivity, large linear range, easy
miniaturization, and low power (conf: high — these are the standard,
widely-reported advantages of bridge-configured TMR) [@lenz2006].

### 14.3.3 Set/reset (flipping), linearization, hysteresis
Ferromagnetic free layers have **hysteresis** and can lose their defined state.
Two standard mitigations:
- **Set/reset (flipping)** coils periodically re-establish the magnetization
  reference and, by alternating polarity, allow the electronics to **separate
  the field signal from offset/1/f drift** (a chopper-like technique).
- **Linearization** via a hard-axis bias, shape anisotropy, or closed-loop
  (field-nulling) operation extends the linear range and reduces hysteresis, at
  some cost in sensitivity or complexity.

These techniques are essential to turn a raw MR element into a metrology-grade
sensor and directly shape the AFE (Ch. 16) and the noise budget.

### 14.3.4 Noise in MR sensors: the 1/f floor
The decisive limitation for EMT (which operates at low frequencies) is
**low-frequency 1/f (flicker) noise**:
- GMR and TMR show **larger 1/f noise than AMR**; in TMR the low-frequency noise
  is dominated by **resistance fluctuations in the tunnel barrier** (largely
  field-independent), plus a magnetic 1/f component tied to the active sensor
  area [@davies2021].
- Detectivity (minimum detectable field, in **T/√Hz**) **improves with larger
  die area** and follows a similar inverse-power-law trend across MR types,
  suggesting a quasi-fundamental area-limited floor; when normalized for linear
  range, TMR detectivity becomes essentially comparable to GMR
  [@davies2021].
- Practical bridge TMR detectivities reported in the literature span roughly
  **sub-nT to tens of nT per √Hz at 1 Hz**, design- and area-dependent (conf:
  med — values vary by source and device; cite specific devices when used, do
  not treat any single number as canonical).
- **High-frequency modulation / chopping** (and the set/reset of §14.3.3) can
  push the effective operating point above the 1/f corner and recover noise
  performance — directly relevant to AC-EMT where the signal already sits at the
  excitation frequency.

> **Why the 1/f floor matters for EMT.** Recall Ch. 4 §4.7: the *signal* at the
> edge of a benchtop volume is sub-µT. For an MR sensor to be useful there, its
> detectivity over the measurement bandwidth must be well below that — achievable
> for larger-area bridges and/or with chopping, but a genuine constraint for the
> tiniest dies. This is the quantitative reason induction coils still dominate
> the smallest *AC* medical sensors, while MR/TMR shines where DC response,
> chip-scale integration, or arrays are required.

### 14.3.5 Hall and fluxgate (for context)
- **Hall effect.** Direct, cheap, DC-capable, but **low sensitivity** and higher
  noise — generally too coarse for precision EMT, though useful for coarse
  presence/position [@lenz2006].
- **Fluxgate.** Excellent low-noise DC vector sensing (down to pT-class), the
  classic choice for high-accuracy DC magnetometry and a natural partner to
  **pulsed-DC** EMT — but physically larger and more power-hungry than MR, and
  harder to miniaturize to catheter scale [@lenz2006].

### 14.3.6 Why MR/TMR suits pulsed-DC, chip-scale, and arrays
Pulling §§14.3.1–14.3.5 together: MR/TMR's **flat DC response** is precisely
what an induction coil lacks, making it the enabling sensor for **pulsed-DC**
architectures (sampling a static field after eddy settling, Ch. 6 §6.4). Its
**silicon-scale size, low power, and batch fabrication** make dense **sensor
arrays** and chip-integrated front ends feasible (cf. transmitter arrays,
Ch. 9 / [@plotkin2003]). The open question is pushing detectivity low enough at
catheter die sizes — an active research area (Part XIII).

## 14.4 MEMS and other emerging approaches
- **MEMS Lorentz-force / resonant magnetometers** sense field via
  current-carrying microstructures deflecting in a field; attractive for
  CMOS-MEMS integration, with their own thermomechanical noise trade.
- **Optically pumped / atomic (OPM) and NV-diamond magnetometers** offer
  extraordinary sensitivity (fT–pT) but face bandwidth, size, and
  dynamic-range challenges for EMT working fields; treated as a frontier in
  Ch. 30.4.

## 14.5 Sensor-selection matrix

Qualitative comparison for EMT use (detailed numbers are device-specific and must
be sourced per design; this matrix is for *architecture selection*).
(conf: med — synthesized from [@lenz2006; @davies2021; @yaniv2009].)

| Sensor | DC response | Sensitivity | Noise floor (LF) | Size (min) | Power | Arrayable | Best fit in EMT |
|---|---|---|---|---|---|---|---|
| Induction coil | ✗ (∝ω) | high (area-turns, ×ω) | Johnson (low) | sub-mm (elongated) | passive | moderate | **AC**, smallest medical sensors |
| Fluxgate | ✓ | high | very low (→pT) | cm-scale | higher | poor | **pulsed-DC**, high-accuracy DC |
| Hall | ✓ | low | high | µm-mm | low | good | coarse position only |
| AMR | ✓ | moderate | low-ish (1/f) | µm-mm | low | good | DC, compact, lower-noise MR |
| GMR | ✓ | high | higher 1/f, small range | µm | low | good | compact DC, small range |
| **TMR (bridge)** | ✓ | **highest** | higher 1/f (area-limited) | **µm** | **low** | **excellent** | **pulsed-DC, chip-scale, arrays** |
| MEMS / OPM / NV | ✓ | varies / very high | varies | varies | varies | varies | research frontier (Ch. 30) |

The matrix encodes the chapter's thesis: **coils win on smallness and noise for
AC; fluxgate wins on DC noise floor; TMR bridges win on integration, power, and
arrayability for DC/pulsed-DC** — and the right choice is dictated by the
excitation architecture chosen back in Ch. 8.

---

## Open questions / to verify
- Replace §14.3.4's detectivity range with a small sourced table of specific
  TMR-bridge devices (value @ 1 Hz, die area, linear range), each cited.
- Find and cite a peer-reviewed demonstration of **TMR/MR sensors used in an
  actual position-tracking system** (vs. current/NDE/biomedical sensing) to
  firm up §14.3.6; tag confidence accordingly.
- Verify the elongated-coil 10–20× and 115 mm tip-offset figures against primary
  sources (currently conf: med from design literature).
- Confirm fluxgate pT-class and Hall sensitivity numbers against [@lenz2006].

## Sources cited
- [@lenz2006] sensor-family taxonomy & comparison. [@davies2021] MR/TMR
  detectivity & 1/f noise. [@yaniv2009] inductive coils as clinical gold
  standard. [@ndi_aurora] miniature sensor form factors. [@plotkin2003] arrays.
