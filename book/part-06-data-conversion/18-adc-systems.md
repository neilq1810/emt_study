# Chapter 18 — ADC Systems

> **Status:** DRAFT · **Part VI — Data Conversion**
> The whole of Part VI. Picks up the AFE output of Ch. 16–17 (band-limited,
> isolated, ~100 dB dynamic range) and hands digital samples to the DSP of
> Part VII. Citation keys resolve to
> [`../../citations/bibliography.json`](../../citations/bibliography.json).

The ADC is the boundary between the analog receive chain and everything
computational. For EMT it must do something specific and demanding: digitize a
**narrowband signal** (the excitation tone, or a pulsed-DC settling waveform)
that sits within a **very wide dynamic range** (~100–120 dB, Ch. 9 §9.6 / Ch. 16
§16.4), with enough effective resolution and low enough timing noise that the ADC
is *not* the limiting element. This chapter covers the architecture trade space,
the SNR/ENOB figures of merit, why **oversampling and Σ-Δ noise shaping** are so
well matched to EMT, and how conversion errors propagate toward pose.

---

## 18.1 Architecture trade space

The four mainstream ADC families [@walden1999] and their fit to EMT:

| Architecture | Resolution | Speed | Latency | EMT fit |
|---|---|---|---|---|
| **Flash** | low (≤8 b) | very high | very low | overkill speed, too few bits — not used |
| **Pipeline** | medium (10–14 b) | high (MS/s–GS/s) | medium (pipeline depth) | rarely needed; EMT bandwidth is low |
| **SAR** | medium–high (12–18 b) | medium (kS/s–MS/s) | very low (per-sample) | good for **TDM** (fast settling, low latency per sample) |
| **Σ-Δ (sigma-delta)** | **very high (20–24 b)** | low–medium (effective) | higher (decimation group delay) | **the default for EMT** |

**Why Σ-Δ dominates EMT.** The signal is narrowband and the priority is
*resolution/dynamic range*, not raw speed — exactly Σ-Δ's strength. It also
brings three EMT-specific bonuses:

1. **Oversampling relaxes the anti-alias filter** (Ch. 17 §17.1): the modulator
   runs far above the signal band, so the analog anti-alias filter is gentle and
   cheap.
2. **Built-in decimation filtering** acts as a band-limiting / noise-rejection
   stage that complements the synchronous detector (Ch. 20).
3. **20–24 bit** resolution covers a large fraction of the dynamic range in the
   digital domain, reducing analog PGA gain-switching (Ch. 16 §16.4).

The cost is **latency** (decimation-filter group delay, Ch. 12 eq. 12.1) and that
Σ-Δ is not ideal for fast TDM slot-hopping, where a low-latency **SAR** can be
preferable. The architecture choice therefore couples back to the multiplexing
decision of Ch. 10.

## 18.2 SNR, ENOB, and the figures of merit that matter

For an ideal $N$-bit converter with a full-scale sinusoid, quantization noise
sets the ceiling [@ieee1241]:

$$
\text{SNR}_{q} = 6.02\,N + 1.76\ \text{[dB]}.
\tag{18.1}
$$

Real converters fall short; the **effective number of bits** captures actual
performance from the measured signal-to-noise-and-distortion ratio (SINAD):

$$
\text{ENOB} = \frac{\text{SINAD} - 1.76}{6.02}.
\tag{18.2}
$$

The EMT-relevant figures of merit [@ieee1241; @walden1999]:

- **Dynamic range / ENOB** — must cover the ~100–120 dB span. By (18.1), 100 dB
  needs ENOB ≈ 16.3 bits, 120 dB ≈ 19.6 bits — *before* margin. This is why
  20–24 bit Σ-Δ parts (or SAR + PGA) are the norm.
- **SFDR (spurious-free dynamic range)** — spurs (e.g. harmonics of the
  excitation, mains intermodulation) that land in the detection band masquerade
  as signal; SFDR must keep them below the weakest pose signal.
- **Noise spectral density** in the detection band — for an oversampled
  converter, what matters is the noise *in the narrow band around the excitation
  frequency*, not the total noise, which the next section exploits.

> **Connecting to the AFE.** Ch. 16's noise budget and this chapter must be read
> together: the ADC's input-referred noise (quantization + thermal) is one term
> in the quadrature sum, and the design goal is to keep it **below** the
> AFE/sensor floor so the system stays sensor-limited. An ADC that dominates the
> budget is wasting the front end.

## 18.3 Sampling theory, oversampling, and decimation

**Nyquist** requires sampling above twice the highest frequency present (after
anti-aliasing, Ch. 17). EMT exploits **oversampling** — sampling at rate $f_s$
far above the Nyquist rate for the signal band — in two ways:

