# Chapter 42 — Distortion from Metal Inside the Patient

> **Status:** DEEPENED (awaiting review) · **Part XIX — Differential Tracking, Registration & Motion**
> Closes the C4 gap and confronts a contradiction in the book's own doctrine: the
> distortion chapters (Ch. 6, 27) say "keep distorters out of the working volume," but
> the worst distorters are **inside the patient and cannot be removed**. Citation keys
> resolve to [`../../citations/bibliography.json`](../../citations/bibliography.json).

The distortion physics of Ch. 6 culminates in eq. 6.4: the field perturbation from a
nearby conductor scales as $a^3 r^3/(d_t^3 d_s^3)$, **diverging as the distorter
approaches the sensor** ($d_s\to0$). The compensation chapter (Ch. 27) and the
clinical chapters (Ch. 29) then advise the obvious remedy — keep metal out of the
volume. For an enormous fraction of real procedures that advice is **impossible to
follow**: stents, prosthetic valves, sternal wires, orthopedic and spinal hardware,
embolization coils, pacemaker/ICD cans and leads — and, most insidiously, the tracked
**instrument's own metal** — all sit in or right at the working volume, often at the
catastrophic $d_s\to0$ geometry, and cannot be taken out. This chapter develops the
taxonomy of in-patient metal, the static-vs-moving distinction, the under-appreciated
**instrument self-distortion** problem, the **bidirectional** active-implant case
(implant-as-distorter *and* EMT-field-as-EMI-source), the irony that the same metal
corrupts the **registration CT**, and the adapted response hierarchy when removal is
off the table.

---

## 42.1 The doctrine fails inside the body

"Keep distorters out" assumes you *can*. Inside the patient you cannot — and the
geometry is the worst case the book's own physics identifies. With an in-patient
distorter, the transmitter-to-distorter distance $d_t$ is comparable to the
transmitter-to-sensor range $r$ (both are deep near the generator), so $r/d_t\approx1$
and eq. 6.4 reduces to
$$
\frac{|\mathbf B_\text{pert}|}{|\mathbf B_0|}\ \sim\ \Big(\frac{a}{d_s}\Big)^{3}\times O(1),
\tag{42.1}
$$
i.e. the distortion is governed almost entirely by the **conductor size relative to
its distance from the sensor**. Metal a few millimetres from the sensor is therefore
not a second-order nuisance — it is a first-order, potentially order-unity field
error. The whole chapter follows from (42.1).

## 42.2 A taxonomy of in-patient metal

| Class | Examples | Mobility | Worst for |
|---|---|---|---|
| **Passive implants** | coronary/peripheral stents, mechanical & bioprosthetic valves, sternal wires, hip/knee/spinal hardware, IVC filters, coils, clips | fixed in anatomy | EP, IR, spine |
| **The tracked instrument's own metal** | steel catheter **braid**, guidewire, needle, ablation electrode | moves *with* the sensor | every catheter/needle procedure |
| **Other tools in the field** | a second catheter, guidewire, introducer, retractor | moves independently | multi-tool EP/IR |
| **Active devices** | pacemaker/ICD **can + leads**, neurostimulators | can fixed, leads move with heartbeat | cardiac EP (also §42.5) |

Two are uniquely EMT-specific and under-treated in the literature: the **instrument's
own metal** (§42.4) and the **active device as a dual distorter/EMI concern** (§42.5).

## 42.3 Static vs. moving in-patient distortion

- **Static in-patient metal** (a stent, a valve, fixed hardware) is fixed *in the
  patient frame* (Ch. 38). After registration it is therefore a **patient-specific
  static distortion** — in principle mappable into the patient's field model, the way
  installation distortion is mapped in Ch. 26. In practice it is rarely corrected,
  because its size/shape/location are unknown a priori and impractical to measure
  intra-procedurally. (A research opportunity: derive the implant's distortion from
  its CT appearance — §42.6.)
- **Moving in-patient metal** (the catheter braid, a guidewire, a heartbeat-driven
  lead or valve) is the *dynamic* distortion case — the genuinely hard, often-unsolved
  problem of Ch. 27, now with the distorter **inside** the patient and sometimes
  **co-moving with the sensor**.

## 42.4 Instrument self-distortion — the catheter braid

The most overlooked source is the tracked tool itself. Catheters are often built with
a **stainless-steel braid** for torque and pushability, and the sensor sits *inside*
it — a conductor at $d_s\approx0.5$–$1$ mm. Equation (42.1) is then brutal: an
effective $a\sim1$–$2$ mm at $d_s\sim1$ mm gives $(a/d_s)^3\sim\!1$–$8$ — an
**order-unity** self-distortion that no external compensation can reach, because it
travels with the sensor (illustrative scaling — the braid is not a compact sphere, so
the perfect-conductor form overstates the coefficient, but the *conclusion* that
steel at the sensor is intolerable holds; conf: med). The remedies are
**construction**, not compensation:
- a **metal-free distal segment** housing the sensor, or a **non-ferromagnetic/
  non-conductive braid** (polymer, or a metal chosen for low eddy response) near it;
- **calibrating the repeatable part** of the self-distortion (a fixed braid–sensor
  geometry gives a fixed, per-device offset → foldable into factory calibration,
  Ch. 26) — though the **flex-dependent** part as the catheter bends is far harder;
- accepting that **other tools** in the field (a guidewire alongside, a second
  catheter) each add their own moving distortion, compounding in multi-tool work.

## 42.5 Active implants — distortion *and* EMI, both ways

A pacemaker or ICD in a cardiac-EP patient is **two** problems at once:

