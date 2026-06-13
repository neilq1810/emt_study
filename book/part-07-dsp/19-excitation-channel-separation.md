# Chapter 19 — Excitation & Channel Separation

> **Status:** DEEPENED (awaiting review) · **Part VII — Digital Signal Processing**
> Develops the multiplexing introduced architecturally in Ch. 10 §10.1. Feeds
> Ch. 20 (detection). Citation keys resolve to
> [`../../citations/bibliography.json`](../../citations/bibliography.json).

A 6-DOF tracker must measure the nine couplings $M_{ij}$ between three transmit
axes and three sense axes (Ch. 5) — and a planar/array generator (Ch. 9) may
have *eight or more* transmit coils, each contributing an equation. But a sensor
axis produces a single voltage that superposes **all** active transmitters
(Ch. 5 §5.6). **Channel separation** is the DSP problem of recovering the
individual couplings from that superposition, and it is solved by designing the
*excitation* so the transmitters are distinguishable. This chapter develops the
three classical multiplexing schemes — frequency, time, and code division — with
their signal models, the **crosstalk mechanisms** that actually limit them in
hardware (harmonics, intermodulation, leakage, motion), and quantified trades of
**update rate, bandwidth, power, and accuracy**. A running concrete example is
the open-source **Anser EMT** platform, which uses FDM across eight
field-generator coils and reports 1.14 mm / 0.04° accuracy [@jaeger2017].

---

## 19.1 The separation problem, formally

Let transmit channel $i$ (one coil) be driven by current $I_i(t)$, and let the
geometry-dependent coupling to sensor axis $j$ be $M_{ij}$ (Ch. 5). By Faraday's
law the sensor-axis EMF is

$$
\varepsilon_j(t) = -\sum_{i=1}^{C} M_{ij}\,\dot I_i(t) + n_j(t),
\tag{19.1}
$$

summed over all $C$ active transmit channels, with $n_j$ the receiver noise
(Parts IV–VI). The estimator must recover the $C$ unknowns $\{M_{ij}\}_i$ for
each sensor axis $j$ from the single scalar stream $\varepsilon_j(t)$. This is
solvable **iff** the drive set $\{I_i(t)\}$ is *separable* — orthogonal in
frequency, time, or code — so that a linear operator (a bank of correlators)
maps $\varepsilon_j$ back to the individual couplings. Formally, separation
requires a set of analysis functions $g_i(t)$ such that

$$
\frac{1}{T}\int_0^T \dot I_i(t)\,g_k(t)\,dt = \kappa_i\,\delta_{ik},
\tag{19.2}
$$

i.e. the demodulator $g_k$ responds only to channel $k$. The three schemes are
three constructions of $\{I_i, g_i\}$ satisfying (19.2) — TDM, FDM, and pulsed-DC
(waveform schematic: `figures/ch19_excitation_schemes.png`); they differ entirely in
*how* the orthogonality is realized and in *how it breaks* under non-ideal
hardware (§§19.2–19.4). The proportionality constant $\kappa_i$ (which depends on
drive amplitude and, for AC, on frequency) is absorbed by calibration (Ch. 26),
but its **frequency dependence is itself a design issue** for FDM (§19.2).

## 19.2 Frequency-division multiplexing (FDM)

Drive each transmit channel at a distinct frequency,
$I_i(t)=A_i\cos(\omega_i t)$, so $\dot I_i(t) = -A_i\omega_i\sin(\omega_i t)$.
All channels radiate **simultaneously and continuously**; the analysis functions
are quadrature sinusoids $g_i(t)=\{\cos\omega_i t,\ \sin\omega_i t\}$ (a bank of
lock-ins, Ch. 20), or equivalently the bins of one FFT. Substituting into (19.1)
and demodulating at $\omega_k$ recovers

$$
\hat M_{kj} \;\propto\; \frac{1}{A_k\,\omega_k}\,\big\langle \varepsilon_j,\ \sin\omega_k t\big\rangle .
\tag{19.3}
$$

**The per-frequency scaling matters.** Because the EMF carries the factor
$\omega_k$ (the coil is a differentiator, Ch. 5 §5.2), higher-frequency channels
produce proportionally larger signals for the same coupling — but also see
proportionally worse eddy-current distortion (Ch. 6 §6.2). The recovered
amplitudes must therefore be calibrated **per frequency** (gain *and* the
frequency-dependent distortion map differ channel to channel, Ch. 26).

### Frequency planning — the real constraints
Choosing $\{\omega_i\}$ is the central FDM design task, governed by four limits:

