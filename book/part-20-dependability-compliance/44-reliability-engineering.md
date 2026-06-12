# Chapter 44 — Reliability Engineering for Electromagnetic Tracking

> **Status:** DEEPENED (awaiting review) · **Part XX — Dependability & Compliance** (opens Part XX)
> Closes the C6 gap. The manuscript has scattered *failure-mode boxes* but no
> quantitative reliability discipline — unacceptable for a safety-critical device. This
> chapter brings FMEA, FIT/MTBF, fault trees, and single-fault analysis to EMT, and
> develops the one reframing that EMT forces: the dangerous failures are **silent and
> partial**, so **detection coverage**, not raw MTBF, is the governing metric. Citation
> keys resolve to [`../../citations/bibliography.json`](../../citations/bibliography.json).

A clinical electromagnetic tracker can misdirect a needle, a catheter, or an ablation,
so it must be engineered not only to be *accurate* (Parts II–IX, XVI) but to be
*dependable* — to keep meeting its essential performance, or to fail safely, over a
service life of mating cycles, flexes, sterilizations, and thermal swings. The book
has so far treated failures qualitatively. This chapter adds the quantitative
reliability toolkit — but, more importantly, it confronts what makes EMT reliability
*different from* most electronics: the system rarely fails by stopping. It fails by
continuing to output a **wrong-but-plausible pose**. That single fact reorders the
whole discipline.

---

## 44.1 What actually fails (the EMT failure landscape)

Field experience, not parts-count theory, names the dominant EMT failures — and they
are mostly **mechanical and at the patient end**, not the exotic physics:

| Class | Modes | Where |
|---|---|---|
| **Connectors & cables** *(the #1 field-failure class)* | mating-cycle wear, flex fatigue, sterilization stress → intermittent opens | catheter/tool connector (T2.8) |
| **Sensor / coil** | fine-wire breakage at the sub-mm coil, solder-joint fracture, potting cracks | tracked tool |
| **Field generator** | coil-insulation breakdown, driver fault, thermal runaway | generator (Ch. 9, 37) |
| **Electronics** | AFE/ADC/compute random faults | SIU/console (Parts V–VI, XVII) |
| **Software** | systematic defects (not random) | pose engine (Ch. 35) |
| **Calibration drift** | thermal/aging accuracy decay | system (Ch. 26.6) |

The lesson the industry learns the hard way: **the connector and cable, not the
magnetometry, dominate returns** — and most of these produce *intermittent* or
*degraded* behaviour, not a clean stop (§44.3).

## 44.2 The quantitative toolkit

- **Failure rate & the bathtub curve.** With a constant hazard $\lambda$, reliability
  $R(t)=e^{-\lambda t}$ and $\text{MTBF}=1/\lambda$; $\text{FIT}=$ failures per
  $10^9$ h. Real components follow a **bathtub**: **infant mortality** (→ screened by
  **burn-in / HALT-HASS**), a flat **useful-life** random region (the constant-$\lambda$
  electronics), and **wear-out** (the connectors/cables/coils of §44.1) — for which the
  remedy is **scheduled replacement / single-use** before the wear-out knee, not a
  better $\lambda$.
- **Reliability prediction.** Parts-count/parts-stress (IEC 61709 / Telcordia, the
  MIL-HDBK-217 lineage) sizes the *electronics*, but **poorly captures** the
  mechanical/connector/sensor failures that dominate EMT — those need **life-test**
  data (mating-cycle, flex, fatigue, sterilization-cycle testing).
- **FMEA / FMECA** [@iec60812]. Enumerate failure modes → effect → **severity × occurrence ×
  detection = RPN** (or a criticality matrix), and act on the high-RPN items. Run both
  a **design** FMEA and a **use/process** FMEA (ties human factors, T1.10).
- **Fault-tree analysis (FTA).** Top-down from a hazard — e.g. *"undetected tool-pose
  error > X mm"* — to the AND/OR combinations of causes, quantified from edge
  probabilities; the complement to bottom-up FMEA.
- **Single-fault condition.** IEC 60601-1 [@iec60601_1] requires safety under **any
  single fault** (Ch. 17). For EMT the binding form is: *no single fault may produce an
  **undetected** dangerous pose error* — which makes redundancy and consistency checks
  (Ch. 13, 27) **single-fault mitigations**, not luxuries.

## 44.3 The reframing: silent, partial failure and detection coverage

In most products, *reliability* (does it work) and *accuracy* (how well) are separate
axes. **In EMT they blur**, and that is the chapter's central point. A degraded sensor,
a drifted calibration, a flaky connector causing micro-dropouts, or an in-patient
distorter (Ch. 42) does **not stop** the tracker — it makes it report a **wrong but
plausible** pose. The hazardous failures are therefore the **silent, partial,
accuracy-degrading** ones, not hard stops.

This inverts the governing metric. The quantity that matters is not MTBF-to-hard-stop
but the **rate of *undetected* accuracy excursions beyond the essential-performance
limit**. Borrowing from functional safety [@iec61508], if a dangerous-failure class
occurs at rate $\lambda$ and the system's **diagnostic coverage** (fraction caught and
flagged) is $\text{DC}$, the **undetected** dangerous rate is
$$
\lambda_\text{dangerous,undetected}=\lambda\,(1-\text{DC}).
\tag{44.1}
$$
The design consequence is decisive: **raising DC beats lowering $\lambda$**. You cannot
make a catheter connector never fail, but you *can* make nearly every failure
**detected and flagged** (Ch. 27 §27.4, Ch. 22, 38, 43). *Worked:* a distortion event
class with a high $\lambda$ but a NIS-alarm $\text{DC}\approx0.99$ yields a 100× lower
*undetected* dangerous rate than its raw rate — so the witness/consistency/NIS
machinery of Ch. 27 is, in reliability terms, the **diagnostic coverage** that
dominates the safety case. **Detect-and-flag is the EMT reliability strategy**, and
"safe-failure fraction" (SFF) is the number to report.

