# Chapter 34 — Sensor & Component Characterization

> **Status:** DEEPENED (awaiting review) · **Part XVI — Performance Characterization**
> The component-level twin of Ch. 33. You are *selecting* — or *building* — a coil
> or biased (TMR/MR) sensor for a system, and the vendor publishes pair performance,
> not the sensor parametrics you actually need. This chapter is the methodology for
> measuring them. Citation keys resolve to
> [`../../citations/bibliography.json`](../../citations/bibliography.json).

Chapter 33 characterized the *system* — a generator + sensor pair across a volume.
But a system is only as good as its sensor, and here the literature and the
datasheets fail the engineer. **Coil-sensor vendors publish size, DOF, and
pair accuracy — not inductance, area-turns, self-resonance, noise, cross-axis
error, or hysteresis. TMR/MR vendors publish DC-sensing parameters — not the
Barkhausen noise, 1/f behavior at a kHz carrier, or hysteresis that govern AC
electromagnetic-tracking use.** So a designer who must feed the link budget (Ch. 8
eq. 8.1), choose between a coil and a biased sensor, or **build a catheter coil
from scratch**, has to characterize the sensor themselves — and, unlike the
system case, there is **no Hummel-equivalent standard** (Ch. 33 §33.4) to lean on.
This chapter constructs that methodology: the parameters that matter (per class),
the bench to measure them, the reference-field rig and its budget, and the figures
of merit that *predict* the Ch. 33 system numbers — with **hysteresis** and
**Barkhausen noise** given the prominence the datasheets deny them.

---

## 34.1 Why sensor-level characterization is necessary — and why it's missing

- **What vendors give vs. what you need.** EMT coil sensors are typically specced by
  outer diameter, DOF (5/6), and the *system* accuracy of a named pair (Ch. 33);
  TMR/MR parts by DC sensitivity, linearity, and (sometimes) a noise density aimed
  at current/position sensing. The **AC-EMT-relevant** parametrics — N·A_eff,
  self-resonant frequency, detectivity *at the carrier*, Barkhausen, hysteresis —
  are usually absent.
- **Why the designer needs them.** (i) To feed the link budget — σ_B = e_n√(ENBW)/
  (N·A_eff·ω) → CRLB (Ch. 8, 24); (ii) to compare a coil against a biased sensor on
  a *common* basis; (iii) to **build your own** coil and qualify it; (iv) to qualify
  incoming production parts.
- **The thread that makes it matter: the single-valued-map assumption.**
  Calibration (Ch. 26) corrects a **repeatable, single-valued** transfer function.
  Two of the most important sensor imperfections — **hysteresis** (history-dependent,
  *multivalued*) and **Barkhausen noise** (random domain jumps) — violate that
  assumption, so they **cannot be calibrated away** and survive as residual
  deterministic/stochastic error in the budget (Ch. 25). They are precisely the
  parameters the datasheet omits *and* the ones a system designer most needs to
  bound. That is the gap.

## 34.2 Parameters that matter — inductive (coil) sensors

- **Sensitivity — effective area-turns $N A_\text{eff}$.** The transduction constant
  (Faraday, Ch. 5): induced EMF $=N A_\text{eff}\,\omega B$. A ferrite core
  multiplies $A_\text{eff}$ (demagnetizing-limited, Ch. 14.1). The single most
  important number, and it must be *measured* in a known field, not taken from a
  turns count.
- **Electrical — $L$, DC resistance, AC resistance (skin/proximity), $Q$,
  self-resonant frequency (SRF) and parasitic $C$.** These set the usable band and
  the loaded-voltage divider (Ch. 5 §5.5, Ch. 15 §15.3): operate safely below SRF.
- **Noise floor — Johnson–Nyquist** (Ch. 15 eq. 15.1, $e_n=\sqrt{4k_BTR}$): the
  irreducible thermal floor of a passive coil; everything else (AFE) should sit
  below it (Ch. 16).
- **Cross-axis / orthogonality error.** The angular misalignment of the sense axis
  corrupts the coupling matrix (Ch. 13, 26) — a per-unit geometric defect.
- **Linearity & saturation.** Air-core coils are exquisitely linear (passive
  Faraday); **ferrite-cored** coils **saturate** above the core's $B_\text{sat}$ and
  carry **core hysteresis** (below).
- **Core hysteresis (key).** A permeable core has a $B$–$H$ loop, so its effective
  permeability — hence the coil's **gain — is history-dependent**, with remanence
  and added core loss. At EMT's µT fields this is usually small but **not zero**,
  and it grows toward saturation and for high-permeability cored catheter sensors;
  being *multivalued*, it is not removable by single-valued calibration (Ch. 6 §6.3).
- **Microphonics / vibration.** Winding flex or motion in a field generates spurious
  EMF — a genuine catheter-handling artifact.
