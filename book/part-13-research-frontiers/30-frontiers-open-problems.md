# Chapter 30 — Research Frontiers & Open Problems

> **Status:** DRAFT · **Part XIII — Research Frontiers** (the whole of Part XIII)
> Surveys the state of the art and what remains unsolved. Citation keys resolve to
> [`../../citations/bibliography.json`](../../citations/bibliography.json).

Electromagnetic tracking is mature in its core physics (Part II) but far from
finished as an engineering discipline. The enduring weaknesses — distortion
(Ch. 6), the accuracy/rate/latency trilemma (Ch. 12), and the size/SNR tension of
miniature sensors (Ch. 14) — define the research agenda. This chapter surveys the
active frontiers: **hybrid optical+EM/IMU** systems, **AI-assisted calibration and
ML distortion compensation**, **novel sensors** (TMR/MR arrays and quantum/atomic
magnetometry), and the **open problems** that a next-generation system must solve.
Throughout, the frontier is judged against the *real* EMT constraints — dynamic
range, bandwidth, working-volume fields, miniaturization, and clinical robustness
— not against headline sensitivity numbers that may be irrelevant to the actual
problem.

---

## 30.1 State of the art and leading directions

Today's best clinical/OEM systems deliver roughly millimetre, sub-degree static
accuracy under controlled conditions (Ch. 1, 28) [@hummel2005; @yaniv2009], with
the gap between *lab* and *in-situ* performance set largely by **distortion and
registration** (Ch. 25, 29). The research community (academic groups in medical
navigation, magnetics, and estimation; spinouts pursuing chip-scale and
compensation methods, Ch. 28.6) is therefore concentrated less on the core dipole
physics than on **robustness, miniaturization, and intelligent compensation**.
The three threads below are not independent — the most promising systems combine
them.

## 30.2 Hybrid optical + EM (+ IMU) systems

The single most practical frontier is **fusion** (Ch. 21), because the modalities
are genuinely complementary (Ch. 13 §13.4, Ch. 21 §21.5):

- **EM + optical.** Optical is accurate and drift-free but occludable; EM is
  robust to occlusion but distortion-prone. Fusing them yields accuracy when the
  optical line of sight exists and continuity when it does not — and lets each
  *cross-check* the other (an EM/optical disagreement flags distortion).
- **EM + IMU.** The IMU supplies high-rate, low-latency, distortion-immune motion
  (attacking the latency trilemma, Ch. 12) and can resolve a 5-DOF coil's roll
  (5→6 DOF, Ch. 13). EM supplies the drift-free absolute reference.

Open challenges: rigorous **time alignment** across modalities (Ch. 12 §12.5),
online **cross-modality calibration**, and principled handling of the moment when
modalities *disagree* (which to trust, and how to communicate the resulting
uncertainty to a clinician or robot). These are estimation and systems problems,
not physics problems, and are tractable — which is why fusion is the
nearest-term frontier.

## 30.3 AI-assisted calibration and ML distortion compensation

ML is being applied to exactly the errors that resist parametric models (Ch. 27):

- **Learned calibration / field maps** mapping raw→true pose, including
  orientation, where polynomial/interpolation models struggle
  [@kindratenko2005].
- **Witness-sensor + learned distortion models** that *identify and compensate* a
  moving distorter from its field signature — demonstrated reducing C-arm error to
  1.52 mm RMS [@cavaliere2023].
- **Online / uncertainty-aware compensation** that adapts during a procedure and
  reports confidence.

The frontier's hard part is the same one Ch. 27 §27.5 flags as a *risk*:
**generalization and trustworthiness**. A model that works in the training room
may fail silently elsewhere; for a regulated medical device (Ch. 29), ML
compensation must be paired with **uncertainty quantification** (Ch. 24),
**out-of-distribution detection**, and the **detect-and-flag** fallback (Ch. 27
§27.4). Demonstrating generalization across rooms/distorters — not just in-sample
accuracy — is the open research and regulatory problem. (conf: high — standard ML-
safety reasoning applied to EMT.)

## 30.4 Novel sensors

### TMR / MR arrays
The magnetoresistive frontier (Ch. 14.3) pushes toward **chip-scale, low-power,
arrayed** field sensing: dense TMR/MR arrays enable many simultaneous sense points
(complementing transmitter arrays, Ch. 9 / [@plotkin2003]) and chip-integrated
front ends. The binding constraint is **low-frequency detectivity at catheter die
sizes** — area-limited 1/f/Barkhausen noise (Ch. 14.3.4, Ch. 25 §25.2)
[@davies2021] — with bias-stable, set/reset/chopped operation needed to approach
useful field-referred noise, and detectivity that stays roughly constant with bias
[@monteblanco2021]. Progress here would unlock pulsed-DC/chip-scale architectures
the coil cannot serve.

