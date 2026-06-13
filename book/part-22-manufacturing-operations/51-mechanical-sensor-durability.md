# Chapter 51 — Mechanical & Sensor Durability

> **Status:** DRAFT (awaiting review) · **Part XXII — Manufacturing, Durability & Field Operations**
> The physical survival of the sensor and its connections in a clinical life — sterilization,
> biocompatibility, encapsulation, single-use economics, and the **connector/cable
> intermittency that is the EMT field's #1 failure mode**. Consolidates the durability and
> interconnect-reliability workstreams (T2.C2 = former T2.7+T2.8). Builds on sensor
> construction (Ch. 14), reliability engineering (Ch. 44), and risk (Ch. 45). Citation keys
> resolve to [`../../citations/bibliography.json`](../../citations/bibliography.json).

The most sophisticated pose solver in the book is useless if the sensor cracks during
sterilization, leaches into tissue, or — most commonly — if a hair-thin wire in a flexing
cable opens intermittently mid-procedure. EMT sensors live in a uniquely hostile place: a
**sub-millimetre coil on the tip of a catheter** that must be biocompatible, survive
sterilization, flex thousands of times, and carry microvolt signals (Ch. 16) through a
connector that is mated and unmated repeatedly. This chapter is about that survival, and it
ends where the field's reliability data actually points: **the interconnect, not the
sensor, is what fails.**

---

## 51.1 Sterilization

A patient-contacting sensor must be **sterile**, and the sterilization method must not
destroy it — a real tension for a device containing fine coils, magnetic cores (Ch. 14),
and sometimes electronics:
- **Ethylene oxide (EO)** [@iso11135] — low-temperature, chemical; **electronics- and
  magnetics-compatible**, hence common for reusable EMT sensors and cabled assemblies.
  Requires aeration and validated cycles (SAL 10⁻⁶).
- **Radiation (gamma / E-beam, ISO 11137)** — penetrating, no residuals, good for
  single-use; but **can damage semiconductors and some polymers/adhesives**, so it suits
  passive coil sensors more than active electronics.
- **Steam autoclave** — high temperature + moisture; cheap and common in hospitals but
  **hostile to fine encapsulation, adhesives, and magnetic properties**; many EMT sensors
  are *not* autoclavable, which is a labeling and workflow constraint.

The method is a **design input** (Ch. 48): it constrains materials, encapsulation, and
adhesives, and its **repeated application** (for reusable sensors) is a fatigue/aging load
that §51.3 must survive — a key reason many catheter sensors are **single-use** (§51.4).

## 51.2 Biocompatibility

Anything contacting tissue is evaluated under **ISO 10993** [@iso10993]: a risk-based
selection of biological endpoints (cytotoxicity, sensitization, irritation, and more for
longer/blood contact) driven by **contact type and duration**. For EMT this lands on the
**encapsulation and outer materials** — the sensor's copper, ferrite, and adhesives must
be sealed behind a biocompatible jacket that also survives sterilization (§51.1). Material
selection is thus a three-way constraint: **biocompatible × sterilizable × magnetically/
electrically transparent** (the jacket must not perturb the field it measures, Ch. 4/6).

## 51.3 Encapsulation & mechanical integrity

The encapsulation does quadruple duty: **biocompatible barrier** (§51.2), **sterilization
survival** (§51.1), **mechanical protection** of the coil, and **dimensional stability** of
the sensor geometry — because the coil's effective area and axis *are* the calibration
(Ch. 15 §15.1, Ch. 26). Mechanical threats:
- **Flex fatigue** — a catheter sensor and its lead flex thousands of times; the coil
  winding, the lead-to-coil joint, and the potting are all fatigue sites.
- **Microfractures & delamination** — thermal cycling (sterilization) and handling crack
  potting or delaminate the jacket, opening biocompatibility and signal paths.
- **Dimensional drift** — swelling, creep, or adhesive relaxation that **moves the coil
  geometry** shows up directly as a **calibration shift** (Ch. 26 §26.6) and a pose error
  (Ch. 15 §15.2) — a mechanical fault masquerading as an accuracy fault.

The verification is **life testing under combined stresses** (flex + sterilization-cycle
aging + thermal), an instance of the reliability demonstration of Ch. 44 §44.4 applied to
the physical sensor.

## 51.4 Single-use vs reusable

