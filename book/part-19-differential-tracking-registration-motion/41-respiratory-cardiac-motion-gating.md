# Chapter 41 — Respiratory & Cardiac Motion: Gating & Modeling

> **Status:** DEEPENED (awaiting review) · **Part XIX — Differential Tracking, Registration & Motion**
> The dynamic clinical error the reference frame *cannot* reach. Closes the
> manuscript's C2 gap: the dominant in-situ error in many procedures is physiological
> **motion of the target relative to the patient**, not tracker noise. Citation keys
> resolve to [`../../citations/bibliography.json`](../../citations/bibliography.json).

The patient reference sensor (Ch. 38) cancels **bulk rigid** patient and table
motion as common-mode. But the clinically interesting target — a heartbeat-driven
ablation site, a respiration-driven lung lesion or liver dome — moves **relative to**
the reference, non-rigidly and cyclically. This is exactly the residual Borgert et
al. measured: a sternal reference predicts an internal needle's respiratory motion
only ~94 %, leaving a fourfold-reduced *but nonzero* error [@borgert2006]. That
residual, $\sigma_\text{motion}$, is the term that was structurally missing from the
book's earlier budgets, and in thoracic/abdominal/cardiac work it can **dominate
everything else** — tens of millimetres before management. This chapter develops the
two physiological motions, the three management strategies (gate, model-compensate,
4D-model), the surrogate–target correspondence model and its hysteresis/drift
failure modes, the role of prediction under latency, and a worked budget showing the
term collapse from ~20 mm to a few mm.

---

## 41.1 The two motions, and why the reference cannot remove them

| | Respiratory | Cardiac |
|---|---|---|
| Frequency | ~0.2–0.3 Hz (12–18 /min) | ~1–1.5 Hz (60–90 bpm) |
| Amplitude (target) | liver/lung **10–25 mm** SI | chamber walls **mm–cm** |
| Character | quasi-periodic, **hysteretic**, baseline drift | quasi-periodic, ECG-correlated |
| Dominant in | ENB, IR (liver/lung) | cardiac EP |

Both are **target-relative**: the diaphragm pushes the liver through the (reference-
defined) patient frame, so the differential measurement of Ch. 38 reports it
faithfully as *target motion* — correctly, but uselessly, because the preoperative
image is a single static snapshot. Compounding it, the **image is acquired at one
phase** (a breath-hold, or one 4D-CT bin) while the procedure runs during free
breathing — a systematic **phase mismatch** that survives even a perfect rigid
registration (Ch. 39–40).

## 41.2 Three strategies

**(1) Gating.** Accept tracking data, register, and act **only at one phase** of the
cycle — typically **end-expiration**, where breathing dwells longest and is most
reproducible — matched to the image's phase [@keall2006]. Simple and robust; the cost
is **duty cycle** (most of the cycle is discarded) and **latency** (you wait for the
gate). End-expiration gating typically leaves a few-millimetre residual within the
gating window at ~30–40 % duty.

**(2) Surrogate + correspondence model (real-time compensation).** Measure a
**surrogate** (a chest-wall reference sensor, respiratory belt, spirometer, or the
internal sensor itself) and apply a learned **correspondence model** mapping
surrogate → target displacement, subtracting the predicted motion continuously
[@mcclelland2013]. Full duty cycle and real-time, but limited by model error,
hysteresis, and drift. Borgert's affine sternum→needle model is the canonical
instance (~4× residual reduction) [@borgert2006].

**(3) 4D / patient-specific motion model.** Build the model from **4D-CT** (a CT
binned across the cycle) or a biomechanical model, and **deform** the registration
(Ch. 40 §40.4) as a function of the surrogate phase [@mcclelland2013; @keall2006].
The most complete and the most data- and compute-heavy.

These are points on one curve: **residual error vs. duty cycle / complexity**. Gating
buys low residual at low duty; modeling buys full duty at model-limited residual.

## 41.3 The correspondence model and its failure modes

Let $s(t)$ be the surrogate and $\mathbf p(t)$ the target displacement. The simplest
model is **affine**, $\mathbf p = \mathbf A\,s + \mathbf b$, fit by least squares over
a synchronized training segment [@borgert2006]. Four physiological realities break the
naive single-valued fit, and each is a design requirement [@mcclelland2013]:

- **Hysteresis.** The target traces a *loop* against the surrogate — the inhale path
  differs from exhale — so $\mathbf p$ is **not single-valued** in $s$. Capture it
  with **phase + amplitude**, or by including the surrogate *velocity* $\dot s$ (a 2-D
  state), not $s$ alone. (The physiological cousin of the sensor hysteresis of
  Ch. 34: a multivalued map a single-input model cannot represent.)
- **Inter-cycle variability & baseline drift.** Breathing amplitude and baseline
  wander; a static model accrues a slow target offset. The model must **adapt**
  (re-fit online) or be periodically retrained.
- **Intra-procedure change.** Over a long case (anaesthesia depth, organ settling) the
  surrogate→target relationship itself drifts — the model can become invalid.
