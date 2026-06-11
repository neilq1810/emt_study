# Chapter 36 — Compute Platform & Processor Selection

> **Status:** DEEPENED (awaiting review) · **Part XVII — Software, Integration & Deployment**
> The silicon under the software. Ch. 22 develops *how* to implement the pipeline
> (CIC/CORDIC, fixed-point, the FPGA→CPU partition); Ch. 35 the software around it.
> This chapter answers the procurement-level question those leave open: **which
> compute** — FPGA, SoC, SoM, MCU, DSP, GPU, host — and **which processor cores**,
> for a given requirement. It cross-references Ch. 22 rather than repeating it.
> Citation keys resolve to [`../../citations/bibliography.json`](../../citations/bibliography.json).

Choosing the compute platform is a *selection* problem driven by four forces, all
established earlier: the **data-rate funnel** (Ch. 22 §22.1), the
**latency/determinism budget** (Ch. 12), the **software-safety class** (Ch. 35
§35.4), and the **form factor** (console → catheter). Get the mapping right and the
implementation (Ch. 22) is straightforward; get it wrong — a Linux core on the
hard-real-time path, or an FPGA where a microcontroller would do — and no amount of
optimization recovers it. This chapter is the decision framework and the silicon
taxonomy, with a worked stage→silicon mapping.

---

## 36.1 The selection drivers

Map requirement to silicon by these axes:

| Driver | Low end → | High end → | Pushes toward |
|---|---|---|---|
| Streaming data rate (Ch. 22 §22.1) | few ch, kSps | many ch, MSps | FPGA fabric / hard DMA |
| Determinism / RT class (Ch. 12) | soft-RT pose | hard-RT streaming | FPGA / Cortex-R / RTOS |
| Numeric type | fixed-point | nonlinear float | Cortex-A/FPU / DSP |
| Parallelism (sensors) | one tool | many sensors / ML | GPU / FPGA lanes |
| Safety class (Ch. 35 §35.4) | Class A | Class C | lockstep + ECC (Cortex-R) |
| Form factor / power | console | catheter pod | SoM/MCU, mW budget |
| Volume / time-to-market | prototype | high volume | SoM (buy) → custom SoC |

The decisive split is **between the deterministic streaming front end** (Stage 1,
demodulation) and the **flexible floating-point back end** (Stages 2–3, solve and
filter) — the same fixed/float boundary as Ch. 22 §22.6, now read as a *device*
boundary.

## 36.2 The silicon taxonomy

- **FPGA.** Deterministic, massively parallel, hard-real-time — the natural home of
  Stage-1 demod/decimation (Ch. 22 §22.2). Cost: development effort, power, and no
  comfortable path for nonlinear floating-point code.
- **SoC (FPGA + hard ARM, Zynq-class).** Fabric *and* application cores on one die —
  the modern norm (Ch. 22 §22.6): the fabric streams, the cores solve/filter/host.
- **SoM (system-on-module).** A COTS module (SoC + RAM + power management) on a
  custom carrier — the **build-vs-buy** lever: buy the hard compute, design only the
  carrier and AFE. Faster time-to-market, lower NRE; less optimal at high volume.
- **MCU (Cortex-M).** A deterministic microcontroller for low-channel/low-rate
  systems, drive sequencing and sync (Ch. 10), housekeeping, or as the
  deterministic island in an AMP SoC (§36.3). M4F/M7 add FPU + DSP extensions for
  modest lock-in/solve; no MMU → bare-metal/RTOS only.
- **DSP.** VLIW/SIMD MAC engines for the back-end math — increasingly subsumed by
  SoC ARM-with-NEON and FPGA, but still strong for dense filtering.
- **GPU.** Many simultaneous sensors, field-map evaluation, or ML
  distortion-inference (Ch. 22 §22.5, Ch. 27); adds latency and power → console
  only.
- **Host CPU (x86 / ARM-A).** The application, UI, and integration stack (Ch. 35),
  and often the solver in a **PC-tethered** system (a small DAQ/FPGA streams to a
  host — the Anser pattern [@jaeger2017]).

