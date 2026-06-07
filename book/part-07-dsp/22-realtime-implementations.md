# Chapter 22 — Real-Time Implementations

> **Status:** DEEPENED (awaiting review) · **Part VII — Digital Signal Processing**
> Maps the DSP of Ch. 19–21 and the pipeline of Ch. 11 onto hardware, under the
> latency/determinism constraints of Ch. 12. Citation keys resolve to
> [`../../citations/bibliography.json`](../../citations/bibliography.json).

The algorithms of Ch. 19–21 must run within a hard latency budget (Ch. 12),
deterministically, on hardware that is often small, power-limited, and
medical-grade. This chapter maps the pipeline onto **FPGA, DSP/embedded CPU, and
GPU** targets, develops the **CIC-decimation front end** and **CORDIC** that make
multi-channel lock-in demodulation cheap, analyzes the **fixed-point word-length**
the wide dynamic range demands, and covers the verification a safety-relevant
real-time system requires. The open-source Anser platform is a concrete (research-
grade) realization on commodity hardware [@jaeger2017].

---

## 22.1 The data-rate funnel (quantified)

The pipeline (Ch. 11) is a funnel; sizing it numerically dictates the
partitioning. A representative AC system:

| Stage | Data rate (per sensor axis) | Reduction |
|---|---|---|
| Σ-Δ modulator stream | ~1–10 MHz (1-bit/low-bit) | — |
| After CIC decimation (§22.2) | ~100–500 kS/s (multi-bit) | ×10–100 |
| After lock-in / FIR → amplitudes | $C$ values per **frame** (e.g. 8) | ×$10^3$–$10^4$ |
| Pose + covariance | a few numbers per frame (100–1000 Hz) | — |

The **expensive, branchy** nonlinear work (solver, filter) thus runs only on the
heavily decimated data — a handful of numbers per frame — which is why a
high-channel-count tracker is feasible on modest hardware. The partitioning
follows the funnel: streaming, fixed-cost demodulation in **hardware**; flexible,
bounded-iteration estimation in **software** (§§22.2–22.6).

## 22.2 FPGA front end: CIC decimation + lock-in + CORDIC

FPGAs are the natural home for **Stage 1** (demodulation), because the work is
high-rate, parallel, and must have **data-independent latency** (Ch. 12 §12.4).

### CIC decimation (Hogenauer)
A Σ-Δ modulator outputs a high-rate, low-bit-depth stream that must be
low-pass-filtered and down-sampled. The **cascaded integrator–comb (CIC)** filter
[@hogenauer1981] does this with **no multipliers**: $N$ integrator stages running
at the high input rate, a rate change by $R$, then $N$ comb (differencing) stages
at the low rate. Its key properties:

- **DC gain** $G = (R\,M)^N$ (with $M$ the differential delay, usually 1–2), so the
  output **register width must grow** by $\lceil N\log_2(RM)\rceil$ bits to avoid
  overflow [@hogenauer1981] — a concrete datapath-width budget the designer
  computes up front. For $N=4$, $R=64$, $M=1$: bit growth $= 4\lceil\log_2 64\rceil = 24$ bits
  added to the input width.
- **Passband droop** (a $\operatorname{sinc}^N$ response) must be flattened by a
  small downstream **FIR compensator** (a few taps), which also sets the final
  channel bandwidth and the anti-alias guard for the output rate.

CIC + FIR is the standard, cheap, deterministic decimator pairing for Σ-Δ
front ends (Ch. 18).

### Per-channel lock-in and CORDIC
After decimation, each channel is demodulated by multiplying by the in-phase and
quadrature references (Ch. 20) — **two multiplies** per (sensor axis × transmit
channel) — and integrating (a boxcar or the CIC/FIR itself). Converting the
resulting $X,Y$ to magnitude and phase (eq. 20.1) uses **CORDIC** [@volder1959]:
an iterative **shift-and-add** that computes $\sqrt{X^2+Y^2}$ and
$\operatorname{atan2}(Y,X)$ in vectoring mode with **no multiplier or divider**,
~1 bit of accuracy per iteration. The whole datapath pipelines at initiation
interval 1 (one result per clock) with a fixed latency — exactly the determinism
Ch. 12 demands. Many channels run as parallel datapaths (or time-shared at the
high clock), so cost scales as $O(S\cdot C)$ for $S$ sensors and $C$ transmit
channels (Ch. 19 §19.7).

