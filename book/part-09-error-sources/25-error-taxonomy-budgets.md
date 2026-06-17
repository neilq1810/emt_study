# Chapter 25 — Error Taxonomy, Budgets & Monte Carlo

> **Status:** DEEPENED (awaiting review) · **Part IX — Error Sources** (the whole of Part IX)
> Assembles the per-stage error contributions established across Parts II–VIII
> into one quantitative model. Citation keys resolve to
> [`../../citations/bibliography.json`](../../citations/bibliography.json).

Every preceding part introduced error: physics (distortion, Ch. 6), sensors
(noise/tolerance, Ch. 15), AFE/ADC (Ch. 16, 18), DSP (crosstalk/leakage,
Ch. 19–20), and the solver's geometric amplification (Ch. 24). This chapter is
where they are **named, classified, propagated, and summed** into a single error
budget — the scorecard (with the latency budget of Ch. 12) by which a design is
judged. We organize errors into **stochastic**, **deterministic**, and
**environmental** classes, give explicit lines for the often-overlooked
mechanisms (including **Barkhausen noise, generator noise, ambient/EM
susceptibility, bias-reference noise in biased sensors such as TMR,
signal-dependent nonlinearity/harmonic distortion, and the field-sensor-specific
offset, cross-axis, and hysteresis terms**), then
show how to combine them via **sensitivity matrices** and **Monte Carlo**.

---

## 25.1 The three error classes

| Class | Behavior | Removable by… | Enters budget as |
|---|---|---|---|
| **Stochastic** | random, zero-mean, averages with √τ | longer integration, lower-noise design | variance (RSS) |
| **Deterministic** | repeatable bias (tolerance, model mismatch, calibration residual) | calibration | bias (often signed, may not cancel) |
| **Environmental** | depends on surroundings (distortion, interference, motion) | mitigation, mapping, fusion, flagging | bias + variance, context-dependent |

The distinction is operational: **stochastic** error sets the precision floor and
shrinks with averaging; **deterministic** error sets accuracy and must be
*calibrated* (Part X), not averaged; **environmental** error is the wild card that
defeats both unless detected and handled (Ch. 21, 27). A budget that lumps them
together is misleading — the same RMS number means very different things depending
on class. *(For a flat, one-row-per-source lookup of every mechanism below — class,
scaling, combination rule, mitigation — see the **Reference → Error-Source Catalog**;
this chapter explains the* why *behind each row.)*

## 25.2 Stochastic error sources (the noise floor)

These propagate to pose via `noise / (√τ · signal) × ‖J⁻¹‖` (Ch. 15 §15.4,
Ch. 24):

1. **Sensor self-noise.** Coil Johnson noise (Ch. 15 eq. 15.1) or MR/TMR 1/f noise
   (Ch. 14.3.4) [@davies2021; @lenz2006].
2. **Barkhausen noise (magnetic sensors & ferrite cores).** Discrete, irreversible
   domain-wall jumps as magnetization changes produce a *low-frequency, often
   non-Gaussian* noise (and a hysteresis/repeatability component). In GMR/TMR free
   layers this is a principal origin of the **magnetic 1/f noise** — "thermally
   excited hopping of magnetic domain walls" — and it also afflicts
   **ferrite-cored pickup coils** [@davies2021; @lenz2006]. It is distinct from
   electronic/Johnson noise and *cannot* be designed away by the AFE; it is
   mitigated at the *device* level (single-domain or vortex-state free layers,
   longitudinal bias, set/reset flipping, Ch. 14.3.3). Because it is partly
   hysteretic, it straddles the stochastic/deterministic boundary. (conf: high —
   mechanism standard; EMT-specific magnitude to be sourced, see *Open questions*.)
3. **Bias-reference noise in biased sensors (TMR).** Unlike a passive coil, an MTJ
   is **voltage-biased**, and both its sensitivity *and* its noise scale with the
   bias voltage; noise on the **bias/reference** therefore multiplies directly
   into the signal. A notable empirical result is that TMR **detectivity stays
   roughly constant with bias** because sensitivity and noise scale together
   [@monteblanco2021] — so chasing sensitivity via higher bias does *not* by
   itself improve the field-referred floor, and an *unstable* bias injects
   correlated multiplicative error. The practical lesson: a biased sensor needs a
   **low-noise, stable voltage/current reference**, and its noise must appear as
   an explicit budget line absent for passive coils. (MTJs also carry **shot noise**
   $\propto\sqrt{I}$ at higher bias, adding to the bias-dependent floor.) (conf: med —
   per [@monteblanco2021]; magnitudes device-specific.)
