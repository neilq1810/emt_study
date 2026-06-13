# Chapter 52 — Deployment & Lifecycle Operations

> **Status:** DRAFT (awaiting review) · **Part XXII — Manufacturing, Durability & Field Operations**
> The device after it leaves the factory: installation and per-room characterization, field
> QA and drift management, post-market surveillance and recalls, and supply-chain/
> obsolescence over a multi-year service life. Consolidates the deployment, service,
> post-market, and supply-chain workstreams (T2.C3 = former T2.9+T2.10+T2.11+T2.12). Builds
> on distortion characterization (Ch. 27/33), recalibration (Ch. 26 §26.6), reliability/
> availability (Ch. 44), and the regulatory file (Ch. 48). Citation keys resolve to
> [`../../citations/bibliography.json`](../../citations/bibliography.json).

A medical EMT system is sold once and *operated* for a decade — in a specific room, by
specific staff, against a specific spec, while components go obsolete and the field learns
how it really fails. The factory (Ch. 50) ships an in-spec unit; this chapter is everything
that keeps it in spec **in the room it actually lives in**, and that closes the regulatory
loop (Ch. 48) by feeding real-world evidence back into the design. The unifying idea: a
tracker's accuracy is a **site-and-time-dependent property**, so it must be **established at
install, verified routinely, and surveilled across the fleet** — not assumed from the data
sheet.

---

## 52.1 Installation & per-room environmental characterization

Because distortion is set by the **room** (Ch. 6/27) and accuracy degrades toward the volume
edge (Ch. 24), the same unit performs differently in different suites. Commissioning is
therefore a **site survey**, not a power-on:
- **Survey the room's conductive/ferromagnetic structures** — table, C-arm, lights, ferrous
  building steel — and the **moving** ones (Ch. 29 §29.9), which set the *dynamic* distortion
  floor that no static map removes.
- **Place the generator** to maximize the well-conditioned volume over the clinical workspace
  (under-table/planar where possible, Ch. 9/T2.1) and away from the worst metal.
- **Per-room baseline characterization** — an accuracy/distortion map of the *installed*
  configuration (the Ch. 33 protocol run on site), which becomes the **reference** against
  which later field QA detects drift, and which calibrates the detect-and-flag thresholds
  (Ch. 27) to this room.
This baseline is the install deliverable that makes "the system meets spec **here**"
a verified statement rather than a factory inheritance.

## 52.2 Service, field QA & drift management

Between cases and over years, the system must be shown to *still* meet spec:
- **Daily/periodic verification** — a quick **known-fixture check** (a reference sensor at a
  known pose) that an operator runs to confirm accuracy before clinical use, with pass/fail
  against the §52.1 baseline. This is the field analogue of the production accuracy gate
  (Ch. 50 §50.1) and the practical face of Ch. 26 §26.5 verification.
- **Drift management** — sensors and generators drift with thermal cycling, aging, and
  sterilization (Ch. 15 §15.5, Ch. 26 §26.6, Ch. 51); field QA detects it, and the **service
  procedure** (recalibration, sensor/cable replacement) restores it. Connector/cable wear
  (Ch. 51 §51.5) is a **scheduled, expected** service item, not a surprise failure.
- **Availability** — uptime, mean-time-to-repair, spares, and remote diagnostics (Ch. 44
  §44.5) determine whether the system is *usable* when the case is booked; field service is
  where designed reliability becomes delivered availability.

## 52.3 Post-market surveillance, vigilance & recalls

The regulatory obligation does not end at clearance (Ch. 48); it **inverts** into a duty to
watch the fielded fleet:
- **Complaint handling & adverse-event reporting** — under **US 21 CFR 803 (MDR)** [@cfr803]
  and **EU MDR vigilance** [@eu_mdr], serious events are reported within defined timelines;
  complaints feed the quality system (Ch. 48).
