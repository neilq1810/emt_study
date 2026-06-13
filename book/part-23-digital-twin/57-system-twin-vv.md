# Chapter 57 — The System Twin & Twin-in-the-Loop V&V

> **Status:** DRAFT (awaiting review) · **Part XXIII — Model-Based Engineering & the Digital Twin**
> The capstone: extend the twin from the device (Ch. 54) and the room (Ch. 56) to the whole
> **navigated system** — registration, motion, sync, and the clinician — propagate it to the
> **target uncertainty the surgeon actually sees**, and use the twin as the engine for
> in-silico verification and regulatory evidence. Closes the "built the tracker, not the
> system" failure. Builds on registration (Ch. 39/40), motion (Ch. 41), cross-modality sync
> (Ch. 10 §10.6), the confidence display (Ch. 46 §46.6), credibility (Ch. 53), and the
> regulatory file (Ch. 48/49). Citation keys resolve to
> [`../../citations/bibliography.json`](../../citations/bibliography.json).

The previous three chapters built a twin of the *tracker* and its *room*. But the regulator
and the patient do not care about the pose of a sensor coil — they care about whether the
instrument reaches the **target** safely, and that number is set by registration, motion,
and the human at least as much as by the tracker (Ch. 29, Ch. 39–43, Ch. 46). The **system
twin** closes the loop by propagating *every* term to the target, and in doing so it makes
the most expensive mistake in the field measurable: optimizing the tracker while the system
error lives somewhere else. This final chapter assembles the twin into the end-to-end model,
shows — quantitatively — where the error actually is, and turns the twin into the engine for
**verification, validation, and in-silico evidence** that the whole Part has been building
toward.

---

## 57.1 From device twin to system twin

The system twin composes the chain the book has built piece by piece, each a transform with
its own uncertainty:
$$
\text{CT/plan} \xrightarrow{\text{registration (Ch.40)}} \text{patient frame}
\xrightarrow{\text{tracker (Ch.54/56)}} \text{pose}
\xrightarrow{\text{frame mgmt (Ch.43)}} \text{target},
$$
with **motion** (Ch. 41) perturbing the patient frame in real time and **cross-modality
sync** (Ch. 10 §10.6) governing whether the transforms are even on the same timeline. The
system twin is the device+environment twin (Ch. 54/56) wrapped in these additional
transforms, propagating a covariance from the field measurement all the way to the
**target-registration error** — the quantity of Ch. 46 §46.6's confidence display. It is the
computational embodiment of the clinical-accuracy chain of Ch. 29 §29.7.

## 57.2 Where the error actually is (computed)

The system twin's first job is to tell the builder **what to optimize**, and the answer
surprises EM-focused teams. Propagating the terms in quadrature (independent contributions),
the Phase-5 system-twin budget (`data/system_twin_budget.json`,
`figures/ch57_system_budget.png`) composes:

| Term | value (mm) | share of target-error **variance** |
|---|---|---|
| Tracker (computed 6-DOF CRLB, §24.6) | 0.086 | **0.21 %** |
| Registration TRE (Ch. 39) | 1.0 | 28.5 % |
| Motion, gated residual (Ch. 41) | 1.5 | 64.2 % |
| Time-sync skew $v\,\Delta t$ (§10.6) | 0.5 | 7.1 % |

giving a **target $\sigma = 1.87$ mm, $T_{95}\approx5.2$ mm** — *twenty times* the tracker
term. The tracker contributes **0.2 %** of the target-error variance; **registration and
motion contribute ~93 %**. This is the "built the tracker, not the system" failure made
exact: **a sub-millimetre tracker does not make a sub-millimetre system**, and a team that
spends its effort shaving the tracker's 0.086 mm is optimizing 0.2 % of the problem. The
system twin redirects the effort to registration, motion-gating, and sync. (The clinical
terms are *representative* inputs (Ch. 39/41/10), labelled illustrative; the **dominance
structure** is the robust result, not the exact millimetres — which is precisely the point a
twin exists to expose.)

## 57.3 The honest boundary: structure, not validated components

The system twin **propagates and exposes**; it does not **supply** the validated
registration and motion-compensation algorithms whose real performance sets those dominant
terms. Those come from Ch. 40/41 and, ultimately, from clinical data the book does not
contain. So the system twin closes gap 5 the same way the others close gaps 1, 2, and 4 —
**as method**: it tells you the target budget, which term dominates, and how much a given
improvement buys, but the validated TRE and motion-residual numbers are the builder's to
measure and the algorithms theirs to validate (Ch. 49). The twin makes the *system*
engineering tractable; it does not do it for you.

## 57.4 Twin-in-the-loop V&V and in-silico evidence

A validated twin is not only a design tool — it is an **evidence engine**, and this is where
Part XXIII rejoins the regulatory file (Ch. 48):
- **In-silico verification.** Run the solver, the detect-and-flag, and the confidence display
  against the twin across thousands of poses, distorters, and motion profiles — coverage no
  bench campaign can match — to verify behaviour and find corner cases (the flag blind spot of
  §33.9/§56.4 was *found this way*).