1. **Bin resolution vs. integration time.** An estimator integrating for time
   $\tau$ resolves frequencies separated by $\gtrsim 1/\tau$ (the FFT/lock-in
   bandwidth). Channels must satisfy
   $|f_i - f_k| \gg 1/\tau$, with margin for filter roll-off and motion smearing
   (below). For $\tau = 10\,\text{ms}$, $1/\tau = 100\,\text{Hz}$, so practical
   spacing is several hundred Hz to ~1 kHz. This directly couples **channel count
   to update rate**: more channels in a fixed band → finer spacing → longer $\tau$
   → slower updates.
2. **Harmonic collisions.** Power amplifiers and coils are mildly nonlinear, so a
   channel at $f_1$ radiates weak energy at $2f_1, 3f_1,\dots$. If another channel
   sits on a harmonic ($f_2 = 2f_1$), that distortion **lands exactly in $f_2$'s
   bin** and is indistinguishable from signal — a coherent, non-averaging bias
   (Ch. 25 §25.3). Frequencies must be chosen **mutually non-harmonic** within the
   distortion-significant range (typically up to the 3rd–5th harmonic).
3. **Intermodulation (IMD).** Two channels $f_i, f_k$ through a nonlinearity
   generate products at $f_i \pm f_k$, $2f_i \pm f_k$, etc. None of these
   low-order products may fall on an occupied bin. With many channels (Anser's
   eight, [@jaeger2017]) this becomes a genuine combinatorial frequency-assignment
   problem.
4. **Band limits.** The band is bounded below by the eddy/SNR trade (Ch. 6) and
   $1/f$ environment, and above by sensor self-resonance (Ch. 15 §15.3) and the
   anti-alias/ADC budget (Ch. 18).

**Pros.** Maximum simultaneity → highest update rate (no channel waits); scales
naturally to many transmitter coils for planar/array generators (Ch. 9);
each channel is a clean single-tone estimation problem amenable to the optimal
single-bin estimator (Ch. 20 §20.2).

**Cons.** Consumes **bandwidth** (guard bands); demands the harmonic/IMD
discipline above; carries **per-frequency distortion**; and drives **all coils
continuously**, so FDM draws more average current/power and dissipates more heat
than TDM (a documented practical difference) — relevant to the generator drive
(Ch. 9 §9.4) and thermal stability (Ch. 15 §15.5). (conf: high for the mechanisms;
the current/heat penalty is reported in the engineering/patent literature and is
a direct consequence of continuous multi-tone drive.)

## 19.3 Time-division multiplexing (TDM)

Energize one transmit channel at a time in sequence; the analysis function is a
gate over channel $i$'s active slot. Each $M_{ij}$ is then read almost directly,
since only one transmitter is on.

**Timing structure.** Each slot comprises (i) a **blanking/settling** interval
(let drive current establish and, in pulsed-DC, let eddy transients decay,
Ch. 6 §6.4), then (ii) an **integration** window. The frame time and update rate
are

$$
T_\text{frame} = N_\text{slots}\,(t_\text{settle} + t_\text{int}),\qquad
f_\text{update} = 1/T_\text{frame},
\tag{19.4}
$$

with $N_\text{slots}$ the number of transmit channels (×axes). The **duty cycle**
per channel is $1/N_\text{slots}$, which is why TDM "supports a limited number of
users/channels": each added channel directly lengthens the frame.

**Pros.** **Simplest, cleanest decode** — no inter-channel crosstalk because only
one channel is on; each slot can hold its own settling (ideal for pulsed-DC eddy
management); only one drive amplifier need be active at a time (lower
instantaneous power, simpler PA). **Cons.** Update rate divided by channel count
(19.4); and — critically — **target motion *between* slots** introduces a skew
(§19.6).

## 19.4 Code-division multiplexing (CDM) & orthogonal excitation

Drive all channels simultaneously but with **mutually orthogonal codes**. The
canonical choice is the **Walsh–Hadamard** set: rows of an $N\times N$ Hadamard
matrix $\mathbf H_N$ (entries $\pm1$, $\mathbf H_N\mathbf H_N^\top = N\mathbf I$).
Each channel $i$ is modulated by code row $\mathbf h_i$ over $N$ chips; the
receiver correlates the captured frame against each code:

$$
\hat M_{ij} \;\propto\; \frac{1}{N}\sum_{c=1}^{N} \varepsilon_j[c]\,h_i[c],
\tag{19.5}
$$

and because $\mathbf h_i\!\cdot\!\mathbf h_k = N\delta_{ik}$, channel $k$'s
contribution cancels for $i\neq k$ — **Hadamard de-multiplexing**, a single
matrix multiply $\hat{\mathbf M} = \tfrac1N \mathbf H_N \boldsymbol\varepsilon$.

