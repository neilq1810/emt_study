# Chapter 48 — Regulatory Pathways & Quality Systems

> **Status:** DRAFT (awaiting review) · **Part XX — Dependability & Compliance**
> The regulatory/quality spine of the book: how an EMT-enabled device actually
> reaches market, and the quality system + design controls + V&V that produce the
> evidence. Consolidates the regulatory-pathways (T2.16) and V&V/quality-system
> (T2.15) workstreams. Builds on risk management (Ch. 45), human factors (Ch. 46),
> software lifecycle & EMC (Ch. 17/35), and feeds clinical evaluation (Ch. 49) and
> post-market surveillance (Ch. 44, T2.C3). Citation keys resolve to
> [`../../citations/bibliography.json`](../../citations/bibliography.json).

Every prior chapter built the *technology*; this one is about the *evidence* and the
*permission*. An EMT subsystem almost never ships on its own — it is a **component of a
regulated medical device** (a navigation or mapping system), and that device cannot be
sold until a regulator is satisfied it is safe and effective for a stated use. The two
disciplines that get it there are **regulatory strategy** (which pathway, in which
jurisdiction, against what claims) and the **quality system** (the design-controls and
V&V machinery that generates the proof). They are not paperwork bolted on at the end:
the intended use chosen here sets the accuracy spec the CRLB chapters chase (Ch. 24/31),
the risk file (Ch. 45) and usability validation (Ch. 46) are submission deliverables,
and the characterization protocols (Ch. 33) *are* the verification evidence. This
chapter ties those threads into the path to market.

---

## 48.1 What is actually being cleared — intended use and classification

The single most consequential document is the **intended use / indications for use**: a
sentence naming the patient population, the clinical purpose, the anatomy, and the
operator. Everything downstream — risk class, required accuracy, clinical evidence,
labeling — flows from it. "Real-time electromagnetic localization of a compatible
catheter tip to aid navigation during bronchoscopy" and "…to position an ablation
catheter for therapy delivery" are different claims with different risk and different
evidence burdens, even on identical hardware.

**What is the device?** Usually the **navigation system** (generator + sensors +
solver + display + the compatible tools), not "the EM tracker." The tracker's pose
error is one input to the system's clinical accuracy; the regulator cares about the
**target accuracy delivered to the clinician** (the propagated chain of Ch. 39/43/46,
not the bench pose CRLB alone).

**Risk classification** sets the pathway:
- **US (FDA):** risk-based **Class I / II / III**. Most surgical/navigation systems are
  **Class II** (special controls, general controls); life-sustaining or high-risk
  therapy-delivery systems can be **Class III**.
- **EU (MDR 2017/745):** rule-based **Class I / IIa / IIb / III** [@eu_mdr]. Active
  devices for diagnosis/monitoring and most navigation software fall under the active-
  device rules; **software that drives or informs a clinical decision is classified by
  Rule 11**, which pushes most navigation software to **IIa or IIb**.

The classification is a *consequence* of the intended use, so claim discipline is the
first lever of regulatory cost: a broader claim (therapy guidance, autonomous action)
raises the class, the evidence, and the timeline.

## 48.2 US pathways — 510(k), De Novo, PMA

```
                       Is there a legally marketed PREDICATE
                       of the same type and intended use?
                                 │
                ┌────────────────┴─────────────────┐
              yes                                   no
                │                                    │
        ┌───────┴────────┐                ┌──────────┴───────────┐
   Class II:                          novel, low/moderate     Class III /
   510(k) — substantial               risk: De Novo           life-sustaining:
   equivalence [@fda_510k]            [@fda_denovo]            PMA
```

- **510(k) (premarket notification).** Demonstrate **substantial equivalence (SE)** to a
  legally marketed **predicate**: same intended use, and the same technological
  characteristics *or* different ones that do not raise new questions of safety/
  effectiveness, supported by performance data [@fda_510k]. This is the dominant route
  for navigation systems: an electromagnetic bronchoscopy-navigation device clears by SE
  to an existing navigation predicate, with **bench accuracy, EMC, electrical-safety,
  software, and usability** data closing the gap. Variants: **Traditional**, **Special**
  (for the manufacturer's own modification), and **Abbreviated** (leveraging guidance/
  standards).
- **De Novo.** For a **novel** device of **low–moderate risk with no predicate**
  [@fda_denovo] (statute: FD&C Act §513(f)(2)). It creates a **new device type and its
  special controls**, after which the device itself becomes a predicate others can cite —
  the route a genuinely new tracking modality (e.g. a first-of-kind sensing principle)
  takes instead of being forced to PMA by the lack of a predicate.
- **PMA (premarket approval).** The most stringent route, for **Class III**: independent
  demonstration of safety and effectiveness, typically including a **pivotal clinical
  trial**. Reserved for the highest-risk therapy-delivery contexts.

**Predicate strategy is the core of US planning:** identify the predicate early, map your
device's technological differences to test evidence, and keep the claim within the SE
envelope — or accept De Novo/PMA and budget the clinical evidence (Ch. 49).

