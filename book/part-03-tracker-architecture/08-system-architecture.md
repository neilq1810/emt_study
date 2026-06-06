# Chapter 8 — Complete System Architecture

> **Status:** DRAFT · **Part III — Tracker Architecture**
> Bridges the physics of Part II to the subsystem chapters (9–12) and to the DSP
> and solver Parts (VII–VIII). Citation keys resolve to
> [`../../citations/bibliography.json`](../../citations/bibliography.json).

This chapter assembles the pieces. Parts I–II established *why* EMT exists and
*what physics* it exploits; from here the book becomes an engineering design
treatise. We give the reference signal chain end to end, then use it to frame
the single most consequential architectural decision — **AC vs. pulsed-DC vs.
hybrid excitation** — at the system level, before the later chapters dive into
each block.

---

## 8.1 The reference signal chain

Every electromagnetic tracker, regardless of vendor, instantiates the same
canonical chain. Read left to right as the flow of information; the chapter
pointers show where each block is developed in depth.

```
                          (magnetic near field, 1/r^3)
                                     ┌───────┐
 ┌──────────┐  drive  ┌───────────┐ │       │ ┌────────┐  EMF  ┌──────────┐
 │ Excitation│──────▶ │   Field   │ │ Field │ │ Sensor │─────▶ │  Analog  │
 │ generator │ I_t(t) │ generator │─┼─────▶ ─┼─│  coil  │ ε(t)  │ front end│
 │ (DDS/PA)  │        │  coils    │ │       │ │ triad  │       │ (LNA/IA) │
 └──────────┘         └───────────┘ └───────┘ └────────┘       └────┬─────┘
   ▲  Ch.10                Ch.9        Ch.4-6     Ch.13-15          │ Ch.16-17
   │ timing/clock                                                  ▼
   │                                                          ┌──────────┐
   │                                                          │   ADC    │ Ch.18
   │                                                          └────┬─────┘
   │  reference (coherent detection)                               ▼
   │                                                       ┌────────────────┐
   └────────────────────────────────────────────────────  │ DSP: channel   │ Ch.19-20
                                                           │ separation +   │
                                                           │ amplitude est. │
                                                           └───────┬────────┘
                                                                   ▼  M_ij  (Ch.5)
                                                           ┌────────────────┐
                                                           │ Position solver│ Ch.23-24
                                                           │ (inverse model)│
                                                           └───────┬────────┘
                                                                   ▼  pose + covariance
                                                           ┌────────────────┐
                                                           │ State estimator│ Ch.21
                                                           │ (Kalman/fusion)│
                                                           └───────┬────────┘
                                                                   ▼
                                                              Host / API  Ch.12
```

The chain's *information* content is exactly the program of the physics
chapters: the excitation and coils impose a **known** $\mathbf{B}(\mathbf{r})$;
the sensor and AFE measure the **coupling** $\mathbf{M}$ (Ch. 5, eq. 5.6); the
DSP estimates the $M_{ij}$ amplitudes from noisy samples; and the solver inverts
the forward model (5.3)/(5.6) to recover pose. Distortion (Ch. 6) enters as an
error on $\mathbf{M}$; calibration (Part X) and the state estimator (Ch. 21)
fight it.

## 8.2 The defining fork: AC vs. pulsed-DC vs. hybrid

The architecture-level decision that colors every downstream block is the
excitation/detection scheme. Chapter 6 gave the physics; here is the
**system-level trade**, which the designer must commit to early because it
dictates the sensor type, the AFE, the timing system, and the achievable update
rate.

| Axis | **AC (continuous sinusoidal)** | **Pulsed-DC (transient)** |
|---|---|---|
| Sensor type | AC pickup coil (EMF $\propto\omega$) | (Quasi-)static magnetometer: fluxgate / MR, or coil + integration |
| Detection | Synchronous / lock-in (Ch. 20) | Sample after eddy-current settling (Ch. 6 §6.4) |
| Conductive (eddy) distortion | **Higher**, grows with frequency | **Lower** (waited out) |
| Ferromagnetic distortion | High | High (no relief) |
| Signal vs. frequency | Sensitivity $\propto\omega$ — raise $f$ for SNR | Set by magnetometer noise floor |
| Update-rate limiter | Integration time for desired SNR/separation | Settling wait per axis |
| Representative lineage | Polhemus [@polhemus_tech]; Raab et al. [@raab1979] | Ascension (Blood), see Ch. 1 §1.6 |