- **CAPA** — corrective and preventive action: investigate root cause, correct, and prevent
  recurrence; an interconnect-intermittency trend (Ch. 51 §51.5), for instance, becomes a
  CAPA that may change a connector design or a service interval.
- **Recalls / field safety corrective actions** — when a fielded issue creates unacceptable
  risk, the manufacturer issues a correction or removal; **traceability (UDI, Ch. 48)** makes
  it possible to find the affected units.
- **PMS/PMCF** — proactive **post-market surveillance** and, in the EU, **post-market clinical
  follow-up** (Ch. 49) keep the benefit-risk and clinical-evaluation conclusions live with
  real-world data. This is the loop that turns field experience into the **cited** failure
  data the durability chapter (Ch. 51) currently lacks.

The structural point: **post-market data is the highest-fidelity reliability and clinical
evidence that exists** — far larger N than any bench or trial — and the lifecycle system
exists to capture it and route it back into design (Ch. 48 loop).

## 52.4 Supply chain & component obsolescence

A device with a 10-year service life is built from components with far shorter market lives,
so **obsolescence management** is a sustaining-engineering discipline:
- **Long lifecycle vs short component life** — ADCs, FPGAs/SoCs (Ch. 36), op-amps, and
  connectors go end-of-life; the manufacturer must **last-time-buy**, **second-source**, or
  **redesign** — and any electrically-different replacement may perturb the noise/timing
  budget (Ch. 16/18) and **require re-qualification and re-validation** (Ch. 48) of the
  affected function.
- **Second-sourcing & qualification** — critical/single-source parts (precision references,
  the sensor itself) are supply risks; qualifying a second source is a controlled design
  change.
- **Counterfeit & quality risk** — broker-sourced obsolete parts carry authenticity risk that
  the QMS (Ch. 48) and incoming inspection must control.
A component change is therefore never "just a swap": it re-enters the design-control loop,
which is precisely why obsolescence is a *lifecycle* concern owned alongside service and
surveillance.

> **Engineering takeaway.** A tracker's accuracy is **site- and time-dependent**, so the
> lifecycle system exists to keep "meets spec" true in the room and over the years:
> **install** with a site survey and a **per-room baseline characterization** (Ch. 33) that
> sets the detect-and-flag thresholds and the QA reference; **operate** with routine
> known-fixture verification and **scheduled drift/connector service** (Ch. 26/51) for
> delivered availability (Ch. 44); **surveil** the fleet through complaints, MDR/vigilance
> reporting (21 CFR 803 / EU MDR), CAPA, recalls, and PMS/PMCF — the loop that feeds the
> highest-N reliability and clinical evidence back into the design (Ch. 48); and **sustain**
> it against component obsolescence, where any second-source or redesign re-enters design
> controls and re-qualification. Deployment is not the end of engineering — it is where the
> design meets reality and the evidence comes home.

---

## Open questions / to verify
- Specify a concrete **daily-verification procedure + acceptance limits** (fixture, poses,
  pass/fail vs the install baseline) as a field-QA artifact tying Ch. 26 §26.5 / Ch. 33.
- Add a **site-survey checklist** (conductive/ferrous inventory, generator placement,
  baseline-map acceptance) for §52.1.
- Source representative **post-market failure/complaint distributions** for EMT systems to
  quantify §52.3 and retire the experiential interconnect-ranking claim (Ch. 51 §51.5).
- Add an **obsolescence-driven re-qualification** worked example (e.g. ADC second-source →
  re-verify noise/ENOB budget, Ch. 18) for §52.4.

## Sources cited
- [@cfr803] US Medical Device Reporting; [@eu_mdr] EU MDR vigilance/PMS/PMCF. Per-room
  distortion/characterization is Ch. 6/27/33; recalibration & drift Ch. 26 §26.6 and Ch. 15
  §15.5; availability/maintainability Ch. 44 §44.5; the design-control loop this surveillance
  feeds is Ch. 48; connector/cable service derives from Ch. 51 §51.5; PMCF ties Ch. 49.
