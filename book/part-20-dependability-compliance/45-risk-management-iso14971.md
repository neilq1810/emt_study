# Chapter 45 — Risk Management (ISO 14971) for Electromagnetic Tracking

> **Status:** DEEPENED (awaiting review) · **Part XX — Dependability & Compliance**
> Closes the T1.9 gap and provides the **integrating safety spine** the book lacked:
> the framework that consumes the FMEA/fault-tree of Ch. 44, the error budgets of
> Ch. 25, the essential-performance posture of Ch. 17, the software hazards of Ch. 35,
> and the use-errors of Ch. 46, and ties them into traceable hazard→control→evidence
> links. Citation keys resolve to [`../../citations/bibliography.json`](../../citations/bibliography.json).

The book covers electrical safety (IEC 60601, Ch. 17), software lifecycle (IEC 62304,
Ch. 35), and reliability (Ch. 44), but those are *inputs* to a discipline it has not
yet stated: **risk management to ISO 14971** [@iso14971], the standard that every
regulator (FDA, EU MDR) requires and that organises all device safety around a single
question — *what is the probability and severity of **harm to the patient**, and have
we reduced it acceptably?* This chapter applies that framework to EMT, develops the
EMT-specific hazard analysis, shows why **detection coverage is the highest-leverage
risk control**, and explains why you **cannot label your way out** of a design hazard.

---

## 45.1 The core definitions — harm, not failure

ISO 14971 is built on three terms whose distinction is the whole discipline:
- **Hazard** — a potential *source* of harm (e.g. an inaccurate pose).
- **Hazardous situation** — a circumstance that *exposes* the patient (the
  interventionalist relies on that inaccurate pose to place a needle).
- **Harm** — actual injury (a punctured vessel, a pneumothorax, an ablation of wrong
  tissue).

$$
\text{Risk}=\text{probability of harm}\times\text{severity of harm}.
$$
The decisive shift from the rest of the book: risk is about **harm to the patient/user**,
not "the device failed." A pose error is only a hazard; it becomes harm through a
**sequence of events** — error → undetected → clinician trusts it → wrong therapy →
injury — and *breaking that sequence at any link* (most powerfully at "undetected")
reduces risk. The ISO 14971 process wraps this: plan → identify hazards → estimate →
evaluate acceptability → **control** → residual-risk and **benefit-risk** evaluation →
**production & post-production** feedback (a loop, not a one-time analysis).

## 45.2 EMT hazard analysis — the sequences to harm

The EMT-specific hazards and the event sequences that turn each into harm — every one
traceable to an earlier chapter:

| Hazard | Source | Sequence to harm (broken by…) |
|---|---|---|
| **Undetected pose error** *(master hazard)* | distortion (Ch. 6/42), noise (Ch. 24), registration (Ch. 39), motion (Ch. 41), drift (Ch. 26), frame confusion (Ch. 43), connector intermittency (Ch. 44) | error → **undetected** → trusted → wrong therapy → injury *(detect-and-flag, Ch. 27)* |
| **Loss of tracking** | dropout, reference loss (Ch. 38) | guidance lost → act on stale display → injury *(flag-and-hold, Ch. 43)* |
| **Latency / lag** | pipeline delay (Ch. 12) | act on old pose during motion → injury *(low latency + prediction, Ch. 41)* |
| **EMI to active implant** | generator field near CIED (Ch. 42) | oversensing → pacing inhibition / shock *(immunity test, Ch. 17/42)* |
| **Patient heating / leakage** | biased-sensor power, faults (Ch. 17/37) | burn / shock *(isolation, single-fault, Ch. 17/44)* |
| **Mis-registration** (wrong side/patient/fiducials) | registration (Ch. 39–40) | wrong-site therapy *(verification, redundant fiducials, workflow)* |
| **Over-trust / automation bias** | use-related (Ch. 46) | clinician over-relies even on a correct device → injury *(uncertainty display, training, Ch. 46)* |

The **master hazard** is the *undetected* pose error: every error source in the book
funnels into it, and its danger is that it is **silent** (Ch. 44 §44.3). That is why
the analysis keeps returning to detection.

## 45.3 The risk-control hierarchy — and why labeling is last

ISO 14971 mandates a **hierarchy** of controls, applied in order:
1. **Inherently safe design** (eliminate the hazard) — higher moment/SNR (Ch. 8),
   pulsed-DC conductive-distortion rejection (Ch. 27.6), a **metal-free instrument
   tip** (Ch. 42), galvanic isolation (Ch. 17).
2. **Protective measures** (reduce probability/exposure) — **detect-and-flag**
   (Ch. 27, the master control), redundancy/consistency (Ch. 13), essential-performance
   monitoring (Ch. 17.3), single-fault tolerance (Ch. 44), reference-loss handling
   (Ch. 38/43).
3. **Information for safety** (labeling, IFU, training) — "keep metal out," distortion
   warnings, "verify before acting."

The principle the book must state plainly: **information for safety is the *weakest*
control, and may not substitute for a feasible design or protective measure.** You
**cannot label your way out** of a distortion hazard — a warning in the IFU does not
reduce risk if a detect-and-flag control or a metal-free tip is achievable. This
directly rebukes the common temptation to "just warn the user" about EMT distortion.

## 45.4 Detection coverage is the highest-leverage control