**Hybrid and alternative excitations.** Between the two poles lie schemes that
try to keep AC sensitivity while mitigating its distortion: quadratic/quadrature
excitation and distortion-aware modulation (surfaced in the patent literature),
**rotating quasi-static fields** decoded by phase/amplitude [@paperno2001], and
**transmitter-array** systems that activate subsets of many uniaxial coils to
trade accuracy against computation [@plotkin2003]. These broaden the design
space surveyed across Part III and Part XIII, but they do not escape the
fundamental tension: *anything that couples usefully into a hidden sensor also
couples into nearby metal.* (conf: high — this tension is intrinsic to near-field
magnetic coupling, Ch. 4–6.)

## 8.3 Source-driven vs. sensor-driven topology

Reciprocity (Ch. 5 §5.5) means the coupling $\mathbf{M}$ is identical regardless
of which element transmits. The system designer is therefore free to choose
topology on *practical* grounds:

- **Large transmitter / small sensor** (the medical norm). A fixed "field
  generator" of substantial moment $m_t$ illuminates the volume; tiny sensor
  coils ride on catheters/needles. Advantages: the miniaturized element is
  *passive* (no power to deliver to the body), and transmit power/safety is
  managed at the fixed generator. This is the CARTO/Aurora style (Ch. 1
  §§1.7–1.8).
- **Small transmitter / large receiver.** The tracked object carries a small
  emitter; fixed large receivers listen. Useful where the tracked object can be
  powered and the infrastructure can be large. Common in some motion-capture and
  VR contexts.

The choice interacts with the **dynamic-range** problem (Ch. 16): because of the
$1/r^3$ law, the signal varies by $\sim60\,$dB across a 10:1 range of distances,
so whichever element is the receiver must accommodate enormous amplitude
variation across the working volume.

## 8.4 What the rest of Part III covers

- **Ch. 9 — Field generators & sensor coils.** Coil geometries, drive
  electronics, field-shaping; mapping coil count/arrangement to 3/5/6-DOF.
- **Ch. 10 — Timing, clocking & synchronization.** Coherent vs. non-coherent
  detection, reference distribution, jitter budget, and the FDM/TDM/CDM
  multiplexing that physically separates the $M_{ij}$ (detailed in Ch. 19).
- **Ch. 11 — DSP pipeline & estimation.** The data path from ADC samples →
  channel amplitudes → coupling matrix → pose hand-off.
- **Ch. 12 — Latency & real-time constraints.** The end-to-end latency budget
  and the throughput/latency/accuracy trade that determines clinical usability.

## 8.5 A system-level error and latency view (forward reference)

Two budgets, assembled later, are best *kept in mind from the start* because
architecture decisions here determine them:

- **Error budget (Part IX, Ch. 25).** Stochastic (sensor/ADC/thermal noise),
  deterministic (tolerance, model mismatch, calibration residual), and
  environmental (distortion, interference, motion) errors combine into the pose
  uncertainty. The excitation choice of §8.2 sets the distortion term; the coil
  and AFE choices set the noise term.
- **Latency budget (Ch. 12).** Integration/settling time + ADC/decimation +
  solver iterations + filtering delay. AC integration time and pulsed-DC
  settling time are the dominant, architecture-fixed contributions.

These two budgets are the quantitative scorecards by which the whole design in
Part XIV is ultimately judged.

---

## Open questions / to verify
- Replace the ASCII block diagram with a rendered SVG in `figures/` (Phase 4)
  and a Three.js interactive in `dashboard/` (Phase 6).
- Source concrete representative update-rate / latency numbers per architecture
  from primary or standardized sources (not vendor marketing) for §8.2/§8.5.
- Verify the claim that modern AC "dynamic metal immunity" narrows the AC/DC
  distortion gap, and quantify if so (ties to Ch. 6 open question).

## Sources cited
- [@raab1979] canonical AC architecture & method. [@polhemus_tech] AC vendor
  lineage. [@paperno2001] rotating-field excitation. [@plotkin2003] transmitter
  arrays. (Pulsed-DC architecture: see Ch. 1 §1.6 and Ch. 6 §6.4.)
