# Chapter 37 — Power Architecture & Design

> **Status:** DEEPENED (awaiting review) · **Part XVIII — Power Architecture & Design**
> The EMT-specific power considerations — *not* generic power electronics. The system
> power tree, and the three places where power design is decisive: the **generator
> drive**, the **low-noise AFE rails**, and the **remote biased-sensor bias/reference**.
> Cross-references Ch. 9 (generator electrical model), Ch. 16 (AFE noise), Ch. 17
> (isolation/safety), Ch. 25 (error budget). Citation keys resolve to
> [`../../citations/bibliography.json`](../../citations/bibliography.json).

In most instruments, power is a background utility. In electromagnetic tracking it
is **on the signal path**, because the power and the measurement share one magnetic
channel: the generator's drive *current is the field* (Ch. 4, 9), the analog front
end sits under a microvolt signal (Ch. 16), and a biased sensor needs power and a
reference delivered into the patient (Ch. 17). This chapter is therefore not about
SMPS topologies or PFC — assume that standard material (e.g. [@horowitz_hill]) — but
about the EMT-specific power problems: the **system power tree** and the three
subsystem cases, quantified where the numbers matter.

---

## 37.1 The system power tree

A defensible EMT power architecture partitions by **domain** *and* by **noise**:

```
Mains ─▶ medical isolation (Ch.17) ─▶ pre-regulators ─┬─▶ GENERATOR DRIVE  (high current, noisy)
                                                      ├─▶ ANALOG / AFE     (quiet, low-noise)  [§37.3]
                                                      ├─▶ DIGITAL / COMPUTE (Ch.36, noisy)
                                                      └─▶ ISOLATED PATIENT-SIDE BIAS (Type CF) [§37.4]
```

- **The cardinal EMT power rule:** keep the **generator-drive** and **digital
  switching** domains *out of the AFE rails and out of the field band* — separate
  windings/regulators, separate returns, local post-regulation, and physical +
  **spectral** separation (switching frequencies chosen away from the carrier and the
  FDM channels, Ch. 19).
- **Isolation barriers (Ch. 17 §17.3):** chassis vs. patient-side; the biased-sensor
  bias supply *crosses* a Type-CF barrier and is a fault source to contain
  [@iec60601_1].
- Each rail's budget traces to a chapter: drive noise → field error (§37.2, Ch. 25
  §25.4); AFE rail noise → input-referred floor (§37.3, Ch. 16); bias-reference
  drift → field-equivalent error (§37.4, Ch. 25 §25.2).

## 37.2 Generator drive power — the decisive case

The generator is a power-electronics problem sitting *on the measurement*.

- **The load.** High-current, **inductive** ($L,R$ from Ch. 9 eq. 9.1), usually a
  **resonant** tank (high $Q$). At resonance the amplifier sees the real winding
  resistance; off-resonance, a large reactance. The tank stores large reactive
  energy ($V_C$, $I_L \gg$ the drive), which dominates the transient behavior.
- **Spectral purity is the headline.** Because $\mathbf B \propto I_\text{drive}$
  (Ch. 4, 9), **any drive-current noise or distortion at/near the carrier is a field
  error the sensor cannot distinguish from signal.** A fractional current noise
  $\delta I/I$ produces $\delta B/B$ of the same size. *Worked:* to keep the
  generator's contribution to $\sigma_B$ below the ~1 nT sensor floor on a ~µT field
  — a fraction of ~$10^{-3}$–$10^{-4}$ — the **in-band** drive-current
  noise + distortion must sit **below that fraction at the carrier**. Worse,
  **harmonics/IMD** land in *other* FDM channels → crosstalk (Ch. 19), and
  **phase noise** smears the lock-in (Ch. 10, 20). Spectral purity of the drive is
  thus a first-order accuracy parameter, not an EMC afterthought.
