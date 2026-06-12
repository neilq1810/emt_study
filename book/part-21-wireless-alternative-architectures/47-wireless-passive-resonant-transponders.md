# Chapter 47 — Wireless & Passive Tracking: Resonant Transponders

> **Status:** DEEPENED (awaiting review) · **Part XXI — Wireless & Alternative Architectures**
> Closes the C5 gap: the book's taxonomy of EM tracking has been entirely **wired-
> sensor** based, omitting a real, FDA-cleared modality with *no sensor wires at all*
> — the **resonant LC transponder** (Calypso-class). Citation keys resolve to
> [`../../citations/bibliography.json`](../../citations/bibliography.json).

Every tracker in this book so far places an *active* sensor — an induction coil or a
biased magnetometer — on the tracked object and runs wires (and a connector, the
dominant failure mode of Ch. 44) back to the electronics. There is an entirely
different architecture that the taxonomy has ignored: put a **passive resonant tag**
on the object, energise and read it **wirelessly** from an external array, and solve
the same dipole inverse from the *outside*. This is how **Calypso** (Varian) provides
real-time, non-ionising "GPS for the body" tracking of implanted markers during
radiotherapy [@balter2005; @willoughby2006], and it is a commercial EM-tracking
modality whose omission makes the book's survey incomplete. It also turns out to be a
*deliberate, cooperative* version of physics the book has already developed — the
reflected-impedance sensing of Ch. 27.7 and the eddy-settling of Ch. 6.4 — which is
why it belongs here, not in a footnote.

---

## 47.1 The passive resonant LC transponder

A transponder is a tiny **series LC resonant circuit** — a coil and a capacitor tuned
to $f_0 = 1/(2\pi\sqrt{LC})$ — sealed in a biocompatible glass capsule, with **no
power source and no wires**. An external **source array** transmits a magnetic field
that **excites** the tag at its resonance; when the excitation stops, the tag
**rings down** at $f_0$, re-radiating a decaying magnetic dipole field that an external
**receive array** detects. The tag's position is then solved from the array's readings
by exactly the **dipole inverse problem** of Ch. 5/23 — only now the passive tag plays
the role of the source and the external array plays the role of the sensor (the
**reciprocity** of Ch. 5 §5.5). Multiple transponders tuned to **distinct
frequencies** are separated by frequency-division multiplexing (Ch. 19), giving
several tracked points at once.

The decisive trick is **frequency- and time-selective detection** that rejects clutter:
excite broadly, let the **non-resonant** eddy currents in surrounding metal **decay**
(the $\tau_e=\mu_0\sigma a^2/\pi^2$ settling of Ch. 6 eq. 6.3), then **listen** in the
window where the **narrowband** tag is still ringing at $f_0$ while the broadband
clutter has died. The tag's ring-down time is set by its quality factor,
$\tau_\text{ring}\sim Q/(\pi f_0)$ — e.g. $Q=50$ at $f_0=400$ kHz gives
$\tau_\text{ring}\approx 40\,\mu$s — so the tag is separated from non-resonant metal in
**both** frequency and time. This is the *same* "excite, wait, then read" idea as
pulsed-DC (Ch. 6.4, 27.6), repurposed to isolate a **cooperative resonant target**
instead of escaping a hostile one.

## 47.2 Calypso — the canonical system

The Calypso 4D Localization System implants three **"Beacon" transponders**
(≈8 mm × 2 mm glass-encapsulated LC tags, at distinct resonant frequencies) in or near
the target (prostate, lung, etc.). An external array above the patient excites and
reads them at **~10 Hz**, and the three positions define the **position and
orientation** of the target volume in real time — tracking respiratory/organ motion
during external-beam radiotherapy for gating or beam-tracking, without ionising
radiation. Reported localization accuracy is **~1–2 mm** vs radiographic reference
[@balter2005; @willoughby2006]. It is, in effect, a wireless, implantable analogue of
the differential reference sensor of Ch. 38 — the implanted tags *are* the patient
reference, moving with the anatomy.

## 47.3 Active vs. passive wireless — the design space

| Architecture | Power at tag | DOF/tag | Pros | Cons |
|---|---|---|---|---|
| **Passive resonant (Calypso)** | none | position only (≥3 for orientation) | tiny, implantable, no battery, no wire/connector | weak signal, steep depth falloff, position-only |
| **Active powered + telemetry** (e.g. FM-wireless [@crowley2023]) | battery / harvested | up to 6-DOF coil | full pose per tag, stronger signal | needs power → larger, finite life |
| **Backscatter / RFID-style** | none / harvested | position | scalable, cheap | modulation/SNR limits |

Passive resonant is the mature clinical instance; the active FM-wireless work of Crowley
et al. [@crowley2023] is the route to a *wireless 6-DOF* sensor (a full coil whose
reading is modulated onto a radio link), at the cost of needing power at the tag.

## 47.4 Why it belongs in this book — the physics is already here