Joining Ch. 44 eq. 44.1 to the risk equation makes the central EMT risk-management
result explicit. A control that raises **diagnostic coverage** DC converts an
*undetected* hazard (high risk, because the harm sequence completes silently) into a
*detected* one (low risk, because the sequence is broken at the "undetected" link):
$$
\text{Risk}_\text{undetected}\ \propto\ P(\text{error})\,(1-\text{DC})\,P(\text{harm}\mid\text{acted on})\times\text{severity}.
$$
Because $P(\text{error})$ is hard to drive to zero in a hostile clinical field (Ch. 42)
but DC can be pushed near 1 by witness/consistency/NIS monitoring (Ch. 27),
**detection is the single most effective risk control in EMT** — it attacks the
*probability of harm* term directly. This unifies three threads of the book —
detect-and-flag (Ch. 27), diagnostic coverage (Ch. 44), and ISO 14971 risk control —
into one statement: *the witness/consistency machinery is not an accuracy feature, it
is the primary safety control.*

## 45.5 Acceptability, benefit–risk, and the radiation dividend

After controls, **residual risk** is evaluated against the plan's acceptability
criteria (reduced "as far as possible," AFAP, under MDR), then weighed in a
**benefit–risk** analysis. EMT's benefits are real and quantifiable: line-of-sight-free
localization that reaches targets otherwise inaccessible (Ch. 29), and — importantly —
**reduced fluoroscopy**, i.e. a *reduction* in ionizing-radiation harm to patient and
staff (Ch. 1, 29). That radiation dividend is itself a **risk reduction**, and it
legitimately offsets residual tracking risk in the benefit–risk balance: an EP or ENB
procedure guided by EMT may carry a small residual pose-error risk while removing a
larger, certain radiation risk. Residual risks that remain are **disclosed** (the IFU,
the consent), the lowest tier of §45.3.

## 45.6 The risk-management file as the integrating document

The **Risk Management File (RMF)** is where the whole book's safety content converges
into traceable links — **hazard → estimated risk → control → verification evidence →
residual risk**:
- FMEA/FMECA and fault trees (Ch. 44) supply hazards and probabilities;
- error budgets (Ch. 25) and CRLB (Ch. 24) quantify the pose-error hazard;
- essential performance in pose terms (Ch. 17.3) defines the harm threshold;
- software hazards (Ch. 35 / IEC 62304) and use-errors (Ch. 46 / IEC 62366) feed in;
- detection coverage (Ch. 44) and detect-and-flag (Ch. 27) are the controls;
- post-market data (T2.11) closes the production/post-production loop.

**Worked example.** Hazard: *undetected position error > 3 mm during ENB → biopsy of
wrong tissue / pneumothorax.* Severity: **serious**. Pre-control risk
$\propto P(\text{err}>3\text{mm})\times P(\text{undetected})\times P(\text{harm})$.
Apply the NIS/witness **detect-and-flag** control (Ch. 27): $P(\text{undetected})$ drops
by ~$(1-\text{DC})$ (Ch. 44), cutting the risk by the same factor; add
information-for-safety (verify against intermittent fluoro) as the backup tier. The
residual risk is judged **acceptable** against the benefit (reaching peripheral lesions
otherwise unreachable, at reduced radiation, Ch. 29 [@folch2019]). The RMF records each
link with its verification evidence — that traceability, not any single number, is what
the regulator and the standard require.

> **Engineering takeaway.** Risk management to ISO 14971 is the **spine** that ties
> the book's safety content together: it reasons about **harm to the patient**, not
> device failure, through **hazard → hazardous situation → harm** sequences. Apply the
> control **hierarchy** — inherently safe design first, protective measures second,
> labeling *last* (you cannot warn your way out of a hazard). In EMT the master hazard
> is the **undetected** pose error, and the highest-leverage control is **diagnostic
> coverage** (detect-and-flag, Ch. 27/44), which breaks the harm sequence at its silent
> link. Weigh residual risk against EMT's real benefits — including the **radiation
> dividend** — and record every hazard→control→evidence link in the risk-management
> file, the document that integrates Parts V, IX, XVII, and XX.

---

## Open questions / to verify
- Build a representative **EMT hazard table / RMF skeleton** (hazard → sequence →
  control → verification → residual) covering §45.2, with quantified pre/post-control
  risk using the Ch. 44 DC values (currently the worked example is illustrative).
- Add **ISO/TR 24971** (guidance on applying 14971) and the **EU MDR GSPR / benefit-risk**
  references to firm up §45.5 (T2.16 regulatory).
- Cross-reference **IEC 62366** use-related hazards (Ch. 46) and **IEC 60601-1 §**
  essential-performance hazards explicitly into the hazard table.
- Quantify the **radiation-dividend** benefit (typical fluoroscopy-time/dose reduction
  with EMT guidance) with primary sources to strengthen the benefit-risk argument.

## Sources cited
- [@iso14971] the risk-management standard (harm-based risk, control hierarchy,
  benefit-risk, RMF). Inputs: FMEA/FTA and diagnostic coverage [@iec60812; @iec61508;
  Ch. 44]; single-fault/essential performance [@iec60601_1; Ch. 17]; software hazards
  [@iec62304; Ch. 35]; the detect-and-flag control (Ch. 27); benefit evidence
  [@folch2019; Ch. 29]; use-errors (Ch. 46, IEC 62366).