- **Imperfect correlation.** Even at best, correlation is ~94 % [@borgert2006];
  respiratory and cardiac motion **superpose**, and the unexplained variance is
  irreducible residual.

Model quality sets $\sigma_\text{motion}$ directly — the term the reference frame
left behind (Ch. 38 §38.7).

## 41.4 Cardiac gating in EP

Electroanatomical mapping (Ch. 28.4, 29.1) acquires points over many beats; without
gating the chamber would be **motion-blurred**. CARTO/EnSite-class systems therefore
**ECG-gate** acquisition to a fixed cardiac phase (e.g. end-diastole) so the map is
built at a consistent geometry, and often add **respiratory** compensation on top
(double-gating, or using the catheter's own motion/impedance). The lesson generalises:
*acquire and act at a reproducible phase of every cyclic motion present*.

## 41.5 Prediction under latency

Compensation must **predict**, not merely measure: by the time the system computes and
acts, the target has moved (the latency budget, Ch. 12). A periodic motion model lets
you **extrapolate** the target's pose a latency $\tau$ ahead (phase advance), and a
filter (Ch. 21) with a periodic/AR motion model does this naturally. Prediction error
grows with $\tau$ and with breathing **irregularity** — so the latency budget and the
motion-management strategy are coupled: lower latency (Ch. 12, 36) shrinks the
prediction horizon and the residual.

## 41.6 Worked budget — the missing term, collapsed

A liver target with **20 mm** peak-to-peak respiratory excursion (SI), under the
clinical accuracy chain of Ch. 38 §38.7:

| Strategy | $\sigma_\text{motion}$ residual | Duty cycle | Note |
|---|---:|---:|---|
| **None** | ~20 mm | 100 % | dominates every other term |
| **End-expiration gating** | ~2 mm | ~30–40 % | reproducible phase [@keall2006] |
| **Surrogate model (≈4×)** | ~5 mm | 100 % | real-time [@borgert2006] |
| **4D model + deformable** | ~2–3 mm | 100 % | most complex [@mcclelland2013] |

The point is stark: **uncompensated, motion is the budget** (a 1 mm tracker is
irrelevant behind 20 mm of breathing); managed, $\sigma_\text{motion}$ drops to a few
millimetres and the *other* terms (registration, tip, tracking) re-enter contention.
This is precisely the "attack the dominant term" lesson (Ch. 12, 29) — and the
dominant term in thoracic/abdominal/cardiac EMT is **motion**, which the book had not
previously budgeted.

## 41.7 Workflow integration and failure modes

- **Match phases end-to-end:** image phase ↔ registration phase ↔ navigation
  gate/model phase. A full-inspiration breath-hold CT navigated during tidal breathing
  is a systematic error no rigid registration removes (§41.1).
- **Detect-and-flag** (Ch. 27): when breathing turns **irregular** (cough, sigh,
  patient motion) or the **surrogate–target correlation drops**, the model is invalid
  — reduce confidence, widen the gate, or pause, rather than present a confidently
  wrong compensated pose.
- **Guard against over-trust:** a compensated display that shows residual as *zero*
  invites automation bias (human factors, T1.10); show the *uncertainty*, not a false
  certainty.

> **Engineering takeaway.** The reference frame removes bulk patient motion; it does
> **not** remove the target's own respiratory and cardiac motion, which in
> thoracic/abdominal/cardiac procedures is often the **largest** error of all. Manage
> it by **gating** to a reproducible phase (low residual, low duty), **surrogate +
> correspondence modeling** (full duty, model-limited — and you must model
> *hysteresis* and *drift*), or **4D/biomechanical** models — always **predicting**
> ahead by the system latency, matching phases from image to action, and
> **flagging** when breathing goes irregular. Only once $\sigma_\text{motion}$ is
> managed do tracker accuracy and registration even matter.

---

## Open questions / to verify
- Phase-5 sim: a surrogate–target **correspondence model** (affine vs. hysteresis-
  aware) on synthetic respiratory traces, quantifying residual vs. model order and vs.
  prediction horizon (ties Ch. 12 latency, Ch. 21 motion model).
- Add procedure-specific motion amplitudes with primary sources (lung-lesion vs.
  liver vs. cardiac-chamber excursion ranges) to firm up §41.1/§41.6 (currently
  representative, conf: med).
- Add a cardiac-EP **double-gating** primary reference and a clinical
  motion-compensation accuracy dataset.
- Connect to T1.10 (human factors) for the over-trust/uncertainty-display point and to
  the deferred motion-model interactive tool.

## Sources cited
- [@borgert2006] surrogate (sternum) → internal (needle) affine model, ~94 %
  correlation, ~4× residual reduction. [@mcclelland2013] definitive review of
  respiratory motion models (surrogate, correspondence, hysteresis, drift, 4D).
  [@keall2006] AAPM TG-76 respiratory-motion management (gating, end-expiration,
  duty cycle, 4D-CT). Cardiac electroanatomical gating from Ch. 28.4/29.1; deformable
  mechanism from Ch. 40 §40.4; prediction/latency from Ch. 12, 21; the budget term it
  fills from Ch. 38 §38.7.