4. **AFE noise.** LNA $e_n$ and $i_n|Z_s|$ (Ch. 16 eq. 16.1), kept below the
   sensor floor [@horowitz_hill].
5. **ADC quantization + thermal.** Below the floor with adequate ENOB/oversampling
   (Ch. 18); dithered to stay white [@walden1999; @ieee1241]. **Caveat:**
   *undithered* quantization is **not** white but **signal-correlated** (harmonic
   spurs) — a deterministic distortion (cf. §25.3 item 7); dither, or an adequately
   "busy" signal, is what *makes* quantization behave stochastically.
6. **Clock/jitter noise.** Aperture jitter (Ch. 10/18 eq. 18.3) — typically
   negligible at EMT frequencies.
7. **RTS / popcorn (burst) noise (MTJ/MR).** Discrete, multi-level switching from
   individual defects or domain states — **non-Gaussian and bursty**, a microscopic
   contributor to (and sometimes distinct from) the magnetic/electronic 1/f of item 1.
   It matters for the **Monte-Carlo tails** (§25.6), not just the variance, and is
   reduced by larger junctions, averaging, and set/reset [@davies2021]. (conf: med —
   mechanism standard for MTJs; EMT-specific magnitude device-specific.)
8. **Cable microphonic & dielectric noise.** Mechanical vibration or flex of the
   sensor cable modulates its capacitance and, via triboelectric/piezoelectric charge,
   injects a **random, vibration-driven** component onto the µV signal — the
   *stochastic* sibling of the deterministic cable drift of §25.4 item 5. Mitigated by
   low-noise / low-triboelectric cable, strain relief, and bonding/guarding
   (Ch. 16 §16.3, Ch. 17 §17.2).

These combine (when independent) in **root-sum-square**; the largest term is the
one to attack.

## 25.3 Deterministic error sources (the bias floor)

1. **Sensor/generator tolerances** — area-turns, axis, inter-element angle
   (Ch. 15 §15.1); mostly removed by per-unit calibration (Ch. 26).
2. **Forward-model mismatch** — dipole vs. real cored generator (Ch. 7 §7.2);
   residual after field-mapping is a bias.
3. **Calibration residual** — the part of (1)–(2) the calibration could not
   capture; the irreducible deterministic floor.
4. **Channel crosstalk / spectral leakage** — FDM filter/nonlinearity leakage
   (Ch. 19 §19.2), non-coherent-sampling leakage (Ch. 20) — *correlated* biases on
   $M_{ij}$.
5. **Thermal drift** — of coil area/core, MR offset, bias reference, and
   electronics gain; drift *after* calibration is the leading recalibration driver
   (Ch. 15 §15.5).
6. **Numerical error** — ill-conditioned solves, finite precision (Ch. 22 §22.4,
   Ch. 24 §24.2).
7. **Sensor & front-end nonlinearity → harmonic/intermodulation distortion.** The
   chain is *assumed* linear (measured amplitude $\propto M_{ij}$), but no element is:
   a **ferrite-cored** pickup approaches B–H saturation/hysteresis in strong field
   (near the generator); an **MR/TMR** sensor has an intrinsically **nonlinear
   transfer curve** — linear only over a bias-set span, saturating beyond (Ch. 14.3);
   the **AFE** has finite THD/IP3 (Ch. 16); the **ADC** has INL (Ch. 18); and the
   **generator drive** has its own THD (Ch. 37 §37.2). It hurts the pose two ways:
   (i) **amplitude compression** — the apparent coupling no longer scales correctly
   with field, biasing inferred range/bearing; and (ii) **harmonic & intermodulation
   generation** — energy at $2\omega_0,3\omega_0,\dots$ and at FDM sum/difference
   tones that **folds into other channels** (the crosstalk of item 4, Ch. 19 §19.2)
   and **biases the lock-in** (a square-wave reference detects the odd harmonics,
   Ch. 20 §20.4). What makes it worse than an ordinary calibratable bias is that it is
   **signal-amplitude-dependent**, and the signal swings $\sim1/r^3$ (≈60 dB) across
   the volume (Ch. 9 §9.6): a transfer-curve correction fit near the generator
   **mis-corrects at the edge**, so it is a *pose-dependent* bias needing an
   amplitude-aware (2-D) calibration — or, better, operation kept within the linear
   region (gain ranging / signal scaling, Ch. 16 §16.4), a low-THD drive and a
   **sine** reference with band-limiting (Ch. 20 §20.4), and FDM frequency planning
   that keeps no channel on another's harmonic (Ch. 19 §19.2). Usefully, the
   **harmonic content is itself a saturation/nonlinearity flag** the detect-and-flag
   layer can watch (Ch. 27), complementary to the quadrature distortion signature of
   Ch. 20 §20.10. (conf: high — mechanism standard; per-device THD / MR-curve
   magnitudes to be sourced.)

