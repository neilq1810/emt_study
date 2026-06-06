# Chapter 19 — Excitation & Channel Separation

> **Status:** DRAFT · **Part VII — Digital Signal Processing**
> Opens Part VII. Develops the multiplexing introduced architecturally in Ch. 10
> §10.1. Feeds Ch. 20 (detection). Citation keys resolve to
> [`../../citations/bibliography.json`](../../citations/bibliography.json).

A 6-DOF tracker must measure the nine couplings $M_{ij}$ between three transmit
axes and three sense axes (Ch. 5). But a sensor axis produces a single voltage
that superposes all transmit axes (Ch. 5 §5.6). **Channel separation** is the
DSP problem of recovering the individual $M_{ij}$ from that superposition, and it
is solved by designing the *excitation* so the transmit axes are
distinguishable. This chapter develops the three classical multiplexing schemes
— frequency, time, and code division — plus orthogonal excitation, and quantifies
the trades among **update rate, bandwidth, distortion, and crosstalk** that the
architecture chapter (Ch. 10) introduced.

---

## 19.1 The separation problem, formally

Let transmit axis $i$ be driven by waveform $s_i(t)$. The sensor axis $j$ sees

$$
\varepsilon_j(t) = -\sum_{i=1}^{3} M_{ij}\,\dot s_i(t) + n_j(t),
$$

with $n_j$ the noise (Parts IV–VI). Recovering the nine $M_{ij}$ requires the set
$\{s_i(t)\}$ to be **separable** by the receiver — orthogonal in frequency, time,
or code. The choice of $\{s_i\}$ is the single design decision that determines
update rate, the bandwidth consumed, the distortion behavior, and the DSP cost.

## 19.2 Frequency-division multiplexing (FDM)

Drive each transmit axis at a distinct frequency: $s_i(t)=\cos(\omega_i t)$ with
$\omega_1,\omega_2,\omega_3$ separated by guard bands. All three axes radiate
**simultaneously and continuously**; the receiver separates them by frequency
(an FFT or three parallel lock-ins at $\omega_1,\omega_2,\omega_3$, Ch. 20).

- **Pros.** Maximum simultaneity → highest update rate (no axis waits for
  another); naturally extends to multiple transmitters/sensors; each channel is
  a clean single-tone estimation problem.
- **Cons.** Consumes **bandwidth** (guard bands to prevent overlap); demands
  **crosstalk control** — imperfect filters or nonlinearity (ADC INL, Ch. 18;
  amplifier distortion, Ch. 16) leak energy between bins and corrupt $M_{ij}$;
  and each frequency has its **own eddy-current distortion** (Ch. 6 §6.2 — eddy
  effects are frequency-dependent), so the per-axis forward models differ and
  must be calibrated per frequency (Ch. 26).
- **Frequency-bin spacing** must satisfy $|\omega_i-\omega_k|\gg 1/\tau$ (the
  integration time $\tau$ sets the bin resolution); this couples FDM channel
  spacing to update rate.

## 19.3 Time-division multiplexing (TDM)

Energize one transmit axis at a time in sequence. Each sense axis is sampled
within the active slot for the active transmit axis, so $M_{ij}$ is read almost
directly.

- **Pros.** **Simplest, cleanest decode** — no inter-axis crosstalk because only
  one axis is on; each slot can include its own **settling wait** (ideal for
  pulsed-DC eddy management, Ch. 6 §6.4); only one drive amplifier need be active.
- **Cons.** Update rate divided by the number of axes/transmitters:
  $f_\text{update}\approx 1/(N_\text{slots}\,t_\text{slot})$, $t_\text{slot}=$
  settling + integration; and — critically — **target motion *between* slots**
  introduces a skew: the three axes are measured at slightly different instants,
  so a moving sensor's $M_{ij}$ are mutually inconsistent, biasing the solver
  (Ch. 11/23) unless motion-compensated.

## 19.4 Code-division multiplexing (CDM) and orthogonal excitation

Drive all axes simultaneously but with **mutually orthogonal codes** (e.g.
pseudo-random sequences, or orthogonal modulation of a carrier): $s_i(t)$ chosen
so $\int s_i s_k\,dt = E\,\delta_{ik}$ over the integration window. The receiver
correlates against each code to recover each $M_{ij}$.

- **Pros.** Simultaneous like FDM (high rate) but **spreads energy** so it is
  robust to narrowband interference and offers **processing gain**; flexible for
  many transmitters.
- **Cons.** Most complex DSP (correlators, code/sync design, Ch. 10); code
  cross-correlation must be low or residual leakage biases $M_{ij}$; bandwidth
  use can be large.

**Orthogonal excitation** more generally means choosing *any* basis of
separable waveforms — the **rotating-field** method of Paperno et al. is a
related idea, encoding axis information into the phase/amplitude of a
two-axis-generated rotating field [@paperno2001], and transmitter-array systems
combine spatial and temporal coding [@plotkin2003]. The unifying principle is the
orthogonality integral above.

## 19.5 The trade space (quantified)

| Criterion | TDM | FDM | CDM |
|---|---|---|---|
| Simultaneity / update rate | low (÷ N) | high | high |
| Bandwidth used | narrow | wide (guard bands) | wide (spread) |
| Crosstalk risk | minimal | filter/nonlinearity-limited | code-correlation-limited |
| Distortion handling | per-slot settling (great for pulsed-DC) | per-frequency calibration | spread |
| Motion artifact | inter-slot skew | minimal (simultaneous) | minimal (simultaneous) |
| DSP complexity | low | medium (FFT/parallel lock-in) | high (correlators) |
| Natural fit | pulsed-DC; few axes | continuous AC; high rate | many emitters; interference |

**Design rules of thumb** (conf: med — engineering practice consistent with the
multiplexing literature and Ch. 10): use **TDM** when distortion cleanliness and
simplicity dominate and the target is slow (or motion is compensated); use **FDM**
when update rate is paramount and bandwidth/crosstalk can be managed; use **CDM**
when many emitters or hostile interference demand processing gain. Hybrid schemes
(e.g. TDM across transmitters, FDM across axes) are common.

## 19.6 The motion problem and why it shapes the choice

For a target moving at velocity $v$, TDM's inter-slot skew $\Delta t$ produces a
position inconsistency $\sim v\,\Delta t$ between axes measured at different
times. At a catheter speed of $0.1\,\text{m/s}$ and a 3-slot frame at, say,
$\Delta t=3\,\text{ms}$ between first and last axis, that is $\sim0.3\,\text{mm}$
of skew — comparable to the static accuracy budget (Ch. 1, [@hummel2005]). This
is a concrete reason high-update or fast-motion applications lean toward **FDM/CDM
simultaneity**, or apply explicit motion compensation in the solver/estimator
(Ch. 21). It is the same kinematic argument as the latency discussion of Ch. 12
§12.3, now applied *within* a measurement frame. (conf: high — direct
kinematics.)

---

## Open questions / to verify
- Quantify achievable FDM crosstalk vs. guard-band/ADC-SFDR for a concrete
  design (ties Ch. 18 §18.2); add as a notebook (Phase 5).
- Source which commercial systems use TDM vs FDM vs hybrid (Ch. 28), with a
  primary/vendor citation each, rather than asserting.
- Add a worked CDM correlation-leakage budget and code-length vs. update-rate
  trade.

## Sources cited
- [@paperno2001] rotating-field/orthogonal excitation. [@plotkin2003]
  transmitter-array spatio-temporal coding. [@hummel2005] static-accuracy scale
  for the motion-skew comparison. Detection math follows in Ch. 20.