## 22.3 Fixed-point word-length analysis

The receive chain spans the ~100–120 dB dynamic range of the 1/r³ law
(Ch. 9 §9.6) — i.e. **~17–20 effective bits of signal** — so the FPGA datapath
must carry enough precision that *processing* quantization stays below the ADC's
hard-won ENOB (Ch. 18). The discipline:

1. **Headroom for CIC growth** (§22.2): size accumulators for the full
   $(RM)^N$ gain; truncating intermediate integrators is unsafe (they can wrap).
2. **Guard bits through mix/decimate** so that round-off noise added at each stage
   is well below the signal LSB; a common rule is to keep intermediate widths a
   few bits above the target ENOB.
3. **Saturating** (not wrapping) arithmetic at points where a strong near-field
   signal could overflow — a wrap turns a large value into a small one and
   **corrupts the entire coupling-matrix estimate** (Ch. 11), far worse than a
   saturation that merely clips one channel (Ch. 16 §16.4).
4. **Scaling/normalization** before the float hand-off so the solver sees
   well-scaled numbers (Ch. 24 §24.2 preconditioning).

The output of this analysis is a per-stage word-length table — part of the
implementation's verifiable specification (§22.8).

## 22.4 Embedded CPU / DSP back end

The **solver and estimator** (Stages 2–3) run on an embedded CPU or DSP core:
iterative nonlinear least squares (Ch. 23), the EKF/UKF/ESKF (Ch. 21), and the
host API. Requirements:

- **Bounded work per frame** — cap LM/UKF iterations; on non-convergence at a
  poorly conditioned pose (Ch. 24), emit the predicted pose with inflated
  covariance and a quality flag rather than overrun (Ch. 12 §12.4).
- **Deterministic scheduling** — a real-time OS (or bare-metal with bounded loops)
  with **worst-case execution time (WCET)** analysis, not average-case.
- **Floating-point** for the back end: the dipole forward model and its Jacobian
  span many orders of magnitude (the $1/r^3$ and $r^{-4}$ derivatives, Ch. 24), so
  single/double precision avoids conditioning loss in the matrix solves. For most
  clinical trackers (one or a few sensors) a modern embedded CPU is ample.

## 22.5 GPU acceleration

GPUs become relevant for **massive parallelism**: many simultaneous sensors
(catheter baskets, electrode arrays), large transmitter arrays
([@plotkin2003]), **particle filters** with many particles (Ch. 21 §21.6), or
**field-map / ML distortion-correction** inference (Ch. 27). GPUs add latency and
power and complicate determinism, so they suit high-throughput or research
configurations more than single-sensor low-latency loops.

## 22.6 SoC integration and the fixed/float split

The modern norm is a **system-on-chip**: FPGA fabric for the streaming front end
plus hard CPU cores for the back end, on one device. The robust, recurring
partition is **fixed-point streaming front end → floating-point nonlinear back
end**, with the scaling/normalization of §22.3 at the boundary. This keeps the
deterministic high-rate path in hardware and the flexible, conditioning-sensitive
math in software. Anser, by contrast, demonstrates the *accessible* end of the
spectrum — commodity National Instruments acquisition plus an Arduino and MATLAB
support code — trading the FPGA's determinism for openness and low cost, while
still reaching 1.14 mm accuracy in a research setting [@jaeger2017]. The two
points bracket the design space.

## 22.7 Latency and determinism

Implementing Ch. 12's requirements concretely:

- **Decimation group delay** is usually the **largest front-end latency term** —
  the CIC + FIR + lock-in low-pass impose a fixed delay counted in eq. (12.1).
  Longer integration (lower ENBW, better SNR, Ch. 20) directly lengthens it.
