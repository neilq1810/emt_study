# Chapter 16 — Amplification & Noise Budgeting

> **Status:** DEEPENED (awaiting review) · **Part V — Analog Front Ends**
> Opens Part V. Picks up the ~nV-class coil noise floor of Ch. 15 (eq. 15.1) and
> the 60 dB dynamic range of Ch. 9 §9.6. Hands off to the ADC (Ch. 18).
> Citation keys resolve to [`../../citations/bibliography.json`](../../citations/bibliography.json).

The analog front end (AFE) stands between a sensor producing nanovolt-class
signals (Ch. 15) and an ADC that needs volt-class inputs (Ch. 18). Its job is to
amplify by 60–120 dB **without adding meaningful noise and without clipping on
the strongest signals in the volume** — two demands that pull in opposite
directions. This chapter develops low-noise amplifier theory, the
source-impedance matching problem unique to coil sensors, the dynamic-range
crisis created by the $1/r^3$ law, and the end-to-end noise budget that decides
whether a system is *sensor-limited* (good) or *electronics-limited* (a design
failure).

---

## 16.1 Low-noise amplifiers: voltage noise, current noise, and the source

Any amplifier referred to its input is modeled by two (largely uncorrelated)
noise generators [@horowitz_hill]:

- a **voltage noise** density $e_n$ [V/√Hz] in series with the input, and
- a **current noise** density $i_n$ [A/√Hz] across the input.

With a source impedance $Z_s$ the total input-referred noise density is

$$
e_{n,\text{tot}} = \sqrt{\,e_n^2 + (i_n\,|Z_s|)^2 + 4k_BT\,\mathrm{Re}(Z_s)\,}\,,
\tag{16.1}
$$

the third term being the source's own Johnson noise (eq. 15.1). Three regimes:

1. **Low source impedance** (resistive, small $|Z_s|$): $e_n$ dominates → choose a
   *low-voltage-noise* amplifier (often bipolar input).
2. **High source impedance** (large $|Z_s|$): the $i_n|Z_s|$ term dominates →
   choose a *low-current-noise* amplifier (often JFET/CMOS input).
3. **Matched**: there is an optimum source resistance
   $R_{s,\text{opt}} = e_n/i_n$ at which the amplifier's **noise figure** is
   minimized; the *noise corner* in $|Z_s|$ where $e_n = i_n|Z_s|$.

**The EMT twist — an inductive source.** A pickup coil is not a resistor; its
impedance is $Z_s = R_s + j\omega L_s$ (plus self-capacitance, §16.3). At the
excitation frequency the reactance $\omega L_s$ can be large, so the
**$i_n|Z_s|$ term is frequently the dominant amplifier noise contribution** —
making *current noise*, not voltage noise, the parameter to minimize for many
coil front ends. This is a point routinely missed by designers who reflexively
reach for the lowest-$e_n$ part. (conf: high — direct from (16.1) with inductive
$Z_s$.)

**The field-sensor twist — a biased resistive source.** A **TMR/MR** sensor is not an
inductive pickup but a **resistive bridge** of moderate, largely-real $|Z_s|$
(k$\Omega$-scale), so the $i_n|Z_s|$ term recedes and the budget returns to the
$e_n$-vs-$4k_BT\,\mathrm{Re}(Z_s)$ balance of the resistive case above — *but* with two
field-sensor-specific lines a coil never has. (i) It is read **ratiometrically against its
bias**, so **bias-reference noise multiplies into the signal** (Ch. 25 §25.2, Ch. 37 §37.4).
(ii) Its **own 1/f magnetic noise usually dominates the AFE** (Ch. 14.3), which *inverts the
design priority*: for a coil you chase the lowest-$e_n$/$i_n$ amplifier and a clean inductive
match, whereas for a TMR you chase a **quiet, stable bias** and accept that the *sensor*, not
the front end, sets the floor — and there is **no $\omega L_s$ to fight** (the source is flat
to DC). (conf: high — direct from (16.1) with a resistive vs inductive $Z_s$.)