**Processing gain.** Correlating over $N$ chips coherently sums signal while
incoherently averaging noise, giving a processing gain $\sim N$ (the same
$1/\sqrt N$ amplitude-SNR improvement as integrating $N$ samples, Ch. 20). CDM
thus spreads each channel's energy across a wide band, making it **robust to
narrowband interference** (a motor or mains harmonic corrupts only the chips it
overlaps). **Cons.** Most complex DSP (correlators, code/frame synchronization,
Ch. 10); **code cross-correlation** must be near-zero — residual correlation
(from timing offset, band-limiting that rounds the $\pm1$ transitions, or
non-simultaneous channel switching) leaks between channels as a bias; and the
frame length $N$ trades against update rate. The closely related **rotating-field**
method encodes axis information into the phase/amplitude of a two-axis-generated
field [@paperno2001], and transmitter arrays combine spatial and temporal coding
[@plotkin2003] — all instances of the orthogonality condition (19.2).

## 19.5 The trade space (quantified)

| Criterion | TDM | FDM | CDM |
|---|---|---|---|
| Simultaneity / update rate | low (÷ $N$) | high | high |
| Bandwidth used | narrow | wide (guard bands) | wide (spread) |
| Crosstalk mechanism | none (sequential) | harmonics / IMD / filter leakage | code cross-correlation / sync |
| Avg. drive power | low (one channel on) | **high** (all on) | high (all on) |
| Distortion handling | per-slot settling (great for pulsed-DC) | per-frequency calibration | spread across band |
| Motion artifact | **inter-slot skew** (§19.6) | bin smearing (Doppler) | chip-window smearing |
| DSP complexity | low | medium (FFT / lock-in bank) | high (correlators + sync) |
| Natural fit | pulsed-DC; few channels | continuous AC; many coils ([@jaeger2017]) | many emitters; hostile interference |

**Design rules of thumb** (conf: med — engineering practice consistent with the
multiplexing literature and Ch. 10): use **TDM** when distortion cleanliness and
simplicity dominate and the target moves slowly (or motion is compensated); use
**FDM** when update rate and channel count are paramount and the
harmonic/IMD/heat budget can be managed (the dominant choice for planar
multi-coil medical generators, [@jaeger2017]); use **CDM** when many emitters or
hostile narrowband interference demand spreading/processing gain. Hybrids are
common — e.g. **TDM across a few transmitter banks, FDM across axes within a
bank** — to balance channel count against power and frame time.

## 19.6 The motion problem and why it shapes the choice

For a target moving at velocity $v$, TDM's inter-slot skew $\Delta t$ between the
first and last axis produces an inconsistency $\sim v\,\Delta t$ among couplings
measured at different instants. At a catheter speed of $0.1\,\text{m/s}$ and a
3-slot frame with $\Delta t = 3\,\text{ms}$, that is $\sim0.3\,\text{mm}$ of skew —
comparable to the static accuracy budget (Ch. 1, [@hummel2005]) — and it appears
as a *correlated* error across DOF that the solver cannot average away
(Ch. 23 §23.6). FDM/CDM are nominally simultaneous, but they are **not** immune to
motion: a moving sensor Doppler-shifts and broadens each FDM bin (and smears CDM
correlation) over the integration window, which both blurs the amplitude estimate
and can spill energy into neighbouring bins. The shared lesson: **integration
time and motion are coupled** — longer $\tau$ buys SNR (Ch. 20) but increases
intra-frame motion error, a facet of the accuracy/rate/latency trilemma (Ch. 12).
Fast-motion systems either shorten $\tau$ (accepting noise), choose simultaneous
schemes, or explicitly motion-compensate in the estimator (Ch. 21). (conf: high —
direct kinematics and Fourier broadening.)

## 19.7 Scaling to many transmitters and many sensors

Real medical generators are not a single triad. A **planar field generator**
(Ch. 9 §9.2) may carry $C \ge 8$ coils so that a single small sensor sees an
**over-determined** set of $C$ equations (one coupling per coil), improving
observability and conditioning (Ch. 24) and enabling a calibrated non-dipole
forward model. Anser, for instance, drives **eight coils on eight distinct
frequencies** and demodulates all simultaneously by lock-in [@jaeger2017]. With
$S$ sensors, the receive side replicates: each sensor channel runs the same
demodulator bank, so cost scales as $O(S\cdot C)$ correlators — which is exactly
why the high-rate demodulation lives on the FPGA (Ch. 22 §22.2). Multiplexing
choice interacts with this scaling: FDM's continuous drive of $C$ coils sets the
generator's thermal limit, while TDM's frame grows linearly with $C\cdot(\text{axes})$.

## 19.8 Worked example — an FDM frequency plan

**Goal:** assign three transmit-axis frequencies for a ≥100 Hz, sub-mm benchtop
tracker (consistent with Ch. 31).