- **Pipelining vs. latency.** Front-end pipelining raises *throughput* but adds a
  fixed *latency*; the two are distinct and both must be budgeted.
- **Acquisition timestamping** at the ADC (Ch. 12 §12.4) so fusion (Ch. 21) and
  the host can compensate fixed transport delays and align modalities.
- **Output jitter** (frame-to-frame timing variation, distinct from clock jitter,
  Ch. 10 §10.4) matters for control loops and fusion as much as average latency;
  FPGA scheduling of the front end keeps it low and deterministic.

## 22.8 Verification of the real-time system

A safety-relevant tracker requires more than "it runs":

- **Bit-exact / model-in-the-loop testing.** Validate the FPGA/fixed-point
  datapath against a floating-point reference model (e.g. the `simulations/`
  `emtrack` library) on recorded and synthetic data, proving the implementation
  matches the *designed* algorithm to within the §22.3 word-length budget.
- **Worst-case timing analysis.** Demonstrate the bounded WCET latency (not just
  average) required by Ch. 12 §12.4 and the regulatory posture of Ch. 29.
- **Fault injection.** Verify graceful degradation (flagging, covariance
  inflation) under saturation, distortion spikes, dropped frames, and solver
  non-convergence — the conditions where naïve implementations fail *silently*.

### Worked resource sketch
For $S=1$ sensor (3 axes) and $C=8$ FDM transmit channels: the demod needs
$3\times8\times2 = 48$ real multiplies per output sample for the I/Q mixing,
plus 3 CIC chains (multiplier-free) and ~24 CORDIC pipelines for magnitude/phase —
comfortably within a small FPGA's DSP-slice budget at a few-hundred-kHz post-decim
rate, leaving the MHz modulator rate handled by the multiplier-free CIC. The
floating-point LM solve on the resulting $\le 24$ couplings runs in well under a
millisecond on an embedded core. (conf: med — order-of-magnitude estimate; a
concrete slice/cycle count is flagged below.)

> **Takeaway.** Real-time EMT is an exercise in putting each computation where the
> data rate and determinism demand it: multiplier-free CIC decimation and
> shift-add CORDIC demodulation, pipelined at fixed latency in **hardware**; a
> bounded-iteration, floating-point estimator in **software**. The funnel (§22.1)
> is what makes the whole thing fit a clinical latency budget.

---

## Failure modes
- **Fixed-point overflow/wrap** (§22.3): a wrapped strong-axis sample corrupts the
  whole coupling matrix — use saturating arithmetic and sized accumulators.
- **CIC droop uncompensated** (§22.2): passband tilt biases amplitudes across the
  band — include the FIR compensator.
- **Unbounded solver iterations** (§22.4): a poorly conditioned pose blows the
  time budget — cap iterations and fall back with a flagged covariance.
- **Average- vs worst-case timing** (§22.7): designing to average latency leaves
  deadline violations under load — budget WCET.
- **Silent fault** (§22.8): no flagging path means distortion/non-convergence is
  reported as a confident wrong pose — inject faults in test.

## Open questions / to verify
- Provide a concrete resource estimate (FPGA DSP-slice count, LUTs, pipeline
  cycles) for a representative multi-channel lock-in + CIC + CORDIC datapath.
- Source which commercial systems use FPGA vs. SoC vs. GPU back ends (Ch. 28)
  with citations rather than assertion.
- Add a fixed-point word-growth worked example (CIC + mix + decimate) tied to a
  target ENOB, as a Phase-5 notebook.

## Sources cited
- [@hogenauer1981] CIC decimation (register growth, droop). [@volder1959] CORDIC
  magnitude/phase. [@jaeger2017] commodity-hardware (NI/Arduino/MATLAB)
  realization. [@plotkin2003] arrays motivating parallelism. Real-time/numerical
  practice cross-referenced to Ch. 11, 12, 18, 23, 24; estimator from Ch. 21.
