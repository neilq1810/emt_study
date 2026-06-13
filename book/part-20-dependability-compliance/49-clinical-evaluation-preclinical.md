# Chapter 49 — Clinical Evaluation & Preclinical Study Design

> **Status:** DRAFT (awaiting review) · **Part XX — Dependability & Compliance**
> The evidence-generation pipeline the regulatory file (Ch. 48) depends on: how EMT
> navigation accuracy is shown to translate into safe, effective clinical use, through a
> staged progression from bench → phantom → cadaver → animal → human. Implements T2.17;
> builds on characterization (Ch. 33), motion/registration (Ch. 39/41/43), and the
> clinical applications (Ch. 29); feeds the submission (Ch. 48) and post-market follow-up
> (Ch. 44). Citation keys resolve to
> [`../../citations/bibliography.json`](../../citations/bibliography.json).

A regulator does not approve a number; it approves a **claim about patients**. Ch. 48
defined the claim and the file; this chapter is about producing the **evidence** that the
claim is true — and doing so with study designs that are *credible*, because a navigation
study has more ways to fool itself than almost any other. The central methodological
fact is that **sub-millimetre bench accuracy is a surrogate**: it is necessary but not
sufficient for the clinical endpoints (diagnostic yield, procedure success, complication
rate, radiation reduction) the device is actually justified by. The work of clinical
evaluation is to bridge that gap rigorously — and to know, at each stage, exactly which
question the study can and cannot answer.

---

## 49.1 The evidence hierarchy — a V-model of clinical proof

Evidence is built in stages, each de-risking the next and answering a distinct question:

```
 bench / engineering (Ch. 33) ── does the pose meet spec in a controlled rig?
        │
 phantom (anthropomorphic, GT fiducials) ── does target accuracy hold in realistic
        │                                     geometry, with distortion & motion?
 ex-vivo / cadaver ── does registration + workflow work in real anatomy & tissue?
        │
 in-vivo animal (GLP) ── does it hold with physiology — breathing, cardiac motion,
        │                  perfusion, a living, moving target?
 first-in-human (feasibility) ── safe & usable in the real procedure?
        │
 pivotal clinical investigation ── does it meet the CLINICAL endpoint vs a control?
        │
 post-market (PMCF / registries, Ch. 44) ── does the benefit hold at scale, over time?
```

The mapping to Ch. 48 is direct: **bench + preclinical** evidence typically supports a
**510(k)** (substantial equivalence on performance); a **pivotal clinical investigation**
underpins **PMA / De Novo** and the EU **Clinical Evaluation Report**; and **PMCF** keeps
the CER live after launch. Each rung trades **realism against control against
ground-truth availability** — and you can rarely have all three at once, which is the
defining tension of navigation evidence.

## 49.2 Preclinical models for EMT

The preclinical stages exist to buy realism while you can still measure truth cheaply:

| Model | Buys | Costs / limits | EMT-specific use |
|---|---|---|---|
| **Anthropomorphic phantom** | controlled geometry, **embedded CT-visible GT fiducials**, repeatability, programmable distortion (Ch. 42) & respiratory motion (Ch. 41) | not real tissue; idealized | accuracy maps, distortion robustness, detect-and-flag validation, workflow rehearsal |
| **Ex-vivo / cadaver** | true anatomy, true tissue, full instrument interaction | no physiology/perfusion; limited/again-idealized motion; tissue degradation | registration accuracy, fiducial workflow, ergonomics, frame management (Ch. 43) |
| **In-vivo animal (GLP)** | physiology, **respiratory & cardiac motion**, perfusion, bleeding, a living moving target; porcine common for lung/cardiac | ethics/cost; anatomy not human; **truth is now hard to measure** | motion-gating validation (Ch. 41), real-time behavior, safety, therapy delivery |

The progression is deliberately ordered so the **ground-truth problem worsens exactly as
realism improves**: a phantom gives perfect truth and poor realism; a live animal gives
real physiology and makes "where was the tip *really*?" genuinely difficult (the GT
hierarchy of Ch. 33 §33.5 and the moving-target truth problem of Ch. 41). A good program
**front-loads the questions that need truth** (accuracy, distortion) into phantom/cadaver
work, and reserves animal/human studies for the questions that need **physiology**
(motion tracking, safety, clinical effect).

## 49.3 From accuracy to outcome — defining the endpoint

The pivotal methodological choice is the **endpoint**, and it splits into two kinds:
- **Technical / surrogate endpoints** — navigation or **target registration error** at a
  defined target (Ch. 39), time-to-target, **fluoroscopy time / radiation dose** reduction.
  Measurable, mechanistic, close to the engineering — but **not what the patient cares
  about**.
- **Clinical endpoints** — **diagnostic yield** (e.g. the proportion of navigated lung
  lesions yielding a definitive tissue diagnosis), procedure success, **complication
  rate** (pneumothorax, perforation), ablation durability / arrhythmia recurrence.

The credibility of the whole evaluation rests on **not confusing the two**. A device can
have excellent targeting accuracy and mediocre diagnostic yield — because yield also
depends on lesion size, tool-lesion congruence, biopsy technique, and CT-to-body
divergence. The **NAVIGATE** electromagnetic-navigation-bronchoscopy study [@folch2019]
is the canonical example: a large prospective study reporting **diagnostic-yield and
safety** endpoints — i.e. the field's own standard is the *clinical* outcome, with
accuracy as a supporting surrogate, not the headline. The study must therefore either
power on the clinical endpoint, or explicitly and honestly position itself as a technical
study that does **not** establish clinical benefit.

