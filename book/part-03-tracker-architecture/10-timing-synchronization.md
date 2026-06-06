# Chapter 10 — Timing, Clocking & Synchronization

> **Status:** DRAFT · **Part III — Tracker Architecture**
> Builds on Ch. 5 (coupling matrix), Ch. 8 (chain). Detailed estimation math is
> in Part VII (Ch. 19–20). Citation keys resolve to
> [`../../citations/bibliography.json`](../../citations/bibliography.json).

The forward model (Ch. 5) gives nine numbers — the coupling-matrix entries
$M_{ij}$ between three transmit axes and three sense axes. But a single sensor
coil produces *one* voltage at a time; the system must **separate** the
contributions of the three (or more) transmit axes, and it must know the
**phase reference** of the excitation to recover signed amplitudes. Both jobs
are problems of *timing*. This chapter covers channel separation
(time/frequency/code division), coherent vs. non-coherent detection, and the
clock-jitter budget — the architectural decisions that determine update rate and
set a noise floor the rest of the system cannot beat.

---

## 10.1 The channel-separation problem

A sensor axis measures $\varepsilon_j(t)=-\sum_i M_{ij}\,\dot I_i(t)$ — a
superposition of all transmit axes (Ch. 5 §5.6). To recover the individual
$M_{ij}$ we must make the transmit axes *distinguishable*. Three classic
multiplexing schemes, exactly analogous to communications:

| Scheme | Transmit axes are separated by… | Pros | Cons |
|---|---|---|---|
| **TDM** (time division) | activating one axis at a time | simple decode; no crosstalk if settled; cheap RF | update rate divided by #axes; motion between slots |
| **FDM** (frequency division) | a distinct frequency per axis | all axes simultaneous → higher rate; easy multi-axis | needs guard bands/bandwidth; crosstalk if filters imperfect; per-frequency calibration |
| **CDM** (code division) | orthogonal codes per axis | simultaneous; processing gain; interference-robust | most complex DSP; code/sync design |

The trade is developed quantitatively in Ch. 19. At the architecture level: TDM
is the simplest and most distortion-clean (each axis can be sampled after its
own settling) but pays an update-rate penalty and is sensitive to target motion
*between* time slots; FDM maximizes simultaneity and update rate but spends
bandwidth and demands careful crosstalk control; CDM trades DSP complexity for
robustness. In practice, "TDM is simpler to keep clean; FDM is faster but
needs care with crosstalk and bandwidth" is the rule of thumb borne out across
implementations (conf: med — consistent with the multiplexing literature and
engineering practice; FDM's easier synchronization but larger-bandwidth/crosstalk
trade is widely reported).

## 10.2 Coherent (synchronous) vs. non-coherent detection

The recovered quantity is a small AC (or transient) amplitude buried under the
geomagnetic field and broadband interference (Ch. 4 §4.7). The dominant
technique is **synchronous (coherent) detection** — multiply the sensor signal
by a reference at the excitation frequency/phase and low-pass filter, i.e. a
**lock-in amplifier** (full math in Ch. 20). Coherent detection requires the
receiver to know the **phase** of the transmitter excitation, which is the core
synchronization requirement of this chapter.

- **Coherent** systems share a phase reference between transmitter and receiver
  (a wired clock, or a recovered reference). They achieve the narrowest
  effective noise bandwidth and recover *signed* amplitudes (sign carries
  orientation information, Ch. 5). This is the high-performance default.
- **Non-coherent** systems estimate amplitude without absolute phase (e.g.
  magnitude from quadrature, or envelope detection). Simpler and tolerant of an
  unsynchronized wireless link, but they lose sign information and pay an SNR
  penalty.

The synchronization can be delivered by a **wired reference**, by an **RF/BLE
clock-sync** between transmitter and receiver, or by an **EM-pulse handshake**
that lets the receiver measure and track its clock offset to the transmitter
(conf: med — these synchronization strategies are documented in the EMT
engineering/patent literature; wireless-sensor systems in particular rely on
such schemes). Wireless and detachable-sensor architectures live or die on the
quality of this sync.

## 10.3 Clock architecture and the reference chain

A coherent system is built around one **master clock** (often the DDS reference
that generates the excitation, Ch. 9 §9.4). The reference is distributed to:
the generator drive (defines excitation frequency/phase), the ADC sample clock
(defines when the receiver looks), and the digital demodulator (defines the
lock-in reference). Any *relative* timing error between these corrupts the
amplitude estimate. The key architectural decision is **how the reference reaches
the receiver** — physically shared (best), recovered from the received signal,
or independently disciplined and offset-tracked (wireless).

## 10.4 Clock jitter as a noise floor

Even with perfect *average* synchronization, **jitter** — random
sample-instant timing error — injects amplitude/phase noise that no downstream
processing can remove. For a sinusoidal signal of frequency $f$, RMS timing
jitter $\sigma_t$ produces an aperture-jitter SNR ceiling

$$
\mathrm{SNR}_{\text{jitter}} = -20\log_{10}\!\big(2\pi f\,\sigma_t\big)\ \text{[dB]},
\tag{10.1}
$$

the standard ADC aperture-jitter relation (derived and applied to ENOB in
Ch. 18). Two consequences for EMT:

1. The same higher excitation frequency that buys coil sensitivity (Ch. 5 §5.2)
   *tightens* the jitter requirement via (10.1) — another facet of the
   frequency trade.
2. The jitter floor must sit **below** the thermal/quantization noise floor of
   the AFE/ADC (Ch. 16, 18), or it dominates the error budget (Ch. 25). This
   makes the reference oscillator's phase noise a first-class system spec, not
   an afterthought.

*Worked sanity check:* at $f=10\,\text{kHz}$, achieving an 80 dB jitter ceiling
needs $2\pi f\sigma_t \le 10^{-4}$, i.e. $\sigma_t \lesssim 1.6\,\text{ns}$ —
readily met by ordinary crystal references, confirming that at EMT's low
frequencies **jitter is usually not the limiting term** (unlike RF systems).
The dominant timing concern in EMT is therefore *settling/sequencing* (TDM) and
*phase-reference integrity* (coherence), not raw jitter. (conf: high — direct
application of (10.1) at EMT frequencies.)

## 10.5 Timing and update rate

Timing choices set the **update rate**, a clinically critical spec:

- **TDM:** $f_\text{update} \approx 1/(N_\text{axes}\times t_\text{slot})$, where
  $t_\text{slot}$ includes settling + integration. More axes (or more
  transmitters in an array) → slower updates unless slots shorten (less
  integration → more noise). A direct rate-vs-accuracy trade.
- **FDM:** all axes simultaneous, so update rate is set by the integration time
  needed for the desired per-frequency SNR and bin separation, not by axis
  count — generally faster, at the bandwidth/crosstalk cost of §10.1.
- **Pulsed-DC:** rate limited by per-axis eddy-current settling wait (Ch. 6
  §6.4) plus magnetometer integration.

These feed directly into the end-to-end latency budget of Ch. 12.

---

## Open questions / to verify
- Attach a primary citation for EM-pulse / RF clock-synchronization schemes in
  wireless EMT (patent literature surfaced in research; find a peer-reviewed
  anchor).
- Provide representative $t_\text{slot}$, integration-time, and update-rate
  figures per architecture from sourced material (Ch. 28) rather than asserting.
- Cross-check (10.1) derivation placement with Ch. 18 to avoid duplication.

## Sources cited
- [@raab1979], [@franz2014] for coherent-detection EMT context; multiplexing and
  synchronization specifics cross-referenced to Ch. 19–20 and flagged for
  primary-source attachment above.