1. **Band.** Pick 7–13 kHz: high enough for coil-EMF SNR (∝ω), low enough to keep
   copper-class eddy distortion modest (skin depth ≈ 0.66 mm at 10 kHz, Ch. 6
   §6.2) and below typical sensor self-resonance.
2. **Integration time.** Target $f_\text{update} \ge 100\,\text{Hz}$ with margin →
   $\tau \approx 5\,\text{ms}$ → bin resolution $1/\tau = 200\,\text{Hz}$. Require
   spacing $\ge 5\times$ that for clean separation → $\ge 1\,\text{kHz}$.
3. **Candidate set.** $f_1 = 7\,\text{kHz},\ f_2 = 9\,\text{kHz},\ f_3 = 11\,\text{kHz}$
   (1 kHz of margin beyond the 1 kHz minimum). Check pathologies:
   - *Harmonics:* $2f_1 = 14$, $2f_2 = 18$, $2f_3 = 22$ kHz — all **outside** the
     7–13 kHz receive band (filtered by anti-alias/band-select, Ch. 17). No
     in-band harmonic lands on a channel. ✓
   - *Low-order IMD:* $f_2-f_1 = 2$, $f_3-f_2 = 2$, $f_3-f_1 = 4$ kHz — none equal
     to $f_1,f_2,f_3$; $f_1+f_2 = 16$ kHz (out of band). The third-order products
     $2f_1-f_2 = 5$, $2f_2-f_1 = 11 = f_3$ ✗ — **collision!** $2f_2 - f_1 = 11\,\text{kHz}$
     coincides with $f_3$.
   - *Fix:* shift to $f_1 = 7,\ f_2 = 9.3,\ f_3 = 11.6\,\text{kHz}$. Recheck
     $2f_2 - f_1 = 11.6 = f_3$ ✗ still collides (because the set is near-uniformly
     spaced, which *maximizes* IMD overlap). Choose a **non-uniform** set:
     $f_1 = 7.1,\ f_2 = 9.7,\ f_3 = 12.3\,\text{kHz}$ → $2f_2-f_1 = 12.3 = f_3$ ✗.
     Uniform-ish triads keep colliding; break it: $f = \{7.1,\ 8.9,\ 12.7\}$ →
     $2f_2-f_1 = 10.7$, $2f_1-f_2 = 5.3$, $2f_3-f_2 = 16.5$, $2f_2-f_3 = 5.1$ — no
     third-order product lands within a bin-width of any channel. ✓

   The lesson is concrete and often surprising to newcomers: **evenly spaced FDM
   frequencies are the *worst* choice** because their intermodulation products
   recombine onto channels; deliberately *irregular* spacing is required. This is
   why production multi-coil systems use carefully optimized, non-uniform
   frequency sets [@jaeger2017]. (conf: high — arithmetic shown; the design
   principle is standard in multitone instrumentation.)

---

## Failure modes (FDM/TDM/CDM)
- **FDM harmonic/IMD bias** — a non-averaging, coherent error (Ch. 25 §25.3);
  caught by spectral monitoring of empty guard bins and by the §19.8 frequency
  audit.
- **FDM/CDM Doppler smearing** — fast motion broadens bins/chips, blurring
  amplitudes and spilling between channels; mitigate with shorter $\tau$ or motion
  models (Ch. 21).
- **TDM inter-slot skew** — correlated multi-DOF error from sequential sampling
  of a moving target (§19.6).
- **Non-coherent leakage** — if the analysis clock is not locked to the excitation
  (Ch. 10), spectral leakage biases every estimate; windowing or coherent
  sampling (Ch. 18 §18.3) is mandatory.
- **CDM sync/cross-correlation leakage** — code timing offset or band-limited
  edges break orthogonality; budget the residual as a deterministic bias.

## Open questions / to verify
- Source the *specific* frequency set and per-channel calibration approach used by
  Anser [@jaeger2017] (and at least one commercial system) to ground §19.2/19.8.
- Quantify achievable FDM crosstalk vs. guard-band/ADC-SFDR for a concrete design
  (ties Ch. 18 §18.2); add as a Phase-5 notebook (a multitone IMD simulation).
- Add a CDM correlation-leakage budget vs. code length and timing offset.
- Confirm the FDM current/heat penalty quantitatively against a primary source
  (currently mechanism-cited, conf: med).

## Sources cited
- [@jaeger2017] open-source FDM (8-coil) EMT, lock-in, accuracy. [@paperno2001]
  rotating-field/orthogonal excitation. [@plotkin2003] transmitter-array
  spatio-temporal coding. [@hummel2005] static-accuracy scale for the motion-skew
  comparison. [@franz2014] medical-EMT context. Detection math follows in Ch. 20.