- **Implant → field (distortion).** The ICD **can** is a centimetre-scale conductive/
  partly-ferromagnetic mass; near a cardiac catheter ($a\sim2.5$ cm, $d_s\sim4$–5 cm),
  (42.1) gives $(a/d_s)^3\sim0.2$ — a ~20 % field perturbation, i.e. **millimetre-to-
  centimetre** position error, with the **leads** adding a heartbeat-moving distorter.
  This is a real, common geometry (EP ablations in patients with CIEDs).
- **Field → implant (EMI).** The EMT generator produces time-varying magnetic fields
  (kHz, µT) close to the chest. Low-frequency fields *can* be mis-sensed by a CIED as
  intrinsic cardiac activity, producing **pacing inhibition or inappropriate therapy**,
  the susceptibility depending on field strength and (unipolar vs bipolar) sensing
  configuration [@tiikkaja2013]. EMT field levels (µT-class) are typically well below
  the interference thresholds for the relevant band, and the **static** component is
  far below the ~mT that trips a CIED magnet/reed switch — but this **must be assessed
  per IEC 60601-1-2**, not assumed, precisely because the generator sits near the
  device. For perspective on the conservative end, even a *0.1 T* magnetic-navigation
  system (orders of magnitude stronger than EMT) is "not strictly contraindicated,
  caution advised" with CIEDs (conf: med — by analogy; EMT-specific immunity testing
  is the proper basis). The honest posture: **EMT–CIED EMI is generally low-risk but a
  mandatory verification item**, and the implant's *distortion* is the larger practical
  effect.

## 42.6 The CT-artifact irony — metal hurts twice

The same metal that distorts the live EMT field also produces **metal artifact**
(beam hardening, streaking) in the **registration CT** — degrading the image *exactly
where the metal is*. So in-patient metal damages tracking **and** corrupts the
reference: fiducials/landmarks near the implant are localized worse, inflating the FLE
that drives TRE (Ch. 39 §39.4) right where accuracy is already compromised by field
distortion. The two effects are co-located and compounding. (The flip side is an
opportunity: the CT *locates* the metal, so a planning step could **predict** where
EMT distortion will be worst and warn the operator — §42.7.)

## 42.7 The adapted response hierarchy

When the distorter cannot be removed, the Ch. 6/27 hierarchy is re-prioritised:

1. **Engineer the instrument** (§42.4) — the only fix for self-metal: metal-free
   distal segment, non-magnetic braid, factory-calibrated repeatable offset.
2. **Detect, bound, and flag — now primary, not a fallback** (Ch. 27 §27.4).
   Redundant channels, EM-vs-fluoro/IMU cross-checks, and the NIS alarm must catch
   when in-patient metal corrupts the reading; **never silently trust** a pose taken
   beside a stent or an ICD can.
3. **Plan from the CT** (§42.6) — use the pre-procedure image to locate implants,
   predict high-distortion zones, and choose reference/working geometry to maximise
   $d_s$ from known metal where anatomy allows.
4. **Characterise the repeatable, patient-specific static distortion** where feasible
   (§42.3) — a research frontier (implant-distortion-from-CT).
5. **Clinical protocol & disclosure** — operator awareness of implants near the
   target, accuracy expectations reduced near large metal, and explicit
   essential-performance/flagging behaviour (Ch. 17 §17.3, Ch. 29).

The special case that defeats even this: **spine navigation**, where the procedure's
*purpose* is to place metal (pedicle screws) — so each screw distorts the field for
the next, a self-defeating geometry that makes EMT spine navigation peculiarly hard
and the detect-and-flag discipline essential.

> **Engineering takeaway.** The book's "keep metal out" doctrine breaks down inside
> the patient, where stents, valves, hardware, active-device cans/leads, and above all
> the **tracked instrument's own steel braid** sit at the $d_s\to0$ geometry that
> eq. (42.1) shows is catastrophic. Self-metal is an **instrument-construction**
> problem (metal-free tip, non-magnetic braid, calibrated offset); fixed implants are
> a *patient-specific static distortion* (mappable in principle, usually just flagged);
> moving implants/tools are the hard dynamic case; and an active CIED is both a major
> distorter and a mandatory **EMI-verification** item near the chest. When you cannot
> remove the distorter, **detect-bound-flag becomes the primary defense** — and the
> same metal that distorts the field also corrupts the CT you registered to.

---

## Open questions / to verify
- Add a **quantitative in-patient-distortion dataset** (implant type/size vs. position
  error) from primary measurement/FEA (ties Ch. 6 eq. 6.4 / Ch. 7) — currently the
  numbers are scaling-law estimates (conf: med).
- Source primary references for **catheter-braid self-distortion** characterization
  and mitigation, and for **EMT-specific CIED immunity** testing (beyond the
  low-frequency-field analogy [@tiikkaja2013]).
- Develop the **implant-distortion-from-CT** idea (predict distortion from the
  registration image) as a research direction (Ch. 30) and a planning feature.
- Quantify the **spine-navigation** screw-by-screw distortion accumulation as a worked
  case.

## Sources cited
- [@tiikkaja2013] in-vivo low-frequency-field EMI with pacemakers/ICDs — the
  active-implant EMI basis (§42.5). In-patient-metal *distortion* rests on the Ch. 6
  induced-dipole scaling (eq. 6.4 → eq. 42.1) and the instrument/environment-distortion
  literature [@poulin2002; @birkfellner1998; @franz2014]; the CT-artifact/FLE link to
  Ch. 39; the detect-and-flag hierarchy to Ch. 27; the patient/reference frame to
  Ch. 38.