8. **Cross-axis (transverse) sensitivity & non-orthogonality.** A sense axis
   responding to fields *off* its nominal axis — **geometric** (triad coils not
   exactly orthogonal, cf. item 1) or **intrinsic** (an MR element's transverse
   sensitivity, Ch. 14.3). It appears as **off-diagonal terms in the $3\times3$
   sensor response matrix**, mixing the coupling across DOF. Largely removed by
   calibrating the full sensor matrix (Ch. 26/55); the residual and its drift remain.
9. **Sensor offset & offset drift.** A passive coil reads $\dot B$ and has **no**
   zero-field output, but a **field sensor (MR/TMR/Hall)** has a DC **offset** (bridge
   imbalance) and, worse, **offset drift** with temperature, time, and magnetic
   history. The static offset calibrates out; the drift/history-dependence is the
   residual, mitigated at the device level by **set/reset flipping and chopping**
   (Ch. 14.3). Architecture matters: **AC (lock-in) and pulsed-DC (step-differencing)
   detection both reject a *static* offset** — and the DC geomagnetic background —
   so offset chiefly bites where the static field is read directly and imperfectly
   rejected.
10. **Hysteresis (history-dependent bias).** Ferrite cores and MR free layers are
    hysteretic: the output depends on the magnetic *history*, not only the present
    field. This **breaks the calibratable-bias assumption** — one cannot subtract a
    single value that depends on the path taken — so hysteresis appears as a
    *non-repeatable* bias (the deterministic sibling of Barkhausen noise, §25.2 item 2).
    Mitigation is device-level: soft / low-remanence materials, set/reset, and staying
    on the small-signal linear minor loop (away from the saturating regime of item 7).
11. **Amplifier gain & offset error.** Distinct from AFE *noise* (the voltage/current
    noise $e_n,i_n$ of §25.2 item 4): a finite, possibly drifting **gain error**
    (multiplicative → a range bias, cube-root-forgiving, calibrated per channel — the
    gain identification of Ch. 55 §55.3) and a DC **offset** (additive). As in item 9,
    a lock-in **rejects** static amplifier offset (Ch. 20), so offset matters mainly in
    DC-coupled paths; gain error and its drift remain a deterministic line.

**A coil-vs-field-sensor note.** Items 9–10 (offset, hysteresis) and the *intrinsic*
part of item 8 are largely **absent for an air-cored induction coil** — inherently
linear, DC-blind, and offset-free — and **present for MR/TMR/Hall field sensors** (and,
mildly, ferrite-cored coils). The error *profile* therefore shifts with the sensor
technology of Ch. 13–14, and the AC-vs-pulsed-DC architecture sets which of these the
detection rejects for free. *(Less-common further sources, for completeness:
**magnetostriction / stress sensitivity** of a cored sensor under catheter flex; the
**DC geomagnetic background** an unprotected field sensor must reject; and hard
**overload / clipping** near the generator or from an interferer — the saturating limit
of item 7 and the dynamic-reserve bound of Ch. 20 §20.4.)*

Deterministic errors do **not** average away and may not cancel across DOF; they
are budgeted as (often signed) biases and propagated through the same Jacobian.

## 25.4 Environmental error sources

1. **Field distortion** — eddy-current (conductors) and ferromagnetic (Ch. 6).
   The dominant environmental term: ferromagnetic/electrical devices in the OR
   can induce translation errors up to **8.4 mm RMS and rotation up to 166°**,
   though they can be identified and kept at distance [@poulin2002].
