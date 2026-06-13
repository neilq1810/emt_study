# Chapter 50 — Manufacturing & Production

> **Status:** DRAFT (awaiting review) · **Part XXII — Manufacturing, Durability & Field Operations**
> How an EMT design becomes thousands of identical, in-spec units at a cost that closes the
> business case. Consolidates the production-test, factory-calibration-at-scale, and
> design-to-cost workstreams (T2.C1 = former T2.5+T2.6+T2.13). Builds on the design-side
> tolerance/noise analysis (Ch. 15), the calibration physics (Ch. 26), and the quality
> system / design transfer (Ch. 48). Citation keys resolve to
> [`../../citations/bibliography.json`](../../citations/bibliography.json).

A tracker that works once on the bench is a demonstration; a *product* is ten thousand
trackers that each meet spec, calibrate in seconds, and cost less to build than they sell
for. This chapter is the bridge from **design transfer** (Ch. 48 §48.4) to **volume
production**: the end-of-line test that screens every unit, the factory calibration that
makes units interchangeable, and the cost engineering that decides whether the design is
viable at all. The recurring theme is that **manufacturing is where unit-to-unit
variability (Ch. 15) is detected, corrected, or rejected** — calibration removes what it
can, production test catches the rest, and cost sets how much of either you can afford.

---

## 50.1 End-of-line production test

Every unit shipped must be **screened**, because the tolerance analysis of Ch. 15 says
units vary and the safety case (Ch. 45/48) assumes each shipped device meets spec. A
production-test sequence for an EMT system layers cheap, fast tests first:

| Stage | Test | Catches |
|---|---|---|
| **In-circuit / functional** | power-up, channel continuity, ADC/front-end functional (Ch. 16/18) | assembly defects, dead channels, solder faults |
| **Parametric** | per-channel gain/offset/noise floor (Ch. 15 §15.3), generator drive amplitude/phase (Ch. 9) | out-of-tolerance components, marginal parts |
| **Calibration** | sensor/generator/system cal (§50.2) | the systematic unit-to-unit variation |
| **Accuracy verification** | pose error at a fixture of known poses (Ch. 26 §26.5, Ch. 33) | residual error after cal; the go/no-go gate |
| **Burn-in / ESS** | optional environmental stress screening | infant-mortality / latent defects (Ch. 44) |

The accuracy-verification gate is the one that matters: a **golden fixture** holding a
reference sensor at known poses, against which the unit's reported pose is compared, with
**acceptance limits derived from the spec with measurement-uncertainty guard-banding**
(the rig must be ~3–5× better than the unit, Ch. 33 §33.5). Test results feed
**statistical process control** — tracking $C_{pk}$, yield, and drift of each parameter so
a process going out of control is caught *before* it makes scrap. First-pass yield is a
primary economic lever (§50.3): a test that rejects 10 % of units doubles effective cost
if those units cannot be reworked.

## 50.2 Factory calibration at scale, golden units & cal-transfer

Ch. 26 established *what* calibration does physically; production must do it **fast,
repeatably, and traceably** on every unit. Three industrial problems arise:

- **Throughput.** A full volumetric field map (Ch. 26 §26.4) takes too long per unit at
  volume. The standard resolution is to **characterize the design once** (a slow, dense
  reference mapping) and **per-unit calibrate only the parameters that actually vary** —
  typically per-channel gain/offset/phase and a low-order geometric correction — against a
  **fast fixture**. The expensive physics is amortized across the production run; the
  per-unit step is reduced to the few degrees of freedom Ch. 15's tolerance analysis says
  are unit-specific.
- **Golden units & cal-transfer.** Production needs a **transfer standard**: a small set of
  **golden units** (exhaustively characterized, themselves traceable) that calibrate the
  *fixtures* on each line, so a unit calibrated in Plant A behaves identically to one from
  Plant B. This is a **metrological-traceability chain** (ISO/IEC 17025 [@iso17025]): the
  unit's calibration traces through the fixture, through the golden unit, to a national
  length/field standard, with an **uncertainty budget at each link**. Without it,
  "calibrated" means nothing comparable across lines or time.
- **Interchangeability.** Single-use or field-replaceable sensors (Ch. 51) must work
  against *any* system without per-pairing calibration, which forces the **sensor's own
  parameters onto the sensor** (a calibration coefficient stored in the connector/EEPROM)
  so the system reads them at plug-in — the manufacturing counterpart of the plug-and-play
  clinical workflow.

Recalibration policy over the unit's life (drift, §50-to-Ch.26 §26.6) belongs to field
operations (Ch. 52), but the **traceability chain established at the factory is what makes
a field recalibration meaningful**.

## 50.3 Cost, BOM & design-to-cost

A design that cannot be built profitably does not ship. Cost engineering is therefore a
**design input** (Ch. 48 §48.4), not an afterthought:

- **BOM (bill of materials)** dominates recurring cost: the field-generator power
  electronics and precision coils (Ch. 9), the multi-channel analog front-end + ADCs
  (Ch. 16/18), the compute (Ch. 36), the sensors (Ch. 13/14), and the cabling/connectors
  (Ch. 51 — often underestimated and a top failure item). **Single-use sensors** move cost
  from capital to per-procedure consumable, changing the whole business model.
- **Design-to-cost** trades performance against BOM explicitly: channel count vs accuracy
  (more receive channels lower PDOP, Ch. 24 §24.3, but cost front-ends); generator moment
  vs power/thermal/cost (Ch. 9, T2.21); sensor technology (wound coils vs solid-state MR,
  Ch. 14) vs unit cost and yield. Each is a point on the accuracy-vs-cost curve the product
  must hit.
- **NRE vs recurring.** Calibration infrastructure (§50.2), test fixtures (§50.1), and
  qualification (Ch. 48) are **non-recurring** costs amortized over volume — which is why
  low-volume medical devices carry high unit cost, and why **design-for-test** and
  **design-for-calibration** (minimizing per-unit time) pay back directly in margin.

> **Engineering takeaway.** Production is where the unit-to-unit variability of Ch. 15 is
> screened and corrected at scale: an **end-of-line test** (functional → parametric →
> calibration → **accuracy-verification go/no-go** against a guard-banded golden fixture,
> under SPC/$C_{pk}$) ensures every shipped unit meets the spec the safety case assumes;
> **factory calibration** amortizes the expensive volumetric physics into a fast per-unit
> step and ties every unit to a **traceable golden-unit chain** (ISO/IEC 17025) so units are
> interchangeable across lines and time — with single-use sensors carrying their cal
> coefficients on-board. And **design-to-cost** (BOM, channel-count-vs-PDOP, moment-vs-power,
> sensor technology, NRE-vs-recurring) decides whether the design is viable at all, making
> cost and testability **design inputs**, not afterthoughts.

---

## Open questions / to verify
- Add a **worked first-pass-yield → effective-unit-cost** model (test reject rate, rework
  cost, scrap) as a concrete artifact tying §50.1/§50.3.
- Quantify a **per-unit calibration-time budget** vs the parameters-that-vary (Ch. 15) for a
  representative design — how few DOF can a fast fixture calibrate and still hit spec?
- Confirm representative **BOM cost splits** for a clinical EMT system once vendor/teardown
  facts are available (conf: low on absolute numbers; the structure is robust).

## Sources cited
- [@iso17025] calibration-laboratory competence & metrological traceability — the golden-
  unit/cal-transfer chain of §50.2. Design-side variability is Ch. 15; calibration physics
  Ch. 26; design transfer & cost-as-design-input Ch. 48; sensor/cable cost & durability
  Ch. 51; field recalibration Ch. 52.