**Worked bipolar-vs-JFET choice.** Take a sensor coil with $R_s=50\,\Omega$ and
inductive reactance giving $|Z_s|\approx300\,\Omega$ at the operating frequency,
rising to several k$\Omega$ near self-resonance (§16.3). Compare two LNA inputs
(typical numbers, in nV/√Hz at the input):

| Input | $e_n$ | $i_n$ | $R_{s,\text{opt}}=e_n/i_n$ | $i_n\lvert Z_s\rvert$ @300 Ω | $i_n\lvert Z_s\rvert$ @5 kΩ |
|---|---|---|---|---|---|
| Bipolar | 1 nV/√Hz | 2 pA/√Hz | 500 Ω | 0.6 nV | **10 nV** |
| JFET | 3 nV/√Hz | 5 fA/√Hz | 600 kΩ | 0.02 nV | 0.03 nV |

At the operating point the **bipolar wins** (total ≈ √(1²+0.6²+0.9²) ≈ 1.5 nV/√Hz
vs the JFET's ≈ 3 nV), because $\lvert Z_s\rvert\approx R_{s,\text{opt}}$. But
**near self-resonance** the bipolar's current-noise term explodes to 10 nV/√Hz
while the JFET is unmoved — so a system that must operate near resonance, or with
a very high-impedance coil, flips to a **JFET/CMOS input**. The design rule:
compare $\lvert Z_s\rvert$ *at the operating frequency* (and its worst-case excursion)
against each candidate's $R_{s,\text{opt}}$. (conf: high — eq. (16.1) with the
tabulated device numbers.)

**Figure of merit.** When power is constrained (implantable/wearable AFEs), the
**noise efficiency factor (NEF)** captures the noise-per-unit-bandwidth achieved
per unit bias current, letting designers compare LNA topologies on equal power
footing. Lower NEF = more noise performance per microamp. (conf: high — standard
low-power AFE metric; the NEF originates with Steyaert & Sansen, 1987 — citation
to add.)

## 16.2 Instrumentation amplifiers and CMRR

Coil signals are best handled **differentially**: a floating coil drives a
difference amplifier so that **common-mode interference** — capacitively coupled
mains (50/60 Hz and harmonics), nearby switching supplies, body-coupled noise —
is rejected. The relevant spec is **common-mode rejection ratio (CMRR)**:

$$
\text{CMRR} = 20\log_{10}\!\frac{A_\text{diff}}{A_\text{cm}}\ \text{[dB]}.
$$

An **instrumentation amplifier** (in-amp) provides high CMRR, high input
impedance, and defined gain [@horowitz_hill]. For EMT the in-amp must hold its
CMRR *at the excitation frequency* (not just DC) — AC CMRR degrades with
frequency, and the residual common-mode that leaks through appears at exactly the
band the lock-in is listening to (Ch. 20), so it is not rejected downstream.
Layout symmetry and source-impedance balance between the two inputs are as
important as the in-amp's datasheet CMRR.

## 16.3 Input impedance and coil loading

The coil + amplifier input forms a resonant network: coil inductance $L_s$,
winding resistance $R_s$, self-capacitance $C_s$, plus the amplifier input
capacitance and any cable capacitance. Consequences the AFE designer must manage:

- **Self-resonance** at $f_0 \approx 1/(2\pi\sqrt{L_sC_s})$ bounds the usable
  upper frequency (Ch. 15 §15.3); operating near $f_0$ gives a sensitivity peak
  but with phase/temperature sensitivity that complicates calibration.
- **Loading.** A **voltage-mode** front end with high input impedance avoids
  damping the coil (preserving Q and signal) but sees the full resonant
  behavior; a **transimpedance (current-mode)** front end holds the coil in a
  virtual short, flattening the response and taming resonance at some noise
  cost. The choice is a response-flatness vs. noise trade.
