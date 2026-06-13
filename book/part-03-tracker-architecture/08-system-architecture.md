# Chapter 8 — Complete System Architecture

> **Status:** DEEPENED (awaiting review) · **Part III — Tracker Architecture**
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
canonical chain (schematic: `figures/ch08_system_block_diagram.png`). Read left to
right as the flow of information; the chapter pointers show where each block is
developed in depth.

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

## 8.4 The architecture parameter space

Beneath the excitation fork, the architect commits to a handful of top-level
parameters *before* any component is selected. These are the real degrees of
freedom, and every later chapter is the detailed design of one of them:

| Parameter | Range | Primarily sets / trades | Detailed in |
|---|---|---|---|
| Excitation scheme | AC / pulsed-DC / hybrid | distortion vs. sensor type | §8.2, Ch. 6 |
| # transmit coils $C$ | 3 (triad) … 8–16 (planar/array) | observability / PDOP; forward-model complexity | Ch. 9, 24, 7 |
| # sensors $S$ | 1 … many | throughput, FPGA cost | Ch. 22 |
| Multiplexing | FDM / TDM / CDM | update rate vs. bandwidth/power/crosstalk | Ch. 19 |
| Excitation band $f$ | ~0.1–30 kHz | SNR ($\propto\omega$) vs. eddy distortion | Ch. 5, 6 |
| Topology | large-Tx/small-Rx or reverse | which element is miniaturized; safety | §8.3 |
| Synchronization | wired / RF / EM-pulse | coherence vs. tether (wireless) | Ch. 10, §8.6 |
| Sensor DOF | 5 / 6 / hybrid+IMU | size vs. roll observability | Ch. 13, 21 |

The medical mainstream (e.g. NDI Aurora, the open-source Anser [@jaeger2017])
occupies one well-trodden corner of this space — **AC, FDM, planar multi-coil
generator, small passive sensor, wired sync** — but it is a *choice*, not a law;
§8.7 maps the alternatives.

## 8.5 The system link budget (the master design relation)

The whole book collapses, at the architecture level, into a single chain from
the generator moment to the pose accuracy — the EMT analogue of a radio **link
budget**. Tracing the signal (AC case):

$$
\underbrace{B \sim \frac{\mu_0 m_t}{4\pi r^3}}_{\text{field, Ch. 4}}
\ \to\
\underbrace{\varepsilon \sim N_s A_s\,\omega\,B}_{\text{induced EMF, Ch. 5}}
\ \to\
\underbrace{\mathrm{SNR} = \frac{\varepsilon}{e_n\sqrt{\mathrm{ENBW}}}}_{\text{detection, Ch. 16/20}}
\ \to\
\underbrace{\sigma_\text{pos} \sim \frac{r}{\mathrm{SNR}}\cdot\mathrm{PDOP}}_{\text{accuracy, Ch. 24}} .
$$

Collecting terms, the architecture-level accuracy relation is

$$
\boxed{\;
\sigma_\text{pos}\ \propto\
\frac{e_n\,\sqrt{\mathrm{ENBW}}\;\cdot\;r^4\;\cdot\;\mathrm{PDOP}}
{\mu_0\,m_t\,N_sA_s\,\omega}\; }
\tag{8.1}
$$

(the $r^4$ collecting the $1/r^3$ field and one further power from the
position-sensitivity, Ch. 24 §24.5). **Every architectural knob appears
explicitly:** raise the generator moment $m_t$ (Ch. 9) or the sensor area-turns
$N_sA_s$ and frequency $\omega$ (Ch. 5, 13); lower the front-end noise $e_n$
(Ch. 15–16); narrow the noise bandwidth ENBW by integrating longer (Ch. 20 — but
that lowers update rate); add transmit coils to cut PDOP (Ch. 24); or shrink the
working radius $r$. Equation (8.1) is the quantitative scorecard the from-scratch
design (Ch. 31) optimizes, and it makes the trade-offs *visible* rather than
emergent. A sanity check: the Ch. 5 worked numbers (50 µV edge signal, ~13 nV
demodulated noise → SNR ≈ 3800) give sub-millimetre $\sigma_\text{pos}$,
consistent with the CRLB of Ch. 24. (conf: high — assembled from the cited
per-chapter results.)

## 8.6 Wireless, active/passive sensors & synchronization architecture

A top-level choice the excitation fork does not settle: **how the sensor's data
and clock reach the processor.**