## 48.3 EU pathway — MDR, GSPR, and conformity assessment

The EU MDR [@eu_mdr] replaces "show equivalence to a predicate" with "**demonstrate
conformity to the General Safety and Performance Requirements (GSPR, Annex I)**." The
spine:
- **GSPR (Annex I).** A checklist of safety/performance requirements; the manufacturer
  produces a **GSPR matrix** mapping each applicable requirement to the **harmonized
  standard** and the **evidence** that satisfies it (the same 60601/62304/62366/14971
  evidence — §48.5).
- **Classification (Annex VIII).** Rule-based; **Rule 11** governs decision-support
  software and typically lands navigation software in **IIa/IIb**.
- **Conformity assessment (Annexes IX–XI).** For IIa and above, a **Notified Body**
  audits the **QMS (ISO 13485)** and reviews the **technical documentation** (Annexes
  II/III); success yields the **CE mark**.
- **Clinical evaluation (Annex XIV).** A continuous process producing the **Clinical
  Evaluation Report (CER)**, fed by literature, equivalence, and/or clinical
  investigation — the EU analogue of the clinical-evidence burden (Ch. 49), with
  **post-market clinical follow-up (PMCF)** continuing after launch.
- **Traceability infrastructure:** **UDI** device identification and **EUDAMED**
  registration.

The practical contrast: the US 510(k) leans on a **predicate**; the EU MDR leans on a
**requirements-to-evidence matrix** and an independent QMS+dossier audit. The same
engineering evidence serves both, organized differently.

## 48.4 The quality system and design controls

Neither pathway accepts evidence produced *ad hoc*; it must come from a controlled
process. That is the **Quality Management System**:
- **ISO 13485:2016** [@iso13485] — the international device QMS (mandatory for CE, via the
  Notified Body audit).
- **US 21 CFR Part 820** [@cfr820] — the Quality System Regulation; the **QMSR final rule
  (2024)** incorporates ISO 13485 by reference, **effective 2 Feb 2026**, largely
  *harmonizing* the two so one QMS serves both jurisdictions.

The heart of both — and the part an EMT engineer lives in — is **design controls**
(21 CFR 820.30 / ISO 13485 §7.3), the V&V V-model of `figures/ch48_design_controls.png`:

```
 User needs ─▶ Design INPUTS ─▶ Design OUTPUTS ─▶ Design TRANSFER ─▶ production
   (intended    (requirements:     (specs, drawings,    (to manufacturing)
    use)          accuracy, EMC,     code, procedures)
                  safety, usability)        │
                          │                 │
                   VALIDATION ◀──────── VERIFICATION
              "right thing?"            "thing right?"
              (meets user needs)        (outputs meet inputs)
                          │
                  Design REVIEWs at each gate;  everything captured in the
                  Design History File (DHF) with a traceability matrix
```

Every requirement is **traceable** forward to a design output and a test, and the whole
record is the **Design History File (DHF)**. For EMT this is where the book's content
becomes auditable artifacts: the accuracy spec (Ch. 31) is a design input; the solver and
calibration (Ch. 23/26) are design outputs; the characterization protocol (Ch. 33) is a
verification record; the usability study (Ch. 46) is a validation record.

## 48.5 The V&V master plan

**Verification vs validation** is the distinction the whole submission turns on:
- **Verification** — *did we build the device right?* Each **design output meets its
  design input** (the spec). Largely **bench/engineering** testing.
- **Validation** — *did we build the right device?* The device **meets user needs and its
  intended use** in representative conditions. Includes **clinical/usability** evidence.

A **V&V master plan** for an EMT-enabled navigation system is a matrix: **design input →
standard/method → test → acceptance criterion → result/record**. A representative slice:

| Design input | Standard / method | Test (where in book) | Acceptance (example) |
|---|---|---|---|
| Positional accuracy over the working volume | NEMA/Hummel-style protocol [@hummel2005] | accuracy map + GT rig (Ch. 33) | 95% target error ≤ τ across spec volume |
| Robustness to field distortion | distortion phantom + detect-and-flag (Ch. 27) | dynamic/distortion test (Ch. 33, T2.27) | flag asserts before error exceeds τ |
| Electrical safety | IEC 60601-1 [@iec60601_1] | safety lab | pass |
| EMC (emissions/immunity) | IEC 60601-1-2 [@iec60601_1_2] | EMC lab | pass at intended-environment levels |
| Software lifecycle | IEC 62304 [@iec62304] | SW V&V, unit→system (Ch. 35) | tests pass at the software safety class |
| Usability / use safety | IEC 62366-1 [@iec62366]; FDA HF [@fda_hf2016] | summative HF study (Ch. 46) | critical tasks performed safely |
| Risk controls effective | ISO 14971 [@iso14971] | risk-control verification (Ch. 45) | residual risk acceptable; benefit-risk positive |
| Cybersecurity (networked) | IEC 81001-5-1 / FDA premarket cyber | security V&V (Ch. 35, T2.14) | threats mitigated; SBOM maintained |