The transponder is not a new physics; it is the book's own machinery run cooperatively:
- **Reflected impedance / transmitter-side sensing (Ch. 27.7).** A Calypso array is a
  *transmitter-side* sensor of a **deliberate** resonant target — the cooperative dual
  of the distorter the generator senses through its reflected impedance. The
  transponder is the witness/reflected-load idea inverted into a feature.
- **Resonant ring-down ↔ eddy settling (Ch. 6.4 / 27.6).** The tag rings where stray
  metal decays; the same pulsed-excite-then-listen separation, now frequency-selective.
- **Reciprocity (Ch. 5.5).** Passive tag + external array is the reciprocal of sensor
  coil + external generator — the forward model and solver are unchanged.
- **Dipole inverse (Ch. 23) and FDM (Ch. 19).** The localization math and the
  multi-tag multiplexing are exactly those already developed.

So the transponder modality costs the reader no new theory — it **recombines** Chs. 5,
6, 19, 23, and 27 into a wireless architecture, which is precisely why its omission was
a taxonomy gap rather than a missing physics.

## 47.5 The trade against wired sensors

- **Reliability — a real win.** Removing the wire and **connector** removes the
  **dominant field-failure mode** (Ch. 44): a passive implanted tag has no connector to
  fatigue, no cable to flex, no power to deliver to the patient end (and so none of the
  Ch. 17 patient-power burden). For long-term implanted tracking this is decisive.
- **Signal — a real cost.** The re-radiated signal traverses the inductive coupling
  **twice** (array→tag→array), so it scales as $k^2$ with $k\propto1/d^3$ — i.e.
  $\sim 1/d^6$ — a **far steeper** depth falloff than the $1/d^3$ of a driven sensor
  (Ch. 5). Passive transponders are therefore **depth-limited** and demand a close
  external array and a high-$Q$ tag.
- **DOF — position only.** Each tag gives position; **orientation needs ≥3** tags
  (as Calypso uses), versus a single 6-DOF coil.

## 47.6 Limitations and the frontier

- **Depth/SNR** ($1/d^6$, §47.5) caps the working volume and target depth.
- **Metal distortion still applies** — the external array sees the same OR metal
  (Ch. 6, 42); the frequency selectivity rejects *non-resonant* eddy clutter, but a
  nearby ferromagnet can **shift the tag's $f_0$** (a resonance pull) and degrade
  detection, and large implants near the tag still perturb the field (the metallic-hip
  case is clinically documented for Calypso).
- **Implant practicalities** — invasive placement, **migration**, and **MRI
  compatibility** of the implanted LC tag.
- **Frontier:** wireless **6-DOF** active sensors (FM-wireless [@crowley2023]),
  **backscatter** and **energy-harvesting** tags, and wireless **capsule** localization
  (the MR-array capsule of Ch. 14.3) — the research edge of untethered EM tracking
  (Ch. 30).

> **Engineering takeaway.** Wireless **passive resonant transponders** (Calypso-class)
> are a real, FDA-cleared EM-tracking modality the book's wired-sensor taxonomy had
> omitted: a passive LC tag is excited and read by an external array, located by the
> same dipole inverse (reciprocity), separated from clutter by resonant
> frequency/time selectivity (the eddy-settling and reflected-impedance physics of
> Chs. 6 and 27 used *cooperatively*), and multiplexed by FDM (Ch. 19). It **wins on
> reliability** — no wire, no connector, no patient-end power — and **loses on signal**
> ($1/d^6$ depth falloff) and DOF (position-only, ≥3 tags for orientation). The active
> wireless route (FM-wireless 6-DOF) trades a battery for full pose. Either way, the
> taxonomy of EM tracking is incomplete without the untethered branch.

---

## Open questions / to verify
- Add the **resonance-pull** quantification (ferromagnet-induced $f_0$ shift vs.
  detection degradation) and a primary reference for the **metallic-implant** effect on
  Calypso (clinically reported, conf: med).
- Source the **transponder design parameters** (typical $L$, $C$, $Q$, $f_0$ band,
  array geometry) from primary/regulatory documentation to firm up §47.1–47.2.
- A Phase-5 sim of the **$1/d^6$ passive-coupling SNR** vs. depth and a worked
  excite-settle-listen timing budget (ties Ch. 6 $\tau_e$, the §47.1 ring-down).
- Expand the **active wireless 6-DOF** and **backscatter** routes (Ch. 30) with
  quantified accuracy/range as that literature matures [@crowley2023].

## Sources cited
- [@balter2005] foundational Calypso wireless-transponder accuracy; [@willoughby2006]
  clinical real-time tracking with three implanted transponders at 10 Hz. [@crowley2023]
  the active FM-wireless route to 6-DOF. The enabling physics is reused from Ch. 5
  (reciprocity, coupling), Ch. 6 (eddy settling), Ch. 19 (FDM), Ch. 23 (dipole inverse),
  Ch. 27.7 (reflected-impedance/transmitter-side sensing); the reliability advantage is
  Ch. 44; the reference-sensor analogy is Ch. 38.