The choice is simultaneously clinical, economic, and reliability-driven:
- **Single-use** sidesteps re-sterilization aging (§51.1), cross-contamination, and
  per-use degradation, and guarantees a *fresh* sensor each procedure — at the cost of a
  **per-procedure consumable** and the interchangeability requirement (the on-board cal
  coefficient of Ch. 50 §50.2). It moves cost from capital to consumable (Ch. 50 §50.3).
- **Reusable** amortizes a higher-quality sensor over many procedures but must **survive N
  sterilization cycles** with bounded calibration drift, and carries reprocessing-validation
  and tracking burden.
Most catheter-tip EMT sensors are single-use; larger reference/tool sensors are often
reusable. Either way the decision propagates into the BOM, the calibration architecture,
and the durability test plan.

## 51.5 The connector, cable & intermittency — the dominant failure

Field reliability data across EMT and cabled medical sensors points to one culprit far
more than coil failure or electronics: the **interconnect**. The physics is unforgiving —
the sensor delivers **microvolt-level signals** (Ch. 16), so any series resistance change
or partial open in a connector or a flexing conductor is a large *relative* perturbation,
and the failures are typically **intermittent**: a marginal contact or a near-broken strand
that conducts at rest and opens under flex or torque, exactly during use.

Why it dominates and why it is dangerous:
- **Mechanical stress concentrates at the connector and the strain-relief**: mate/unmate
  cycles wear contacts; cable flex fatigues conductors at the boundary to a rigid joint.
- **Intermittency defeats naive testing** — the unit passes end-of-line (Ch. 50) at rest and
  fails only under in-use flex, so production test must include **flex/wiggle and
  contact-resistance-under-load** screening, not just continuity.
- **It presents as a tracking glitch, not an obvious fault** — a dropout or a noise spike
  that the solver may partially absorb, making it a **silent/partial failure** of exactly the
  kind Ch. 44 §44.3 warns about: the detection-coverage and detect-and-flag machinery
  (Ch. 27/44) must catch the resulting signal anomaly and flag it, because the operator
  cannot see a flaky wire.

Design and test responses: **robust strain relief and connector retention**, redundant or
twisted/shielded conductors (Ch. 17), **contact-resistance and intermittency monitoring**
as a built-in self-test (Ch. 44 diagnostic coverage), flex-life qualification (§51.3), and
treating connector wear as a **scheduled-maintenance / consumable** item in field
operations (Ch. 52). The risk file (Ch. 45) must carry intermittent interconnect failure as
a named hazard with the flag as its control.

> **Engineering takeaway.** A sensor must be **biocompatible (ISO 10993) × sterilizable
> (EO/radiation/steam — each constraining materials and aging) × mechanically stable**, and
> because the coil's geometry *is* its calibration, mechanical drift (flex fatigue,
> delamination, creep) shows up as an **accuracy** fault — verified only by combined-stress
> life testing. Single-use sensors dominate at the catheter tip (fresh each case, on-board
> cal), reusables elsewhere (must survive N sterilization cycles). But the load-bearing
> reliability fact is that the **connector and flexing cable — not the coil — are the #1
> EMT field failure**: microvolt signals make any contact/conductor change huge, the
> failures are **intermittent** (pass-at-rest, fail-under-flex), and they manifest as silent
> tracking glitches — so they demand flex/contact-under-load production screening, in-use
> intermittency monitoring with detect-and-flag (Ch. 27/44), robust strain relief, and
> treatment as a maintained/consumable item (Ch. 52).

---

## Open questions / to verify
- Add quantitative **flex-life / mate-cycle** targets and a representative
  contact-resistance-vs-cycles curve (conf: low on specific numbers; the failure ranking is
  well-supported by field experience and is cross-referenced to Ch. 44 §44.1).
- Source a primary **field-reliability/complaint dataset** (or vendor service data)
  confirming the interconnect-dominant failure ranking to replace the experiential claim
  with a cited one (ties Ch. 52 post-market data).
- Specify the **built-in interconnect self-test** (contact-resistance / intermittency
  detection thresholds) as a concrete design tying Ch. 44 diagnostic coverage.

## Sources cited
- [@iso10993] biocompatibility evaluation; [@iso11135] EO sterilization validation
  (radiation ISO 11137 and steam noted by reference). Sensor construction & geometry-as-
  calibration are Ch. 14/15/26; silent/partial failure, detection coverage, and life testing
  are Ch. 44; the interconnect hazard feeds the Ch. 45 risk file; maintenance/consumable
  handling is Ch. 52.