## 36.3 ARM Cortex-M vs R vs A — the core-family choice

The three families exist for three different guarantees; pick by which guarantee
the stage needs:

- **Cortex-M (microcontroller).** No MMU (MPU only), **deterministic** interrupt
  latency, low power; bare-metal or a small RTOS. M4F/M7 carry an FPU and DSP
  instructions. *Role in EMT:* drive sequencing and synchronization (Ch. 10),
  housekeeping, watchdogs, low-channel lock-in, or the deterministic real-time core
  in an AMP SoC. *Not* for Linux or a heavy floating solve.
- **Cortex-R (real-time).** Hard-real-time with bounded latency, frequently
  **dual-core lockstep with ECC** for functional safety, and tightly-coupled memory
  for determinism. *Role:* the **safety-critical** real-time/guard compute — a
  Class-B/C pose-guard or essential-performance monitor (Ch. 35 §35.4) where a
  deterministic, fault-detecting processor is required.
- **Cortex-A (application).** MMU, runs Linux, high throughput, NEON SIMD,
  multi-core. *Role:* the nonlinear **solver/filter** (Ch. 21, 23), the
  **integration/host** stack (OpenIGTLink/ROS, Ch. 35), and the UI. It is **not
  inherently deterministic** (MMU, caches, Linux scheduling) — keep the hard-RT path
  off it, or pair it with an M/R companion.
- **The AMP pattern.** A modern SoC combines all three — Cortex-A (Linux: solve +
  integration) + Cortex-R/M (deterministic RT + safety) + FPGA fabric (streaming) —
  communicating over shared memory / RPMsg. **Map each pipeline stage to the core
  whose guarantee fits**, rather than forcing one core to do everything.

> **Decision rule.** Deterministic streaming → FPGA (or a Cortex-R island);
> deterministic control/housekeeping → Cortex-M; throughput float + Linux +
> integration → Cortex-A; safety-critical guarding → lockstep Cortex-R; massive
> parallelism / ML → GPU.

## 36.4 Mapping the pipeline to silicon (worked)

Take the capstone (Ch. 31): 8-coil FDM, ~kHz carriers, an ADC stream of, say,
**8 channels × 1 MSps × 16 bit ≈ 128 Mbit/s**, producing **≥100 Hz** pose.

| Stage | Work | Rate / load | RT class | → Silicon |
|---|---|---|---|---|
| 1 — demod + decimation (Ch. 22 §22.2) | CIC + lock-in + CORDIC, fixed-point | ~128 Mbit/s in | **hard-RT** | **FPGA fabric** (or Cortex-R + DMA, low ch.) |
| 2 — calibrate + solve (Ch. 23) | apply map, LM on SO(3) | ~10²–10³ solves/s, float | soft-RT | **Cortex-A** (NEON) / DSP |
| 3 — filter/fuse (Ch. 21) | EKF/UKF + covariance | per-pose, float | soft-RT | **Cortex-A** |
| host / integration / UI (Ch. 35) | OpenIGTLink/ROS, display | streaming | soft-RT | **Cortex-A / Linux** or x86 host |
| safety guard / EP monitor (Ch. 35 §35.4) | watchdog, NIS alarm (Ch. 27) | continuous | hard-RT | **Cortex-R** lockstep |

**Compute sanity check.** Stage 1 is the heavy streaming load — a few
multiply-accumulates per sample per channel at MSps → tens–hundreds of MMAC/s,
comfortably inside a small FPGA's DSP-slice budget (Ch. 22 resource sketch). Stages
2–3 are *cheap*: a few hundred kFLOP per pose × 10³ poses/s ≈ sub-GFLOP/s — a
single Cortex-A core (multi-GFLOPS with NEON) sits at low single-digit %
utilization, leaving ample margin for the integration stack. **The streaming front
end, not the solver, sizes the silicon** — the data-rate-funnel lesson (Ch. 22
§22.1) in procurement form.