- **Passive sensor (the medical norm).** In the large-Tx/small-Rx topology the
  sensor is a bare coil with no power; its microvolt EMF travels down thin wires
  to the AFE. Pros: tiny, safe, simple. Cons: those µV-level, high-impedance
  wires are vulnerable to triboelectric and cable pickup (Ch. 16 §16.3), so the
  cable is part of the error budget (Ch. 25).
- **Active / wireless sensor.** The sensor digitizes locally and transmits over
  RF/BLE, eliminating the µV cable — attractive for untethered instruments — but
  it now needs *power* and, crucially, **clock synchronization** with the
  transmitter, since there is no shared wire for the coherent reference. This is
  solved by RF clock-sync or an EM-pulse handshake (Ch. 10), and is an active
  research direction (wireless EMT). The synchronization architecture — **wired
  reference (best coherence) vs. recovered vs. wirelessly disciplined** — is
  therefore a first-class architectural decision, not a detail, because coherent
  detection (Ch. 20) is only as good as its phase reference (Ch. 10 §10.4).

## 8.7 Worked architecture selection & commercial mapping

The parameter space of §8.4 is navigated by the *dominant requirement*. A
compact decision logic (expanded in Ch. 31):

- **Small passive catheter sensor + high update rate** → **AC + FDM + planar
  multi-coil generator** (the Aurora/Anser corner) [@jaeger2017].
- **Conductive-clutter-dominated environment, magnetometer sensor acceptable** →
  **pulsed-DC + TDM** (the Ascension corner, Ch. 6 §6.4).
- **Many simultaneous emitters / hostile narrowband interference** → **CDM**
  spreading (Ch. 19 §19.4).
- **Untethered instrument** → active/wireless sensor + RF/EM-pulse sync (§8.6).

Mapping representative systems onto the parameter space (Ch. 28; vendor/
literature-sourced, conf: med):

| System | Excitation | Mux | Topology | Coils |
|---|---|---|---|---|
| Polhemus | AC | FDM/TDM | Tx triad / Rx triad | 3 |
| Ascension | pulsed-DC | TDM | large Tx / small Rx | 3 |
| NDI Aurora | AC | FDM | planar Tx / small passive Rx | multi |
| Anser (open) [@jaeger2017] | AC | FDM | planar 8-coil / small Rx | 8 |

The clustering in the "AC/FDM/planar/small-passive" corner is not coincidence: it
is the corner that (8.1) and the safety/miniaturization constraints jointly favour
for *medical* use — but VR, biomechanics, and pulsed-DC clutter-immune
applications populate other corners.

## 8.8 What the rest of Part III covers

- **Ch. 9 — Field generators & sensor coils.** Coil geometries, drive
  electronics, field-shaping; mapping coil count/arrangement to 3/5/6-DOF.
- **Ch. 10 — Timing, clocking & synchronization.** Coherent vs. non-coherent
  detection, reference distribution, jitter budget, and the FDM/TDM/CDM
  multiplexing that physically separates the $M_{ij}$ (detailed in Ch. 19).
- **Ch. 11 — DSP pipeline & estimation.** The data path from ADC samples →
  channel amplitudes → coupling matrix → pose hand-off.
- **Ch. 12 — Latency & real-time constraints.** The end-to-end latency budget
  and the throughput/latency/accuracy trade that determines clinical usability.

## 8.9 A system-level error and latency view (forward reference)

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
  from primary or standardized sources (not vendor marketing) for §8.2/§8.9.
- Validate the link-budget relation (8.1) end-to-end against the Phase-5 CRLB
  sim for one concrete architecture (a small sourced numeric case study).
- Verify the claim that modern AC "dynamic metal immunity" narrows the AC/DC
  distortion gap, and quantify if so (ties to Ch. 6 open question).
- Confirm the §8.7 commercial parameter-mapping per product against primary/
  vendor sources (currently conf: med; shared with Ch. 28).

## Sources cited
- [@raab1979] canonical AC architecture & method. [@polhemus_tech] AC vendor
  lineage. [@jaeger2017] open-source AC/FDM planar-generator architecture (Anser).
  [@franz2014] medical-EMT architecture taxonomy. [@paperno2001] rotating-field
  excitation. [@plotkin2003] transmitter arrays. (Pulsed-DC architecture: see
  Ch. 1 §1.6 and Ch. 6 §6.4; link budget assembled from Ch. 4–24.)