- **Quantization-noise spreading.** Quantization noise power is fixed but spread
  over $0$–$f_s/2$; oversampling by ratio $\text{OSR}=f_s/(2B)$ (with $B$ the
  signal band) and then digitally filtering to $B$ keeps only a fraction of that
  noise. The SNR gain is

  $$
  \Delta\text{SNR} = 10\log_{10}(\text{OSR})\ \text{[dB]}\quad(\approx 0.5\ \text{bit per octave of OSR}),
  $$

  for a plain (non-shaped) oversampled converter.
- **Noise shaping (Σ-Δ).** An $L$th-order Σ-Δ modulator additionally *pushes
  quantization noise out of the signal band*, giving a far steeper gain:

  $$
  \Delta\text{SNR} \approx (6L + 3)\ \text{dB per octave of OSR}\quad(\approx L+0.5\ \text{bits per octave}).
  $$

  This is how a 1-bit modulator becomes a 24-bit converter — a structural match
  to EMT's narrow signal band sitting at a known frequency.

**Decimation** then low-pass filters and down-samples to the output rate. The
decimation filter is simultaneously the anti-alias guard for the output rate and
a band-limiter that aids interference rejection — but its **group delay is a
latency term** (Ch. 12) and its **phase response is a calibration constant** for
the synchronous detector (Ch. 20, Ch. 26).

**Coherent sampling.** When possible, lock $f_s$ to the excitation frequency
(both derived from the master clock, Ch. 10 §10.3) so an integer number of signal
cycles fits the analysis window. Coherent sampling makes the single-bin DFT /
lock-in estimate exact (no spectral leakage) and is the cleanest way to estimate
the channel amplitudes of Ch. 11 §11.1.

## 18.4 Clock jitter and quantization-error propagation

**Aperture jitter.** Random sample-instant error $\sigma_t$ caps SNR (the same
relation introduced in Ch. 10 eq. 10.1, here a property of the ADC clock):

$$
\text{SNR}_{\text{jitter}} = -20\log_{10}(2\pi f\,\sigma_t)\ \text{[dB]}.
\tag{18.3}
$$

As shown in Ch. 10 §10.4, at EMT frequencies (≤ tens of kHz) even nanosecond-
class jitter leaves an 80+ dB ceiling, so **jitter is rarely the EMT limit** —
unlike the high-speed converters where Walden identifies aperture jitter as a
dominant ceiling [@walden1999]. The lesson is to spend the clock budget where it
matters (low-frequency stability, coherence) rather than chasing femtosecond
jitter that EMT does not need.

**Error propagation toward pose.** Conversion error enters the pipeline (Ch. 11)
as noise/bias on the channel amplitudes $\hat a_{ij}$ and propagates to pose
through the forward-model Jacobian (Ch. 11 §11.5, Ch. 24). Two practical points:

1. **Quantization is (usually) benign and dither-able.** With adequate ENOB and
   oversampling, quantization noise is small and white-ish; dither linearizes any
   residual quantization nonlinearity so it averages out over the integration
   window (Ch. 11 §11.1, ∝1/√τ).
2. **Spurs and nonlinearity are not benign.** INL/DNL and in-band spurs create
   *correlated* errors that do **not** average away and can bias the coupling
   matrix — hence the SFDR/linearity emphasis of §18.2. These contribute to the
   *deterministic* error term of the budget (Ch. 25), distinct from the
   stochastic noise term.

## 18.5 Putting Part VI in the chain
The ADC converts the clean, scaled, band-limited analog signal (Parts IV–V) into
samples whose in-band noise sits below the sensor floor and whose dynamic range
covers the working volume. With coherent, oversampled, noise-shaped conversion,
the digital signal handed to Part VII is limited by the *sensor and physics*, not
by the converter — which is the whole point of the receive chain. The next part
(DSP) turns these samples into the channel amplitudes and, ultimately, pose.

---

## Open questions / to verify
- Add a worked conversion plan for a target system: choose OSR, Σ-Δ order, output
  rate, and decimation group delay to hit a stated ENOB and latency, as a figure
  (Phase 4) / notebook (Phase 5).
- Source representative ENOB/SFDR/noise-density numbers for ADC parts actually
  used in commercial EMT (Ch. 28), with conditions, rather than asserting.
- Cross-check the (6L+3) dB/octave noise-shaping result and state assumptions
  (ideal modulator, no instability) with a primary data-conversion reference to
  add to the bibliography (e.g. a Σ-Δ text / Schreier–Temes).

## Sources cited
- [@walden1999] ADC architecture/limits survey; jitter and resolution-vs-rate
  trends. [@ieee1241] ENOB/SINAD/SNR definitions and test methods. AFE/sensor
  floor and dynamic-range requirements from Ch. 9, 15, 16.