## 44.4 Demonstrating reliability — screening and life testing

Because parts-count cannot predict the dominant modes, EMT reliability is
**demonstrated by test**:
- **Burn-in / HALT-HASS** to screen infant mortality in electronics and generators.
- **Connector mating-cycle** life test to the rated reuse count; **cable flex-life**
  (dynamic bend) testing; **sensor pull/fatigue** testing.
- **Sterilization-cycle** testing (EtO/gamma/autoclave) as an accelerated-aging
  stressor on sensors, potting, and electronics (ties T2.7).
- **Fault-injection** verification that each modeled fault is actually **detected and
  flagged** (Ch. 22 §22.6) — i.e. *measuring* the DC of §44.3 rather than assuming it.

## 44.5 Availability & maintainability

A clinical system cannot cancel a booked procedure, so **availability** (uptime) and
**maintainability** matter alongside reliability: low **MTTR** via field-replaceable
units, spares strategy, and **predictive maintenance** using the system's own
self-health signals — the built-in-test of Ch. 35 (T3.4) and, elegantly, the
**generator drive-impedance monitor of Ch. 27 §27.7** read as a *health* sensor
(a drift in the coil's reflected impedance flags an aging generator or cable before it
fails outright).

> **Engineering takeaway.** EMT reliability is dominated by **connectors, cables, and
> the fine sensor coil** — wear-out items whose answer is life-tested replacement or
> single-use, not a better failure rate — and by **calibration drift**. But the
> defining feature is that EMT **fails silently and partially**: it keeps emitting a
> plausible wrong pose. So the governing metric is not MTBF but the **undetected**
> dangerous-failure rate $\lambda(1-\text{DC})$ — and the highest-leverage reliability
> investment is **diagnostic coverage** (the witness/consistency/NIS detect-and-flag of
> Ch. 27), verified by fault injection. Build FMEA/FTA around *silent* failures, meet
> the single-fault condition with redundancy, screen infant mortality and schedule out
> wear-out, and report safe-failure fraction — because a tracker that fails loud is far
> safer than one that fails quiet.

---

## Open questions / to verify
- Build a worked **EMT FIT/​FMECA budget** allocating a system dangerous-undetected
  target across subsystems, with life-test-derived rates for connectors/cables/coils
  (currently the failure ordering is field-experience qualitative, conf: med — pin to
  a published reliability dataset).
- Add a worked **fault tree** for "undetected tool-pose error > X mm" with quantified
  diagnostic-coverage branches (ties Ch. 27 NIS, Ch. 13 redundancy).
- Source primary **connector mating-cycle / cable flex-life** reliability data for EMT
  catheters (the dominant mode; deep dive deferred to T2.8).
- Cross-map to the **risk file** (T1.9, ISO 14971): every high-RPN FMEA item and
  fault-tree cut set becomes a risk-control requirement.

## Sources cited
- [@iec60812] FMEA/FMECA method (severity × occurrence × detection). [@iec61508]
  functional-safety framework — SIL, **diagnostic coverage / safe-failure fraction**,
  the basis for the silent-failure reframing (§44.3). [@iec60601_1] single-fault
  condition (Ch. 17). The diagnostic-coverage machinery is the detect-and-flag of
  Ch. 27 / Ch. 22 / Ch. 38 / Ch. 43; calibration-drift reliability from Ch. 26.6; the
  risk-file consumer is T1.9.