- **Temperature coefficients.** Cu resistance +0.39 %/°C and core $\mu_r(T)$ drift
  the gain (Ch. 15 §15.5) — the recalibration-interval driver (Ch. 26 §26.6).

## 34.3 Parameters that matter — biased sensors (TMR/MR, Hall, fluxgate)

- **Sensitivity** (e.g. mV/V/mT) and its **bias dependence** — for TMR the
  detectivity can be made roughly **constant with bias** [@monteblanco2021].
- **Detectivity — field-noise spectral density (nT/√Hz)** with its **white floor**
  [@davies2021] and **1/f corner** (Hooge, Ch. 14.3.4). This is the FoM that sets
  σ_B at the carrier and therefore the system CRLB.
- **Barkhausen noise (key for AC use).** Discrete domain-wall reorganization
  produces excess, telegraph-like noise that is **not on DC-oriented datasheets**
  because MR parts target DC/low-frequency sensing. At an EMT carrier it can
  dominate the area-limited floor of a small die (Ch. 14.3.4, Ch. 25 §25.2) — so for
  AC-EMT it **must be measured**, not assumed.
- **Hysteresis (key).** The sensing (free) layer has **magnetic hysteresis** — the
  output depends on field history — quoted, when at all, as % of full scale. It is a
  primary **linearity/repeatability** limiter for MR, reduced by bias/pinning, flux
  concentrators, set/reset pulsing, or closed-loop (flux-feedback) operation. Being
  multivalued, it sets a floor calibration cannot remove (§34.1).
- **Linearity, saturation field, dynamic range.** The linear window and clip point;
  it must span EMT's near-to-far field (~100 dB, Ch. 9 §9.6) without saturating the
  strong axis (Ch. 16 §16.4).
- **Offset & offset drift; bias/temperature coefficients.** A DC offset and its
  thermal drift re-enter the budget; chopper/bridge techniques mitigate (Ch. 16
  §16.6).
- **Cross-field (perpendicular) sensitivity, bandwidth, set/reset behavior.**
  Off-axis response is an orientation-error source; bandwidth must cover the carrier.

| Parameter | Coil | Biased (TMR/MR) | Enters the system as… |
|---|:--:|:--:|---|
| Sensitivity (N·A_eff / mV/V/mT) | ✓ | ✓ | signal → σ_B → CRLB (Ch. 24) |
| Detectivity / noise floor | Johnson | white+1/f+**Barkhausen** | stochastic budget (Ch. 25 §25.2) |
| **Hysteresis** | core B–H | free-layer | **un-calibratable** residual (Ch. 25 §25.3) |
| Linearity / saturation | core B_sat | linear window | clipping → coupling-matrix error (Ch. 11) |
| Cross-axis / cross-field | orthogonality | perpendicular sens. | orientation error (Ch. 13) |
| L, R, Q, SRF | ✓ | (AFE Z_in) | usable band (Ch. 15 §15.3) |
| Tempco / offset drift | Cu, μ_r(T) | offset, bias | recalibration interval (Ch. 26 §26.6) |

## 34.4 The characterization bench

Two instruments around a controlled environment:

- **Impedance analyzer / LCR meter / VNA** — $L$, $R(f)$, $Q$, SRF, parasitic $C$
  for coils (and AFE input impedance for biased parts).
- **A traceable, uniform reference field** — a Helmholtz pair or long solenoid
  producing a *known* $B(I,f)$. This is the **dual of Ch. 33's reference pose**:
  there the traceable reference was *position*; here it is **field**. Calibrate the
  field constant (geometry → tesla per amp) and, crucially, its **uniformity** over
  the sensor volume, traceable via a reference magnetometer (calibrated fluxgate or
  NMR/Hall probe).
- **A shielded / zero-gauss environment** — a mu-metal can or actively nulled coil
  chamber to remove Earth's field and ambient, so offset and **noise** are measured
  at the sensor's own floor; the shielding sets the measurement floor.
- **Low-noise preamp + FFT/spectrum analyzer** — noise spectral density, 1/f corner,
  Barkhausen (statistical jump analysis), SNR.
- **Thermal chamber** — temperature coefficients of sensitivity, offset, $L$, $R$.

## 34.5 Measuring each parameter

- **Sensitivity, linearity, saturation** — sweep the reference-field amplitude at the
  operating frequency: slope = sensitivity, deviation from the line = nonlinearity,
  knee = saturation.
- **Hysteresis — trace the loop.** Ramp the field **up then back down** and plot
  output vs. field: the loop **width ÷ full scale = % hysteresis**, and the vertical
  gap at zero field = **remanence**. Do it at *EMT field amplitudes* (small minor
  loops, not just the major loop) — for a cored coil this is gain-vs-history; for MR
  it is output-vs-history. Hysteresis measured here is the un-calibratable residual
  of §34.1.