- **Tuned (resonant) pickup.** Deliberately tuning the sensor coil with a
  capacitor to resonate at the excitation frequency multiplies the signal by the
  loaded $Q$ (the receive analogue of the resonant *generator* drive, Ch. 9 §9.4)
  — buying SNR for free in principle. The costs are the same: a narrow bandwidth
  $f_0/Q$ that must contain the channel and demands frequency stability (Ch. 10),
  and strong temperature sensitivity of the tuning. It also conflicts with FDM if
  one sensor must receive *several* transmit frequencies. Resonant pickup is
  therefore common in single-frequency/TDM systems and avoided in
  broadband-FDM ones — a genuine architecture-coupled choice.
- **Cable capacitance** between sensor and AFE shifts $f_0$ and can pick up
  interference; for catheter sensors with long thin leads this is a real error
  source (Ch. 14.2, Part IX) and argues for amplification as close to the sensor
  as safety/size allow.

## 16.4 Dynamic range and the strong-near-field problem

The $1/r^3$ law (Ch. 4) means received amplitude varies by ~**60 dB** across a
10:1 distance range, *before* the angular factor and before accounting for the
strongest pose (sensor on-axis, close to the generator) versus the weakest
(far edge, equatorial). A realistic end-to-end dynamic-range requirement of
**~100–120 dB** is common — meaning ~17–20 effective bits.

No single fixed-gain stage spans this. Standard responses:

- **Programmable-gain amplification (PGA) / auto-ranging:** adapt gain to the
  current signal level so the ADC stays well-filled but unclipped. Gain switches
  must be calibrated (each gain has its own error) and must settle within the
  timing budget (Ch. 10/12).
- **High-resolution ADC** (Σ-Δ, Ch. 18) to cover much of the range in the digital
  domain, reducing analog gain switching.
- **Avoiding clipping** is non-negotiable: a clipped strong-axis signal corrupts
  the *entire* coupling matrix estimate (Ch. 11), not just one channel, because
  the solver expects consistent $M_{ij}$.

**Worked gain plan for 120 dB.** Two ways to cover it (Ch. 18 gives the ADC
side):
- **Single high-resolution Σ-Δ, no PGA.** A 20-bit-ENOB converter has
  $6.02\times20+1.76\approx122$ dB of dynamic range (Ch. 18 eq. 18.1) — enough to
  digitize the full span directly, with fixed analog gain. Simplest and
  gain-error-free, at the cost of a premium ADC and the decimation latency
  (Ch. 12). This is the modern default.
- **PGA + modest ADC.** A 16-bit ADC gives ~96 dB; adding a PGA with, say, three
  ranges (0 / 24 / 48 dB) extends the reachable span to ~144 dB. Cheaper ADC, but
  each gain range carries its own calibrated error (Ch. 26), the switch must
  settle within the frame (Ch. 10/12), and auto-ranging logic must avoid
  oscillating near a threshold.

Either way the binding rule is **never clip the strong-axis signal**: a clipped
near-generator sample corrupts the *whole* coupling matrix (Ch. 11), so the
gain/headroom is set by the strongest pose, and the noise floor by the weakest.
This is one of the hardest AFE problems in EMT and a place where naive designs
fail in the field (works on the bench at mid-range, clips near the generator,
disappears at the edge).

## 16.5 The end-to-end noise budget

The cascade rule (Friis) says the **first stage dominates** the noise figure if
it has enough gain: later-stage noise is divided by the preceding gain when
referred to the input [@horowitz_hill]. Design procedure:

1. **Establish the floor.** The sensor self-noise (Ch. 15): coil Johnson
   ~1.3 nV/√Hz for the worked $100\,\Omega$ example, *or* the MR/TMR 1/f floor
   at the operating frequency.