A **Zynq-class SoC** (FPGA + Cortex-A + optional Cortex-R5) covers Stages 1–3 on one
device; a **PC-tethered** variant puts Stage 1 on a small FPGA/DAQ and Stages 2–3 on
the host — the Anser architecture [@jaeger2017], which trades integration density
for openness and low cost.

## 36.5 Real-time OS and the software pairing

- **OS by core.** Bare-metal / FreeRTOS / Zephyr on the M/R deterministic island;
  **Linux (PREEMPT_RT)** on the A core for the app and integration; **AMP** with
  RPMsg/shared memory between them.
- **Determinism techniques** (Ch. 22 §22.7, Ch. 35 §35.2): IRQ priority, CPU
  pinning/isolation, no paging on the RT path, tightly-coupled memory.
- **The 62304 angle** (Ch. 35 §35.4): the RTOS and Linux are **SOUP** to be
  version-pinned and risk-assessed; the safety core's **lockstep + ECC** is part of
  the Class-C hardware argument that backs the software safety case.

## 36.6 Form factor, power and thermal

The patient end constrains compute as hard as the algorithm does:

- **Console / cart** — no meaningful power/thermal limit → FPGA + GPU + host as
  needed.
- **Portable / wearable** — SoC/SoM, single-digit watts, passive cooling.
- **Catheter handle / tethered pod** — only the AFE (and perhaps a small MCU) at the
  patient end; the heavy compute lives **up the cable or in the console**, because a
  hot SoC cannot sit inside a **Type-CF** applied part under the
  patient-heating/leakage limits of Ch. 17. Power maps to heat maps to a
  **safety** limit, not merely a thermal one.

## 36.7 Build-vs-buy and lifecycle

- **COTS SoM + custom carrier** — fastest, lowest NRE; couples you to the module's
  availability and lifecycle (a long-term-supply and regulatory concern, Ch. 35).
- **Custom SoC/board** — best size/cost/power at volume; high NRE and time.
- **Lifecycle wins over fashion.** Long-term availability, security-update support,
  and the IEC 62304 / cybersecurity posture (Ch. 35 §35.4) favor a documented,
  supported, *boring* platform over the bleeding edge — the same conservatism the
  safety case rewards. (conf: med — engineering guidance; representative
  MIPS/GFLOPS/DSP-slice figures here are vendor-class and should be pinned to
  specific parts at design time.)

> **Engineering takeaway.** Choose silicon by the requirement, not the fashion. The
> data-rate funnel and the determinism budget put **streaming demod on an FPGA (or a
> Cortex-R island)**, the **floating nonlinear solve and integration stack on
> Cortex-A/Linux**, **deterministic control on Cortex-M**, **safety-critical
> guarding on lockstep Cortex-R**, and **massive parallelism on a GPU** — often
> several of these on one AMP SoC. The patient-heating limits (Ch. 17) and the
> software-safety class (Ch. 35) bound the choice as much as raw compute does.
> Chapter 22 tells you how to implement each stage; this chapter tells you what to
> run it on.

---

## Open questions / to verify
- Source which commercial EMT systems use FPGA vs. integrated SoC vs. PC-tethered
  DAQ back ends (shared with the Ch. 22 / Ch. 28 open item).
- Add a worked **power/thermal budget** for a catheter-tethered vs. console form
  factor, tied quantitatively to the Ch. 17 patient-heating limits.
- Pin the representative MIPS/GFLOPS/DSP-slice/power figures (currently vendor-class,
  conf: med) to specific candidate parts once a design is chosen.
- Add an AMP **inter-core latency** budget (RPMsg/shared-memory hop) into the Ch. 12
  end-to-end latency accounting.

## Sources cited
- [@jaeger2017] Anser — a PC-tethered (DAQ + host) open-source architecture, the
  reference for the "FPGA/DAQ front end + host solver" partition. [@iec62304]
  software-safety classification motivating lockstep/ECC safety cores. Pipeline,
  determinism, and partition ties to Ch. 11, 12, 21–23, 22, and 35; patient-heating
  limits to Ch. 17.