### Quantum / atomic magnetometry — promise vs. EMT reality
**Optically pumped (atomic) magnetometers** reach extraordinary sensitivity —
SERF devices exceed $10^{-15}\,\text{T}/\sqrt{\text{Hz}}$ [@budker2007] — and
**NV-diamond** magnetometers offer high sensitivity in a solid-state, potentially
microscale package [@barry2020]. Their natural medical home is **biomagnetic
sensing** (MEG/MCG), where the target fields are fT–pT.

For *EMT specifically*, the honest assessment is more nuanced (conf: med — frontier
judgment):
- EMT does **not need** fT sensitivity; its signals are µT-class (Ch. 4 §4.7). The
  binding needs are **dynamic range** (~100 dB, Ch. 9 §9.6), **bandwidth**,
  **operation in the presence of large applied fields**, and **miniaturization** —
  none of which are the strengths SERF/NV optimize for.
- SERF magnetometers operate near *zero field* and have limited dynamic range and
  bandwidth, which is awkward for the structured µT fields EMT deliberately
  creates; NV sensors face readout-fidelity and dynamic-range limits and are "far
  from theoretical limits" today [@barry2020].
- The plausible near-term role is therefore **niche/hybrid** (e.g. ultra-sensitive
  pickup for very-low-field or deep-volume regimes, or biomagnetic co-sensing),
  not wholesale replacement of pickup coils or MR bridges. This is a place where
  the literature's excitement must be matched against EMT's actual requirements.

### MEMS and other approaches
CMOS-MEMS Lorentz-force/resonant magnetometers (Ch. 14.4) offer integration at the
cost of thermomechanical noise; continued co-integration with the AFE (Part V) is
an engineering frontier.

## 30.5 Open problems

A consolidated list of what remains genuinely unsolved (each cross-referenced to
where the book frames it):

1. **Robust real-time compensation of *moving* distorters** without per-room
   training — the central unsolved problem (Ch. 6, 27) [@cavaliere2023].
2. **Trustworthy ML in a regulated loop** — generalization, OOD detection,
   calibrated uncertainty (Ch. 24, 27, 29).
3. **Catheter-scale sensors with DC capability and adequate detectivity** —
   pushing TMR/MR below the area-limited noise floor at sub-mm sizes (Ch. 14, 25)
   [@davies2021; @monteblanco2021].
4. **Beating the accuracy/rate/latency trilemma** for fast-moving targets — better
   per-sample information (moment, low-noise AFE) and fusion/prediction (Ch. 12,
   21).
5. **Standardization & comparability** — extending Hummel-style protocols to
   *dynamic* and *distortion* conditions so vendor/clinical claims are comparable
   (Ch. 26, 28) [@hummel2005].
6. **System-level clinical accuracy** — attacking the dominant *registration* and
   *motion* terms (Ch. 29), since these often exceed the tracker error.
7. **Quantum-sensor relevance to EMT** — determining whether OPM/NV can be made
   dynamic-range/bandwidth-suitable for tracking, or remain biomagnetic tools
   (Ch. 30.4) [@budker2007; @barry2020].

> **Takeaway.** The frontier of EMT is mostly *not* new physics — the dipole and
> its inverse are well understood. It is **robustness** (distortion, in-situ
> accuracy), **integration** (fusion, chip-scale sensors), and **trust** (validated
> ML, honest uncertainty) in a regulated clinical setting. The systems that win
> will combine fusion, intelligent compensation, and better sensors — each wrapped
> in the uncertainty quantification this book has insisted on throughout.

---

## Open questions / to verify
- Add primary citations for specific **hybrid optical+EM** and **EM+IMU** clinical/
  research systems with quantified benefit (currently argued from the fusion
  framework, Ch. 21).
- Source recent (2023–2025) results on **TMR sub-pT/biomagnetic** sensing and any
  *tracking*-specific MR demonstrations to update §30.4 (Ch. 14 open question).
- Track standardization efforts for dynamic/distortion assessment protocols
  beyond Hummel [@hummel2005].
- Add active grants/conferences/lab list (project brief) with verifiable sources.

## Sources cited
- [@cavaliere2023; @kindratenko2005] ML/witness compensation. [@davies2021;
  @monteblanco2021] TMR/MR noise & bias. [@budker2007] optical/atomic (SERF).
  [@barry2020] NV-diamond. [@plotkin2003] arrays. [@hummel2005; @yaniv2009]
  SOTA/assessment. Fusion framework from Ch. 21; trilemma from Ch. 12.