2. **Budget the AFE below the floor.** Choose the first-stage LNA so its
   input-referred $e_{n,\text{tot}}$ (eq. 16.1, with the inductive $Z_s$) is a
   factor (say 2–3×, i.e. adds <0.5–1 dB) *below* the sensor noise. Then the
   system is **sensor-limited**, the desired outcome.
3. **Refer everything to the input** and combine in quadrature: sensor noise,
   LNA $e_n$ and $i_n|Z_s|$, in-amp noise, PGA, ADC quantization + thermal
   (Ch. 18), and jitter-induced noise (Ch. 10 eq. 10.1). Whichever term is
   largest is the thing to fix.
4. **Check the result is dominated by the sensor**, not the electronics — if the
   ADC or a gain stage dominates, the AFE is wasting the sensor.

> **Worked sanity target.** To keep a 1.3 nV/√Hz coil sensor-limited, the LNA
> must contribute $\lesssim 0.6$ nV/√Hz input-referred at the operating
> frequency — demanding but achievable with a low-$e_n$ bipolar (or paralleled)
> input stage *provided* the $i_n|Z_s|$ term is controlled by managing the coil's
> reactance (§16.1/16.3). For a high-impedance coil this can instead force a
> low-$i_n$ JFET stage. The choice between them is dictated by $R_{s,\text{opt}}
> = e_n/i_n$ versus the coil's $|Z_s|$ at the excitation frequency. (conf: high —
> direct application of (16.1).)

## 16.6 The AFE differs for AC coils vs. biased (MR/DC) sensors

A subtle architecture coupling: *where the signal sits in frequency* dictates the
AFE's 1/f strategy.

- **AC coil systems** place the signal at the excitation frequency (several–tens
  of kHz), comfortably **above the amplifier's 1/f corner**, and the lock-in
  (Ch. 20) already rejects everything off-band. The AFE's own flicker noise and
  offset are therefore largely irrelevant — a plain low-noise LNA suffices.
- **Biased/DC sensors** (MR/TMR, fluxgate baseband, pulsed-DC) put the signal at
  or near **baseband**, *in* the amplifier's 1/f region. Here the AFE needs
  **chopper-stabilization or auto-zeroing** — modulate the signal above the 1/f
  corner, amplify, then demodulate — to remove amplifier flicker noise and offset
  drift. This is the analog counterpart to the sensor's own set/reset chopping
  (Ch. 14.3.3).

The biased-sensor path also carries an electrical-safety burden the passive coil
does not: it must **deliver a stable bias/reference to the sensor at the patient
end**, i.e. active conductors into a (possibly Type CF) applied part, with the
attendant leakage-current, isolation, and self-heating constraints — developed in
Ch. 17 §17.3. A passive coil delivers *no* power to the patient and largely
sidesteps this. The AFE choice (chopper vs. plain LNA) and the safety architecture
are thus both downstream of the AC-coil-vs-biased-sensor decision of Ch. 8/13.

The result of this chapter — an input-referred noise density and a dynamic-range
spec — is the direct input to the ADC requirements of Ch. 18 and the stochastic
term of the error budget (Ch. 25).

---

## Open questions / to verify
- ✅ **Resolved:** §16.1 now has a worked bipolar-vs-JFET noise-matching table
  (operating vs near-resonance), and §16.4 a worked 120 dB gain plan
  (single 20-bit Σ-Δ vs PGA + 16-bit). Remaining: replace the representative
  $e_n/i_n$ with specific candidate-part datasheet numbers (cite per design).
- Add the NEF origin reference (Steyaert & Sansen, *IEEE JSSC*, 1987) to the
  bibliography once the search index is available to verify it.
- Quantify achievable AC CMRR vs. frequency for a candidate in-amp at the
  excitation band, with datasheet citations.

## Sources cited
- [@horowitz_hill] amplifier noise model, noise matching/NEF, in-amps/CMRR,
  chopper/auto-zero, cascade/noise-figure. Sensor floor from Ch. 15; dynamic range
  from Ch. 9 §9.6; biased-sensor safety → Ch. 17.