2. **Ambient EM interference / susceptibility.** Background EM noise from OR
   equipment. Reassuringly, measured *ambient-noise* error (as opposed to
   distortion) can remain **below ~0.15 mm RMS** even in an OR — i.e. broadband
   ambient noise is usually *not* the limiting term; **distorters and
   ferromagnetics are** [@poulin2002; @yaniv2009]. This is the in-situ counterpart
   to the IEC 60601-1-2 immunity requirements (Ch. 17 §17.3) [@iec60601_1_2].
3. **Generator (transmitter-side) noise.** Drive-current noise, power-amplifier
   noise, and excitation **frequency/phase/amplitude instability** modulate the
   *transmitted* field, so the error appears **correlated across all receive
   channels** (it scales the whole coupling matrix), unlike per-channel receiver
   noise. It is bounded by a low-noise, stable drive and a clean reference
   (Ch. 9 §9.4, Ch. 10) and partly cancelled in *ratiometric* schemes that
   normalize sensor output by a monitored drive sample. It deserves an explicit
   budget line because its correlation structure means it does **not** RSS like
   independent receiver noise. (conf: med — correlated-error reasoning is standard;
   EMT-specific magnitudes to be sourced.)
4. **Motion effects** — intra-frame TDM skew (Ch. 19 §19.6) and latency-induced
   dynamic error (Ch. 12 §12.3): ~1 mm at 0.1 m/s with 10 ms latency.
5. **Cable effects** — triboelectric/flex noise, capacitance shift (Ch. 16 §16.3,
   Ch. 17 §17.2).
6. **Synchronization errors** — phase-reference drift in coherent detection
   (Ch. 10).

## 25.5 Sensitivity matrices: propagating to pose

Each error source $p$ maps to pose error through the forward-model Jacobian
(Ch. 23–24):

$$
\delta\mathbf{x} \approx (\mathbf{J}^\top\mathbf{R}^{-1}\mathbf{J})^{-1}\mathbf{J}^\top\mathbf{R}^{-1}\,\frac{\partial h}{\partial p}\,\delta p .
$$

The matrix $\partial h/\partial p$ (the **sensitivity matrix**) tells you *which
error hurts which DOF and where in the volume*. Two structural facts recur:

- The mapping is **pose-dependent and conditioning-weighted** (Ch. 24): the same
  $\delta p$ produces far larger $\delta\mathbf{x}$ in weakly observable / poorly
  conditioned regions (volume edges, near ambiguities).
- **Correlated** sources (generator noise, crosstalk) must be propagated with
  their cross-terms — they can add coherently across channels and so are *not*
  reduced by the channel averaging that tames independent noise.

Stochastic terms combine as variances (covariance addition, RSS); deterministic
terms combine as biases (signed, worst-case or RSS depending on independence);
the result is a per-pose error mean and covariance.

### The law of propagation of uncertainty (GUM)
The rigorous, standardized way to combine the contributions is the **GUM**
(*Guide to the Expression of Uncertainty in Measurement*) [@gum2008]. For a
measurand $y=f(x_1,\dots,x_N)$, the **combined standard uncertainty** is

$$
u_c^2(y) = \sum_{i=1}^{N} c_i^2\,u^2(x_i)
\;+\; 2\!\sum_{i=1}^{N-1}\sum_{j=i+1}^{N} c_i\,c_j\,u(x_i,x_j),
\qquad c_i=\frac{\partial f}{\partial x_i},
\tag{25.1}
$$

with $c_i$ the **sensitivity coefficients** (here the columns of the pose
sensitivity map above) and $u(x_i,x_j)$ the covariances. Two regimes:

- **Independent sources** ($u(x_i,x_j)=0$): the cross-terms vanish and (25.1) is
  the familiar **root-sum-square** — the rule for sensor/AFE/ADC noise.
- **Correlated sources** ($u(x_i,x_j)\neq0$): the cross-terms *do not* vanish. For
  **fully correlated** contributions (generator-drive noise common to every
  channel, §25.4) the combination tends toward a **linear sum**, not RSS — which
  is why such a term can dominate even when each channel's contribution looks
  small, and why it gets its own budget line.

GUM also distinguishes how each $u(x_i)$ is *evaluated*: **Type A** by statistical
analysis of repeated observations (e.g. a measured jitter or noise-floor RMS), and
**Type B** by other means (datasheet limits, calibration certificates, a physics
model, prior data) [@gum2008]. The reported figure is then the **expanded
uncertainty** $U = k\,u_c$ with coverage factor $k$ ($k=2$ for ~95% under
approximate normality) — the form a clinical/regulatory accuracy claim should take
(Ch. 29). This is the metrology backbone of the budget table in §25.7.