- **Fault injection.** Inject modeled faults — gain drift, a moved C-arm, **connector
  intermittency** (Ch. 51) — and verify the divergence monitor (Ch. 56) flags them; the one
  gap the twin cannot *close* (the physical connector) it can at least help **test the
  detector for**.
- **In-silico evidence.** Under **ASME V&V 40** [@asme_vv40] and the **FDA CM&S guidance**
  [@fda_cms2023], a credibility-assessed twin can *augment or partially replace* bench/clinical
  testing in a submission — but only within its validated Context of Use (Ch. 53), and the
  required credibility scales with how much the evidence leans on the model. This is the
  regulatory payoff that makes the whole twin worth building.

The recursive caution from Ch. 53 closes the Part: in-silico evidence from an **unvalidated**
system twin is the sixth failure at fleet scale — it would certify, in software, the very
optimism the real OR breaks. Twin-in-the-loop V&V is therefore inseparable from twin
*credibility*.

## 57.5 Synthesis: what the digital twin does and does not close

Part XXIII set out to test whether a model-based methodology could close the gaps that sink
real builds. The honest scorecard:

| Gap (from the failure analysis) | Twin chapter | Closed? |
|---|---|---|
| 1 — Calibration cliff | Ch. 55 (identification) | **as method** — fit twin params; identifiability via Ch. 24 (sim 13: 15 mm → 0.1 mm) |
| 2 — σ_B noise fantasy | Ch. 54 (forward twin) | **structurally** — compose a measured, structured $\mathbf R$ (sim 14) |
| 4 — In-situ distortion | Ch. 56 (environment twin) | **as method** — reconcile + divergence-flag + witness (sim 15) |
| 5 — Built the tracker, not the system | Ch. 57 (system twin) | **partially** — propagate + expose dominance (sim 16); validated components external |
| 3 — Connector intermittency | — | **not closed** — empirical/physical; twin only helps *test the detector* (§57.4) |

The pattern is consistent and worth stating plainly: **the digital twin converts the gaps of
*understanding* (which the rest of the book already prevents) into gaps of *measurement* —
explicit, structured, validatable model inputs the builder must populate.** It supplies the
method, the structure, and the experiment that tells you whether you got it right; it does
not supply the measured values, the proprietary tuned numbers, or a robust connector. That is
the precise line between a definitive *textbook* and a vendor's *engineering program* — and
the digital-twin Part is the book's most complete statement of where that line falls.

> **Engineering takeaway.** The system twin extends the device+environment twin (Ch. 54/56)
> through registration (Ch. 40), motion (Ch. 41), frame management (Ch. 43), and sync
> (§10.6) to the **target** uncertainty the clinician sees (§46.6) — and its first lesson is
> brutal: a Phase-5 budget puts the **tracker at 0.2 % of target-error variance and
> registration+motion at ~93 %** (target $\sigma\approx1.9$ mm vs a 0.086 mm tracker), so a
> sub-mm tracker is *not* a sub-mm system and the effort belongs on registration/motion/sync.
> The twin then becomes an **evidence engine** — in-silico verification (it *found* the
> §56.4 flag blind spot), fault injection (the one way it touches the connector gap), and
> credibility-assessed **in-silico evidence** for the submission (ASME V&V 40 / FDA CM&S,
> Ch. 48) — provided the twin is validated, since an unvalidated system twin is the sixth
> failure at fleet scale. Across the Part, the twin closes gaps 1/2/4 as method and 5
> partially, leaves gap 3 (the physical connector) open, and in every case **converts a gap
> of understanding into an explicit gap of measurement** — method and structure, never the
> measured values themselves. That is exactly as far as a textbook can take a builder, and
> the digital twin takes them all the way there.

---

## Open questions / to verify
- Replace the §57.2 representative registration/motion terms with **measured** TRE and
  gated-motion residuals from a clinical/preclinical study (Ch. 49) — the budget's structure
  is exact; its inputs are the open empirical question.
- Build a **twin-in-the-loop in-silico test harness** (Phase-6) running the solver +
  detect-and-flag + confidence display against the full twin, reporting coverage and found
  corner cases — the operational form of §57.4.
- Draft a **V&V 40 credibility dossier** for one system-twin Context of Use (e.g. in-silico
  augmentation of a bench accuracy test), tying §57.4 to Ch. 48.

## Sources cited
- [@asme_vv40] / [@fda_cms2023] computational-model credibility and in-silico evidence
  (§57.4); [@glaessgen2012] the reconciled system twin. The clinical-accuracy chain is
  Ch. 29 §29.7; registration Ch. 39/40; motion Ch. 41; frame management Ch. 43; sync
  Ch. 10 §10.6; the target-uncertainty display Ch. 46 §46.6; credibility Ch. 53; the
  regulatory/clinical file Ch. 48/49; the connector gap Ch. 51. Computed in
  `simulations/run_all.py` (sim 16).