## 49.4 Study design and statistics

A defensible navigation study is built from standard clinical-trial machinery, adapted to
the navigation context, under **Good Clinical Practice (ISO 14155** [@iso14155], EU MDR
Annex XV; **FDA IDE / 21 CFR 812** in the US):
- **Comparator & design.** Single-arm vs comparative; the control is usually **standard
  of care** (e.g. conventional bronchoscopy, fluoroscopy-only guidance). Single-arm
  studies against a **performance goal** are common for 510(k)-class technical claims;
  comparative (often **non-inferiority** or superiority) studies support stronger claims.
- **Hypothesis, powering, sample size.** Pre-specify the endpoint, the hypothesis, the
  margin (for non-inferiority), and **power the study on the clinical endpoint** — a study
  powered only for a surrogate cannot claim clinical benefit.
- **Bias controls.** Randomization where feasible; **blinded, independent core-lab
  adjudication** of endpoints (a bronchoscopist cannot adjudicate their own yield);
  pre-registration; handling of **multiplicity** across endpoints and subgroups.
- **Ground truth for accuracy endpoints in vivo.** The hard one: confirm tip-at-target
  with **CBCT/CT** at the moment of acquisition, accepting that in a breathing patient
  "truth" itself has uncertainty (Ch. 33 §33.5, Ch. 41) — and **never** use the *same*
  registration/imaging that drives the navigation as the truth against which it is scored
  (the circularity trap, §49.5).

## 49.5 Bias and pitfalls specific to navigation studies

Navigation studies fail credibility in characteristic ways; a reviewer looks for each:
- **The surrogate-endpoint trap.** Reporting millimetres and *implying* clinical benefit.
  Accuracy is necessary, not sufficient (§49.3).
- **Ground-truth circularity.** Scoring navigation against the very CT/registration that
  produced it — guaranteeing flattering numbers. Truth must be **independent** of the
  system under test.
- **Learning curve & operator confound.** Results from a single expert operator at a high-
  volume center rarely generalize; the learning curve can dominate early outcomes. Report
  operator experience; consider multi-center, multi-operator designs.
- **Selection bias.** Enrolling easy targets (large, central lesions) inflates yield.
- **CT-to-body divergence / motion.** Pre-procedure CT vs intra-procedure anatomy (Ch. 41)
  is a systematic error that no amount of tracker accuracy removes — and that a phantom
  study will entirely miss.
- **Generalizability of the GT rig.** A truth method validated in a phantom may not hold
  in vivo; state the truth method's own uncertainty and its limits.

The throughline is the same as §49.3: **honesty about what the evidence supports.** A
technical study that openly claims only a technical result is credible; a technical study
dressed as a clinical one is not.

## 49.6 Synthesis: the evidence pipeline as disciplined risk reduction

Clinical evaluation is the staged conversion of engineering confidence into *clinical*
confidence — the outward-facing twin of the risk file (Ch. 45). Each rung answers the
question the next one cannot afford to leave open, the ground-truth problem is
front-loaded onto the stages that can still measure truth, and the endpoint is chosen so
the claim the regulator approves (Ch. 48) is the claim the evidence actually supports.
The pipeline then does not end at approval: **post-market clinical follow-up and
registries** (Ch. 44; MDR PMCF) keep the benefit-risk conclusion live as the device meets
operators, patients, and environments the studies never saw.

> **Engineering takeaway.** Sub-millimetre bench accuracy is a **surrogate**, not the
> clinical claim — so the evaluation must climb a staged ladder (bench → phantom →
> cadaver → animal → human → post-market) in which **realism rises as measurable
> ground-truth falls**, front-loading accuracy/distortion questions onto phantom/cadaver
> work and reserving animal/human studies for physiology, safety, and the **clinical
> endpoint** (diagnostic yield, success, complications — the NAVIGATE posture). Design
> under GCP (ISO 14155 / FDA IDE): pre-specify and **power on the clinical endpoint**, use
> **independent blinded adjudication**, and obtain **ground truth independent of the
> navigation system** to avoid the circularity, surrogate, learning-curve, and
> selection-bias traps. Above all, **claim only what the evidence supports** — that
> discipline is what makes the file (Ch. 48) believable.

---

## Open questions / to verify
- Add a **worked sample-size calculation** for a representative ENB diagnostic-yield
  endpoint (assumed yields, non-inferiority margin, power) as a concrete artifact.
- Build a **phantom-design spec** (CT-visible fiducial lattice, tissue-mimicking,
  programmable distortion/motion) tying Ch. 33 GT, Ch. 41 motion, Ch. 42 metal — a
  candidate Phase-6 reference design.
- Confirm representative **diagnostic-yield / complication figures** and the NAVIGATE
  [@folch2019] endpoint definitions during the citation-verification pass (X1); add a
  second independent clinical reference (conf: med on specific numbers).
- Map **ISO 14155 vs FDA IDE (21 CFR 812)** differences explicitly for a combined
  US/EU program (conf: high on existence, med on procedural detail).

## Sources cited
- [@iso14155] GCP for device clinical investigations (study conduct, ethics, data
  integrity); [@folch2019] NAVIGATE — a large prospective ENB study reporting
  diagnostic-yield and safety endpoints, the worked clinical-endpoint example; [@hummel2005]
  bench accuracy protocol (the surrogate end of the chain). Preclinical truth and motion
  ties are Ch. 33/41/42/43; the regulatory file this evidence feeds is Ch. 48; post-market
  follow-up is Ch. 44.