## 25.6 Monte Carlo uncertainty analysis

Linear sensitivity propagation (25.5) is a first-order approximation that breaks
down with strong nonlinearity, non-Gaussian noise (Barkhausen, RTS/popcorn), ambiguities, or
large distortion. The general tool is **Monte Carlo**:

1. Sample each error source from its modeled distribution (with correct
   correlations — e.g. generator noise common across channels).
2. Run the full forward model + solver (Parts VIII) per sample.
3. Accumulate the pose-error distribution over the working volume.

Monte Carlo captures the **non-Gaussian tails** (outliers from distortion,
ambiguity-induced bimodality) that the CRLB/covariance (Ch. 24) understates, and
validates the linear sensitivity analysis where it is valid. It directly backs the
"Monte Carlo uncertainty" and "error propagation" interactive modules of the
project brief (Phase 5).

## 25.7 Assembling the error budget

The deliverable of Part IX is a **table** with one row per source, each tagged by
class, with its magnitude, its pose-error contribution (via 25.5), and its
combination rule:

| Source | Class | Mechanism (chapter) | Combine as | Mitigation |
|---|---|---|---|---|
| Coil/MR sensor noise | stochastic | Ch. 15, 14.3 | RSS | moment, integration, area |
| Barkhausen / domain noise | stochastic(+hyst.) | Ch. 14.3, 25.2 | RSS (+bias) | single-domain/vortex layer, set/reset |
| Bias-reference noise (TMR) | stochastic(×bias) | 25.2 | RSS, multiplicative | stable low-noise reference |
| AFE / ADC noise | stochastic | Ch. 16, 18 | RSS | keep below sensor floor |
| RTS / popcorn noise (MTJ) | stochastic (non-Gaussian) | Ch. 14.3, 25.2 | RSS (+ tails) | larger junction, set/reset, averaging |
| Cable microphonic / dielectric | stochastic | Ch. 16/17, 25.2 | RSS | low-tribo cable, strain relief, guarding |
| Tolerance / model mismatch | deterministic | Ch. 7, 15 | bias | calibration (Ch. 26) |
| Crosstalk / leakage | deterministic | Ch. 19, 20 | bias (correlated) | TDM, guard bands, coherent sampling |
| Thermal drift | deterministic | Ch. 15 | bias (drifting) | stability, recalibration |
| Nonlinearity / harmonic distortion | deterministic (signal-dependent) | Ch. 14/16/18/20, 25.3 | bias (amplitude-/pose-dependent) + harmonic crosstalk | linear region, gain ranging, low-THD drive, sine ref, FDM plan |
| Cross-axis / non-orthogonality | deterministic | Ch. 14/15, 25.3 | bias (off-diagonal, mixes DOF) | 3×3 sensor-matrix calibration |
| Sensor offset & drift (field sensors) | deterministic | Ch. 14.3, 25.3 | bias (additive, drifting) | set/reset, chopping; AC & pulsed-DC reject static offset |
| Hysteresis | deterministic (history-dep.) | Ch. 14, 25.3 | non-repeatable bias | soft materials, set/reset, linear minor loop |
| Amplifier gain / offset | deterministic | Ch. 16, 25.3 | gain = mult. bias; offset rejected by AC lock-in | per-channel gain cal |
| Field distortion | environmental | Ch. 6 | bias + outliers | mapping, fusion, flagging (Ch. 27, 21) |
| Ambient EM / susceptibility | environmental | 25.4, Ch. 17 | RSS (usually small) | shielding/band-select, EMC (60601-1-2) |
| Generator noise | environmental | 25.4, Ch. 9 | correlated (not RSS) | low-noise drive, ratiometric |
| Motion / latency | environmental | Ch. 12, 19 | bias (dynamic) | simultaneity, prediction, fusion |
| Cable / sync | environmental | Ch. 16, 17, 10 | bias + noise | cable discipline, coherent ref |

The bottom line is a **per-pose pose-error mean and covariance**, summed by class,
mapped across the working volume — the quantitative answer to "how accurate is
this system, where, and why," and the input to the clinical requirements of
Ch. 29 and the from-scratch design of Ch. 31.