- **Detectivity / 1-f / Barkhausen** — in zero field, FFT the output; fit a white +
  1/f model; identify **Barkhausen** as the non-Gaussian, telegraph-like excess and
  confirm it by its **bias/field dependence** (Johnson noise has none).
- **L / R / Q / SRF** — impedance sweep.
- **Cross-axis / cross-field** — rotate the sensor in the uniform field and record
  the off-axis response.
- **Temperature coefficients** — repeat sensitivity and offset across the chamber
  range.

## 34.6 The reference-field rig's own budget (worked)

As in Ch. 33, the **reference's** uncertainty enters every reading — here it is the
*field*, not the pose. To certify sensitivity to 1 %, the reference field must be
known far better than 1 %:

$$
\sigma_\text{B,ref}^2 = \sigma_\text{geom}^2 + \sigma_\text{current}^2 + \sigma_\text{uniformity}^2 + \sigma_\text{align}^2 .
$$

**Worked example.** A Helmholtz reference: field constant known to 0.3 %
(geometry + current sense), field **uniformity** 0.2 % over the sensor volume,
axis **alignment** 0.1° (a $\cos$ error of ~$1.5\times10^{-6}$, negligible) →
reference floor $\sqrt{0.3^2+0.2^2}\approx \mathbf{0.36\,\%}$. You can therefore
**certify sensitivity to ~0.4 %, not better** — the 5–10× rule of Ch. 33, now in the
field domain. For **noise**, the shielded chamber + preamp (input-referred to field)
set the lowest detectivity you can measure; you can characterize a sensor only when
its NSD sits **above** that floor and **below** saturation.

## 34.7 Figures of merit, and the map to system performance

The point of sensor characterization is that a component number **predicts** a
system number (Ch. 33):

- **Detectivity** $D$ (nT/√Hz at the band) → σ_B → CRLB σ_pos (Ch. 24) → the link
  budget (Ch. 8 eq. 8.1). Measure $D$ on the bench; predict the system accuracy.
- **NEF** (Ch. 16) for the biased-sensor + AFE chain.
- **Area-turns per unit volume** for coils — the catheter constraint made
  quantitative: a smaller $N A_\text{eff}$ raises σ_B and pays the z⁴ range penalty
  (Ch. 24, 31).
- **Dynamic range** against the ~100 dB EMT need (Ch. 9 §9.6).
- **Hysteresis and Barkhausen as floors** — entered as the un-calibratable
  deterministic (hysteresis) and stochastic (Barkhausen) residuals of the Ch. 25
  budget; their measured magnitudes tell you whether a biased sensor is *usable* in
  an AC architecture at all.
- **Coil vs. biased on one bench.** Run both through this rig and compare $D$,
  dynamic range, hysteresis, and DC capability; then decide per the architecture —
  AC pickup coil vs. pulsed-DC/chip-scale MR (Ch. 6, 8, 14). The bench makes the
  choice *evidence-based* instead of datasheet-limited.

> **Engineering takeaway.** The system datasheet hides the sensor. To design to the
> link budget, to choose coil-vs-TMR, or to build your own, you must measure what
> the vendor omits: area-turns and SRF for coils; detectivity, 1/f and **Barkhausen**
> for biased parts; and **hysteresis** for both — because hysteresis and Barkhausen
> are exactly the errors a single-valued calibration **cannot** remove, so they must
> be *characterized and budgeted*. Build a traceable reference-*field* bench whose
> own uncertainty sits 5–10× below your target, and report sensor parametrics that
> *predict* the system figures of Ch. 33.

---

## Open questions / to verify
- Propose a **sensor-level characterization protocol** — the missing
  Hummel-equivalent for components — so coil and biased-sensor parametrics become
  comparable across vendors and labs (shared with the Ch. 30 / Ch. 33 standardization
  gap).
- Phase-5 sims: a **hysteresis-loop / Barkhausen model → residual position error**
  link, and a **reference-field uniformity** FEA (Ch. 7) to back §34.6.
- Add a primary reference for **MR hysteresis characterization** and a
  reference-magnetometer **traceability chain** (currently leaning on [@lenz2006]
  for general magnetic-sensor characteristics, conf: med on specifics).
- Tabulate representative measured values (coil $N A_\text{eff}$, SRF; TMR $D$, 1/f
  corner, hysteresis %) for the worked examples once bench or literature data are
  sourced.

## Sources cited
- [@lenz2006] magnetic sensors and their characteristics (coil/fluxgate/MR).
  [@davies2021] magnetoresistive **detectivity** (white floor, comparative).
  [@monteblanco2021] TMR detectivity ~constant with bias. Hooge 1/f and Barkhausen
  ties to Ch. 14.3; Johnson noise to Ch. 15; CRLB/link-budget mapping to Ch. 8/24;
  hysteresis physics to Ch. 6 §6.3; system-level counterpart in Ch. 33.