- **Ratiometric rescue — and its limit (Ch. 25 §25.4).** Sense the *actual* drive
  current and normalize the sensor reading by it: this cancels **common,
  correlated** drive amplitude drift and noise. But it cancels only what the
  current-sense captures, at the same band and instant — **post-sense** effects
  (coil self-heating changing $R$, connector drift, the sense element's own noise)
  and out-of-band/per-channel terms survive. The **current-sense quality bounds the
  rescue**, so the sense resistor/transformer is itself a precision, low-noise
  component.
- **Linear (class-AB) vs. switching (class-D).** Class-AB gives a clean spectrum at
  poor efficiency and real heat (thermal drift, Ch. 15 §15.5) — favored when
  spectral purity dominates. Class-D is efficient but injects switching spurs
  (hundreds of kHz–MHz) whose IMD with the carrier can **fold into band**; it demands
  heavy output filtering and a switching frequency chosen well clear of the carriers
  and their harmonics. The trade is **efficiency vs. in-band spur risk** — and in EMT
  the spur risk is often decisive.
- **Loop stability into a reactive load.** A current-drive amplifier into $L$ and a
  high-$Q$ tank carries phase lag that erodes phase margin, and the tank can ring.
  Compensate/damp for stability with the *reactive/resonant* load, and bound the
  **transient settling** — critical for **pulsed-DC** (the current step must settle
  within the eddy-settling budget, Ch. 6 §6.4) and for FDM amplitude changes.
- **Current-mode drive.** Regulate the *current* (hence the field), not the voltage;
  current-mode control with a clean current sense serves both field stability and the
  ratiometric reference at once.
- **Thermal.** $I^2R$ in coil and output stage → temperature → coil resistance/area
  drift (recalibration, Ch. 15 §15.5) and amplifier bias drift; manage the heat
  and/or sense temperature (the same $I^2R$ noted in Ch. 9 driving the thermal
  problem).

| Generator-power requirement | Why (EMT-specific) |
|---|---|
| In-band current noise ≲ σ_B target fraction | drive noise = field noise = measurement noise |
| Low harmonics/IMD at carrier multiples | else FDM cross-channel crosstalk (Ch. 19) |
| Low phase noise | else lock-in smearing (Ch. 10, 20) |
| Stable into high-Q reactive load | no ringing; bounded transient |
| Bounded settling | pulsed-DC eddy budget (Ch. 6) |
| Clean current sense | enables ratiometric (Ch. 25 §25.4) |

## 37.3 Low-noise power for the sensor-interface unit (AFE)

The AFE amplifies microvolts (Ch. 16); rail noise enters through finite **PSRR**.

- **The budget.** A rail noise $e_\text{rail}$ referred to input as
  $e_\text{rail}/\text{PSRR}$ must sit **below the coil Johnson floor** (~nV/√Hz,
  Ch. 15 eq. 15.1). *Worked:* with $e_{n,\text{coil}}\approx1.3$ nV/√Hz and a stage
  **PSRR ≈ 80 dB at the carrier**, the rail noise must be ≲ $1.3\,\text{nV}\times
  10^{4}\approx 13\ \mu\text{V}/\sqrt{\text{Hz}}$ in band — trivial for a good
  **LDO**, but out of reach for a raw switcher (mV-class ripple and spurs).
- **LDO post-regulation.** Let a medical-isolated switching pre-regulator do the
  efficient heavy lifting, then clean the **final analog rail** with an LDO chosen
  for **high PSRR at the carrier** and low self-noise — watching the LDO's PSRR
  roll-off as the carrier rises.
- **Rail/return partitioning & grounding (Ch. 17 §17.2).** Separate analog/digital/
  drive returns to a single-point/star tie, guard the high-impedance front end, and
  keep switching $di/dt$ loops small and far from the pickup. **Choose switching
  frequencies so spurs and harmonics miss the carrier band and the FDM channels.**

## 37.4 Remote biased-sensor bias & reference tree

The biased-sensor case (TMR/MR/Hall/fluxgate; Ch. 14.3, 16.6, 17) makes power a
*patient-side* problem.

- **Why it's special.** A passive coil needs **no power at the patient end** (only
  its induced EMF). A biased sensor needs **DC bias + a stable reference delivered to
  a remote tip** → active power crossing into a **Type-CF** applied part: isolated
  bias supply, single-fault containment, patient-leakage limits (10/50 µA)
  [@iec60601_1] (Ch. 17 §17.3).
- **Reference stability *is* measurement stability.** A biased sensor's output scales
  with its bias/reference, so a reference drift $\delta V_\text{ref}/V_\text{ref}$ is
  **indistinguishable from a field change** — a direct bias-reference error term
  (Ch. 25 §25.2). *Worked:* a TMR bridge output $\propto V_\text{bias}$; to keep the
  field-equivalent error below the $\sigma_B$ budget (~$10^{-4}$ fractional), the
  reference's combined temperature drift + noise from DC to the carrier must hold to
  ~$10^{-4}$. This is *the* reason biased-sensor EMT lives or dies on reference
  design.
- **Ratiometric / chopper defense (Ch. 16 §16.6).** Drive the bridge **and** the
  ADC reference from the *same* reference → ratiometric cancellation of reference
  drift; chopper/auto-zero rejects offset and 1/f. Architect the bias and the ADC
  reference as **one** subsystem.
- **Delivery over the cable.** Voltage drop, noise pickup, and thermal effects on long
  thin catheter leads argue for **remote (Kelvin) sensing** of the bias at the tip,
  barrier-side filtering, and treating the bias rail as a contained fault source
  (Ch. 17 §17.3).
- **Power vs. heat at the tip.** Bias power dissipated at the sensor causes **tip
  self-heating** against the patient-heating limit (Ch. 14, 17) — bounding the
  allowable bias power and favoring high-impedance/low-power bias schemes.

> **Engineering takeaway.** In EMT, power is on the signal path. The generator's
> drive current *is* the field, so its in-band noise, distortion, phase noise, and
> switching spurs become measurement error — making **spectral purity, current-mode
> drive with a clean current sense (for ratiometric), stability into a reactive load,
> and bounded transient settling** the dominant generator-power concerns. The AFE
> rails must sit **below a microvolt front end** (PSRR + LDO post-regulation +
> partitioned returns). And a biased sensor turns power into a **patient-side,
> safety-bounded** delivery of bias and a **stable reference whose drift masquerades
> as field** — defended ratiometrically. None of this is generic power electronics;
> all of it is EMT-specific because the power and the measurement share one magnetic
> channel.

---

## Open questions / to verify
- Turn §37.2 into a numeric **drive-current noise/THD budget** from a target
  $\sigma_B$ via the link budget (Ch. 8 eq. 8.1) — express as ppm and THD at the
  carrier.
- Provide a **class-D switching-frequency + output-filter** worked example that
  keeps spurs and IMD out of a given FDM plan (Ch. 19).
- Quantify **catheter-tip bias self-heating** vs. the Ch. 17 patient-heating limit
  for a representative TMR bias current.
- Add a primary reference on **low-noise / ratiometric magnetometer bias** and on
  high-PSRR analog-rail design for instrumentation front ends.

## Sources cited
- [@horowitz_hill] standard analog/power-supply design (the generic material this
  chapter assumes). [@iec60601_1] medical isolation/leakage governing the
  patient-side bias supply. Generator electrical model and resonant drive from Ch. 9;
  AFE noise/PSRR from Ch. 16; isolation/grounding/medical-grade power from Ch. 17;
  ratiometric and bias-reference error terms from Ch. 25; FDM/crosstalk from Ch. 19.