Two EMT-specific points the plan must get right: (1) **validate the *system* accuracy the
clinician sees** (propagated target error, Ch. 39/43/46), not only the bench pose error —
the regulator's accuracy claim lives at the target; and (2) **verify that detect-and-flag
actually fires** before error exceeds the clinical tolerance, because the entire safety
argument (Ch. 27/44/45/46) rests on that control being effective, not merely present.

## 48.6 Software, AI, and cybersecurity adjuncts

Modern EMT systems are software-defined, so three adjunct frameworks attach to the
submission:
- **IEC 62304** [@iec62304] — the software development lifecycle, with a **software
  safety classification (A/B/C)** that scales the required rigor (Ch. 35).
- **Cybersecurity** — for networked trackers, a premarket cybersecurity package (threat
  model, SBOM, secure update) under emerging standards (IEC 81001-5-1; FDA premarket
  cybersecurity), developed in Ch. 35 / T2.14.
- **AI/ML functions** — if ML distortion compensation (Ch. 27/30, T2.18) is in the
  product, its training/validation data, generalization evidence, and a **predetermined
  change-control plan** for model updates become part of the file.

## 48.7 Synthesis: the standards-to-evidence map and lifecycle

The chapters of Part XX and their neighbors are not a grab-bag — each is a **named input
to the regulatory file**:

| Concern | Standard | Book home |
|---|---|---|
| QMS & design controls | ISO 13485 / 21 CFR 820 (QMSR) | **Ch. 48** |
| Risk management | ISO 14971 | Ch. 45 |
| Usability / use safety | IEC 62366-1; FDA HF | Ch. 46 |
| Basic safety | IEC 60601-1 | Ch. 17 |
| EMC | IEC 60601-1-2 | Ch. 17 |
| Software lifecycle | IEC 62304 | Ch. 35 |
| Cybersecurity | IEC 81001-5-1 / FDA | Ch. 35 (T2.14) |
| Performance/accuracy | NEMA/Hummel-style | Ch. 33 |
| Clinical evidence | MDR Annex XIV / FDA clinical | Ch. 49 (T2.17) |
| Post-market | MDR PMS/PMCF; FDA MDR | Ch. 44 (T2.C3) |

And the lifecycle is a loop, not a line: **intended use → design controls/DHF →
V&V → submission (510(k)/De Novo/PMA or CE) → market → post-market surveillance** (Ch. 44,
T2.C3) → which feeds change control back into design. The regulatory pathway is, in the
end, the disciplined externalization of everything the rest of the book argues for: a
**stated claim**, an **accuracy budget** that supports it, **risk controls** that are
**verified to work**, and a **human-validated** way of showing the clinician how much to
trust the number.

> **Engineering takeaway.** EMT ships *inside* a regulated navigation system, and the
> **intended use** sentence sets the risk class, the accuracy spec, and the evidence
> burden — so claim discipline is the first cost lever. The **US** route is usually a
> **510(k)** on substantial equivalence to a predicate (De Novo for novel low/moderate
> risk, PMA for Class III); the **EU** route demonstrates conformity to the **MDR GSPR**
> via a Notified-Body QMS+dossier audit and a Clinical Evaluation Report. Both are fed by
> one engine: an **ISO 13485 / 21 CFR 820** quality system whose **design controls** make
> every requirement traceable to a **verification** (built it right) or **validation**
> (built the right thing) record in the **DHF**. For EMT specifically, **validate the
> target accuracy the clinician sees** (not just bench pose error) and **verify that
> detect-and-flag actually fires** before error exceeds the clinical tolerance — that
> control is the load-bearing member of the entire safety case.

---

## Open questions / to verify
- Build a **worked traceability matrix** for the Ch. 31 reference design (every design
  input → output → V&V record) as a downloadable artifact / Phase-6 table.
- Confirm the **QMSR effective date (2026-02-02)** and any transition guidance closer to
  publication; track FDA cybersecurity and **AI/ML (PCCP)** guidance versions as they
  update (conf: high on the rule, med on evolving guidance editions).
- Add a concrete **predicate-device worked example** (a real cleared EMT navigation
  510(k) and its predicate chain) once vendor-facts are verified in the Ch. 28 pass (X1).
- Cross-check **MDR Rule 11** classification outcomes against published Notified-Body
  guidance for navigation software (conf: med).

## Sources cited
- [@fda_510k] 510(k)/substantial equivalence; [@fda_denovo] De Novo; [@eu_mdr] EU MDR
  (GSPR, classification, conformity assessment, clinical evaluation); [@iso13485] QMS;
  [@cfr820] 21 CFR 820 / QMSR; [@iec62304] software lifecycle; [@iso14971] risk;
  [@iec62366]/[@fda_hf2016] usability; [@iec60601_1]/[@iec60601_1_2] safety/EMC;
  [@hummel2005] accuracy protocol. Design-controls/V&V evidence is produced across
  Ch. 17/27/33/35/45/46; clinical evidence in Ch. 49; post-market in Ch. 44.