### Worked example — propagating one source of each class
Before tabulating the whole budget, here is the **method applied end-to-end** to
one representative source of each class, at the mid-volume pose $z=0.3$ m of the
Ch. 31 design. Each step is: identify the source, find its **sensitivity
coefficient** $c=\partial(\text{position})/\partial(\text{source})$ (§25.5,
eq. 25.1), evaluate its **standard uncertainty** (GUM Type A or Type B, §25.5),
and propagate.

**(1) Stochastic — sensor + AFE field-referred noise.** Evaluated *Type A* (from
the measured noise floor) as $\sigma_B = 0.9\,\text{nT}$ (1σ). The sensitivity is
the CRLB gain — the inverse-Jacobian mapping from field noise to position — which
the Phase-5 simulation gives at $z=0.3$ m as
$c_1 = 0.086\,\text{mm/nT}$ (Ch. 24; position $\sigma$ scales linearly with
$\sigma_B$). Hence
$$
u_1 = c_1\,\sigma_B = 0.086\,\tfrac{\text{mm}}{\text{nT}}\times 0.9\,\text{nT}
= 0.077\,\text{mm}.
$$

**(2) Deterministic — per-channel gain calibration residual.** Evaluated *Type B*
as a bound: the calibration leaves a residual gain error of at most
$\varepsilon = \pm0.2\%$. The sensitivity coefficient follows from the dipole
range law: the measured amplitude $A\propto r^{-3}$, so
$\dfrac{\mathrm dr}{r} = -\dfrac13\dfrac{\mathrm dA}{A}$, i.e.
$c_2 = \partial r/\partial\varepsilon = r/3 = 100\,\text{mm}$. The cube-root is
forgiving — **a 0.2% gain error becomes only a 0.067% range error**:
$$
\delta r = c_2\,\varepsilon = 100\,\text{mm}\times 0.002 = 0.20\,\text{mm (bound)}
\;\Rightarrow\; u_2 = \frac{0.20}{\sqrt3} = 0.115\,\text{mm}
$$
(the $/\sqrt3$ converts a rectangular Type-B *bound* to a standard uncertainty).

**(3) Environmental — a nearby conductor (eddy distortion).** A 5 cm conductor at
$d_t = 0.3$ m from the generator and $d_s = 0.2$ m from the sensor. The *raw*
distortion fraction is (Ch. 6, eq. 6.4)
$$
\eta = \frac{a^3 r^3}{d_t^3 d_s^3}
= \frac{(0.05)^3(0.3)^3}{(0.3)^3(0.2)^3} = 1.56\% .
$$
Static field-mapping (Ch. 27) typically suppresses a fixed distorter by
$\sim$8×, leaving a residual $\eta_\text{res}\approx0.20\%$. Propagating this like
a fractional field error through the same $r/3$ range sensitivity (plus a
comparable lateral/bearing term) gives a positional bound $\delta x\approx
0.30\,\text{mm}$, so $u_3 = 0.30/\sqrt3 = 0.17\,\text{mm}$ (Type B).

**Combine (independent → RSS, eq. 25.1).** The three sources are uncorrelated, so
the cross-terms vanish and
$$
u_c = \sqrt{u_1^2 + u_2^2 + u_3^2}
= \sqrt{0.077^2 + 0.115^2 + 0.17^2} \approx 0.22\,\text{mm},
$$
and the **expanded uncertainty** (coverage factor $k=2$, ~95%) is
$U = 2u_c \approx 0.44\,\text{mm}$.

Three takeaways the calculation makes concrete: (i) the **cube-root forgiveness**
($c\propto r/3$) means gain and distortion errors hurt range *three times less*
than their raw fractional size; (ii) the environmental term, even after mapping,
is the **largest single contributor** — the recurring EMT lesson; and (iii) the
*method* is uniform across classes (sensitivity coefficient × standard
uncertainty, then combine) even though the *evaluation* differs (Type A noise vs.
Type B bounds). The full budget below simply repeats this for every row.

### A worked numeric position budget (mid-volume)
For the Ch. 31 example (0.5 m volume) at a well-conditioned mid-volume pose
($z=0.3$ m), using the Phase-5 mapping that a field-referred noise
$\sigma_B=1\,\text{nT}$ yields a CRLB position $\sigma\approx0.086$ mm (Ch. 24,
`data/crlb_vs_range.csv`), and the ambient/distortion magnitudes of Poulin & Amiot
[@poulin2002]. Values are **illustrative** (design-dependent; conf: med), but the
*method* and combination rules are exact:

| Source | Class / eval | Input | → position σ [mm] | Combine |
|---|---|---|---|---|
| Coil Johnson + AFE noise | stochastic / A | ~0.8 nT | 0.069 | RSS |
| ADC quantization+thermal | stochastic / A | ~0.4 nT | 0.034 | RSS |
| Clock jitter | stochastic / B | negligible @10 kHz | <0.005 | RSS |
| **Stochastic subtotal** | | RSS → ~0.90 nT | **≈ 0.077** | — |
| Calibration residual | deterministic / B | per-unit map | 0.20 | bias (RSS) |
| Thermal drift since cal. | deterministic / B | warm-up spec | 0.10 | bias (RSS) |
| Static distortion (mapped residual) | environmental / B | installation | 0.30 | bias |
| Ambient EM noise | environmental / A | OR-measured | <0.15 | RSS |
| Generator drive noise | environmental / B (corr.) | ratiometric | 0.05 | linear (correlated) |
| **Combined std. uncertainty $u_c$** | | (25.1) | **≈ 0.42** | — |
| **Expanded $U=2u_c$ (95%)** | | $k=2$ | **≈ 0.84** | — |

So the static, well-conditioned mid-volume accuracy is $\sim0.8$ mm (95%) —
inside the ≤1 mm target (Ch. 31), consistent with standardized assessments
[@hummel2005]. **The conditions matter as much as the number:** at the volume edge
the stochastic term alone grows ~8× ($z^4$, Ch. 24), and a *moving* ferromagnetic
distorter or fast target motion (Ch. 12 §12.3, ≈1 mm at 0.1 m/s × 10 ms) are
**separate operating conditions** that blow this budget — which is precisely why
the clinical claim is stated as "within $X$ mm under stated conditions, **or flag
loss of tracking**" (Ch. 29 essential performance).

### Top-down allocation
The same table runs **backwards** as a design tool: given a target (say $U\le1$ mm
at the edge), allocate it across classes — e.g. budget ≤0.5 mm stochastic (sets
the required $\sigma_B$, hence the coil/AFE/ADC noise and generator moment via the
CRLB, Ch. 9/15/16), ≤0.3 mm deterministic (sets the calibration/stability spec,
Ch. 26), ≤0.7 mm environmental (sets the distortion-compensation requirement,
Ch. 27) — then RSS the allocations back to the target. This closes the design loop
of Ch. 31: the budget is both a *scorecard* and a *requirements generator*.

---

## Open questions / to verify
- Source EMT-specific *magnitudes* for Barkhausen, generator-side, and
  bias-reference noise (currently mechanism-cited; magnitudes device/system
  specific). Candidate: dedicated MTJ noise-vs-bias and Barkhausen/vortex
  free-layer studies (arXiv:2103.04750 published version; vortex-state spin-valve
  noise papers).
- ✅ **Partially resolved:** a worked numeric position budget (§25.7) now combines
  classes via the GUM law of propagation (25.1) to a combined/expanded uncertainty,
  using the Phase-5 CRLB mapping. Remaining: drive it from a Phase-5 Monte-Carlo
  run (not first-order) and replace the illustrative per-line magnitudes with
  sourced/measured values.
- Quantify the **nonlinearity / harmonic-distortion** line (§25.3 item 7): a Phase-5
  sim of amplitude compression vs range and harmonic folding into FDM channels for a
  representative sensor THD / MR-curve, to replace the mechanism-only treatment with a
  pose-error magnitude (ties Ch. 14/16/19/20).
- Confirm Poulin & Amiot figures (8.4 mm / 166°; 0.15 mm ambient) against the
  primary text and add the exact measurement conditions [@poulin2002].

## Sources cited
- [@gum2008] uncertainty budgeting (Type A/B, law of propagation, expanded
  uncertainty). [@davies2021; @lenz2006] MR/Barkhausen/1f noise mechanisms.
  [@monteblanco2021] TMR bias-voltage/detectivity (bias-reference term).
  [@poulin2002] OR interference & ambient-noise magnitudes. [@hummel2005]
  standardized assessment. [@yaniv2009] clinical environment. [@iec60601_1_2] EMC
  immunity. [@horowitz_hill; @walden1999; @ieee1241] AFE/ADC noise. Propagation/CRLB
  from Ch. 24.
