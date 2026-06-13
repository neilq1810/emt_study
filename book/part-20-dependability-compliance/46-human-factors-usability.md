# Chapter 46 — Human Factors & Usability Engineering

> **Status:** DEEPENED (awaiting review) · **Part XX — Dependability & Compliance** (closes Part XX)
> Closes the T1.10 gap and the over-trust/automation-bias thread that Ch. 41 and Ch. 45
> forward-referenced. The system being navigated is not the tracker — it is the tracker
> **plus the clinician**, and a perfectly accurate pose can still cause harm through
> **use error**. Citation keys resolve to [`../../citations/bibliography.json`](../../citations/bibliography.json).

Every prior chapter optimised the *device*. But use error is a leading cause of
medical-device harm — frequently exceeding device failure — and a tracker that is
correct to the micron is useless, or dangerous, if the clinician mis-reads it,
over-trusts it, or is mis-led by its display. **IEC 62366** [@iec62366] makes
usability engineering a required discipline, feeding use-related hazards into the risk
file (Ch. 45). This chapter applies it to EMT: it treats the **human as part of the
system**, enumerates the EMT-specific use errors, develops the **trust-calibration**
problem that the book's recurring "detect-and-flag" depends on, and argues that the
single most important interface decision is to **display uncertainty, not false
precision**.

---

## 46.1 The human is in the loop

The navigated "system" is **device + clinician + workflow**. The pose can be exactly
right and harm still occur if the operator reads the wrong frame, accepts a bad
registration, fails to notice a loss-of-tracking flag, or simply trusts a precise-
looking crosshair more than the physics warrants. IEC 62366 therefore treats the **use
error** as a hazard on equal footing with a hardware fault (the over-trust row of the
Ch. 45 hazard table), and requires that **critical tasks** — those where a use error
could cause harm — be identified and **validated** with representative users. The
corollary is structural: the detect-and-flag control that Ch. 27/44/45 lean on
**reduces risk only if the human perceives the flag and responds correctly** — and
that is a human-factors property, not a device property.

## 46.2 EMT-specific use errors

| Use error | Mechanism | Control (HF) |
|---|---|---|
| **Automation bias / over-trust** | a sharp crosshair *implies* a certainty the system lacks; the displayed FRE reads reassuringly small (Ch. 39) | **display uncertainty** (§46.4); calibrate trust (§46.3) |
| **Mode confusion** | which frame / tool / phase? (gated vs live, registered vs not, which catheter) — Ch. 43 frame confusion as a *use* error | unambiguous mode/frame indication |
| **Accepted mis-registration** | operator accepts a bad registration because FRE "looked fine" (Ch. 39 §39.3) | forced, salient verification on an *independent* check |
| **Missed loss-of-tracking** | a frozen display looks live; the flag is not noticed | **blank/grey-out**, not freeze; unmissable failure indication (§46.4) |
| **Alarm fatigue** | too many distortion/quality warnings → operator tunes them out | salient-but-sparse alarm design; tiered severity |
| **Setup errors** | reference-patch misplacement, fiducial mis-picking, generator positioning | guided setup, forcing functions, checklists |
| **Workflow disruption → workaround** | if navigation slows the case, the operator disables/ignores it | fit the workflow; minimal setup; hands-busy design |

The recurring thread: an EMT display **over-promises precision**, and the operator's
response to its *failures* (flags, dropouts, distortion) is mediated by interface
design. Both are human-factors problems, not accuracy problems.

## 46.3 Trust calibration — the central HF problem

Parasuraman & Riley's framework names the failure modes precisely: **misuse**
(over-reliance / automation bias), **disuse** (under-reliance), and the goal of **trust
calibration** — the operator's trust should match the system's *actual* reliability
[@parasuraman1997]. Both directions are harmful in EMT:
- **Over-trust (misuse):** the clinician acts on a distorted or mis-registered pose
  because it looked authoritative → wrong-site therapy (the master hazard, Ch. 45).
- **Under-trust (disuse):** the clinician distrusts good guidance and reverts to
  fluoroscopy → the navigation benefit is lost *and* radiation dose rises (the
  benefit-risk dividend of Ch. 45 §45.5 is forfeited).

The interface's job is to make trust **track reliability moment-to-moment**: present
*more* confidence when the pose is good (clean field, good geometry) and *visibly less*
when it is not (distortion flagged, near a volume edge, reference suspect). A static,
always-confident crosshair guarantees mis-calibration in both directions. This reframes
"detect-and-flag" (Ch. 27) as a **trust-calibration** mechanism: the flag is how the
device tells the human to *lower* trust at exactly the right instant.

## 46.4 Display uncertainty, not false precision

The single highest-leverage interface decision follows from §46.3: **show the
uncertainty**. The estimator already produces a pose **covariance** (Ch. 11 §11.6,
Ch. 24), the registration a **TRE** (Ch. 39), and the chain a propagated covariance
(Ch. 43 §43.5). Rendering that honestly — an **error ellipsoid** or a crosshair whose
size/colour grows with covariance, a registration-quality indication based on
*predicted TRE at the target* (not FRE), a confidence that drops visibly under a
distortion flag — gives the operator the information to calibrate trust. A point
crosshair throws all of it away and **manufactures false certainty**, which is the
proximate cause of automation bias. (This is the clinician-facing realisation of the
uncertainty-communication item, T2.24, and the honest counterpart to the FRE-misuse
warning of Ch. 39.)

Three more interface imperatives specific to EMT:
- **Failure indication must be unmissable and unambiguous:** loss of tracking should
  **blank or grey** the navigation (so stale data cannot masquerade as live), not
  freeze it; the indication must survive a glance from a busy operator.
- **Latency is perceived as sluggishness** and the human-perception loop is unforgiving
  (Ch. 29.6) — the latency budget (Ch. 12) is a *usability* requirement, not only an
  engineering one.
- **Alarms must be tiered and sparse** to avoid fatigue, or the diagnostic coverage of
  Ch. 44 collapses at the human boundary.

## 46.5 The usability-engineering process and the safety case

IEC 62366's process [@iec62366]: **use specification** (users, uses, environment) →
identify **UI characteristics related to safety** → identify **known/foreseeable use
errors** and the **hazard-related use scenarios** they create → **formative**
evaluation (iterative, during design) → **summative** evaluation (validation with
representative users performing the **critical tasks** in realistic conditions,
demonstrating the UI is safe). The outputs feed the safety case:
- use-related hazards and controls go into the **ISO 14971 risk file** (Ch. 45);
- summative usability validation is part of **design validation** (Ch. 35 V&V);
- the result is the evidence that the detect-and-flag controls *actually work in the
  operator's hands* — closing the loop the device-only chapters left open.

**Worked hazardous-use scenario.** Mid-ENB, a distortion flag appears; the operator,
focused on the task and trusting a precise-looking crosshair, does not heed it and
biopsies the wrong spot (harm). HF controls: render the live **uncertainty ellipsoid**
so the crosshair never over-promises; on a confidence drop, **grey out** the navigation
and require acknowledgement; tier the alarm so it is salient but not fatiguing.
**Summative validation:** representative pulmonologists in a simulated case must
**reliably detect and correctly respond** to the flag — and if they do not, the
*interface*, not the user, has failed and must be redesigned. That is the IEC 62366
posture: **use error is a design defect, not operator error.**

## 46.6 A concrete uncertainty-display specification

§46.4 argues *that* uncertainty must be shown; this section specifies *how*, turning the
covariances the book already computes into pixels. The inputs are all in hand: the
solver's **6-DOF pose covariance** $\mathbf P$ (Ch. 11 §11.6, Ch. 24 §24.6), the
registration **TRE** at the target (Ch. 39), and any **distortion/quality flag**
(Ch. 27 NIS). The design problem is to map them to a display whose apparent confidence
tracks the *actual* reliability (§46.3).

**1 — Render the position ellipsoid honestly.** Take the position block
$\mathbf P_{pp}$ (the $3\times3$ part of $\mathbf P$); its eigenvectors are the
error-ellipsoid axes and its eigenvalues $\lambda_i$ the squared semi-axes. A
**95 % containment** ellipsoid scales each axis by $\sqrt{\chi^2_{3,0.95}}=\sqrt{7.815}
=2.80$ (three DOF), so the rendered semi-axes are $2.80\sqrt{\lambda_i}$; a single
projected axis uses the $1.96\sigma$ (1-DOF) factor. **Critical safety tie:**
$\mathbf P_{pp}$ **must be the orientation-marginalized block of the full $6\times6$
$\mathbf F^{-1}$** (§24.6), *not* the orientation-known $\mathbf F_{pp}^{-1}$ — the
latter is optimistic by the pose-invariant $\approx2.95\times$ coupling penalty, so a
display built on it would **under-draw the ellipsoid by ~3×** and manufacture exactly
the false certainty §46.4 warns against.

**2 — Render the tool-axis cone.** The orientation block gives an angular uncertainty;
draw the tool axis as a **cone** whose half-angle is $2.80\,\sigma_\varphi$ (95 %,
3-DOF) or $1.96\,\sigma_\varphi$ per axis. Because orientation degrades as $z^3$ and
position as $z^4$ (§24.6), the cone and the ellipsoid grow at *different* rates with
range — both must be live, not a single fudge factor.

**3 — Compose with registration.** The quantity the clinician actually cares about is
**target uncertainty**, so combine pose and registration in quadrature (independent
contributions): $\sigma_\text{tgt}=\sqrt{\sigma_\text{pos}^2+\text{TRE}^2}$, and inflate
on a distortion flag (Ch. 27). Report the **predicted 95 % target error**
$T_{95}=2.80\,\sigma_\text{tgt}$ — not FRE (Ch. 39 §39.3).

**Worked numbers (Phase-5 CRLB, $\sigma_B=1$ nT).** At mid-volume ($z=0.3$ m) the
marginalized position $\sigma_\text{pos}=0.086$ mm (§24.6), so the **95 % position ball
has radius $2.80\times0.086\approx0.24$ mm**; orientation $\sigma_\varphi=0.033^\circ$
gives a **95 % tool-axis cone half-angle $\approx0.092^\circ$**. With a representative
registration $\text{TRE}=0.8$ mm (Ch. 39), $T_{95}=2.80\sqrt{0.086^2+0.8^2}\approx2.25$
mm — i.e. **registration, not the tracker, dominates the number the surgeon sees**, and
the display should say so. (Had the display used the optimistic orientation-known
covariance, the tracker term would read $0.029$ mm — invisible — reinforcing the wrong
intuition that the tracker is "perfect.")

**4 — Map to a navigation-confidence state.** Collapse $T_{95}$ and the flags to a
**tiered GREEN/AMBER/RED** indicator against the *clinical* tolerance $\tau$ (the
accuracy the procedure requires, Ch. 29/45 — e.g. $\tau\approx2$ mm for many ENB
targets):

| State | Condition | Display behaviour |
|---|---|---|
| 🟢 GREEN | $T_{95}<\tfrac12\tau$, no flag, geometry well-conditioned | full-confidence crosshair + small ellipsoid |
| 🟡 AMBER | $\tfrac12\tau\le T_{95}<\tau$, **or** near volume edge / high PDOP (§24.3), **or** reference suspect | enlarged ellipsoid, caution colour, prompt to verify |
| 🔴 RED | $T_{95}\ge\tau$, **or** distortion flag set, **or** loss of tracking | **grey-out/blank** the navigation; do not show a pose |

This makes the detect-and-flag control (§46.3) a concrete pixel behaviour and ties the
threshold to the *procedure's* requirement rather than a fixed number. Two
implementation cautions: **hysteresis** on the state transitions (and a short temporal
filter on $\mathbf P$) so the indicator does not flicker AMBER↔GREEN frame-to-frame
(Ch. 12 update rate), and a **monotonic, pre-attentive** colour/size encoding so a busy
operator reads it at a glance (§46.2 alarm fatigue). The companion regulatory anchors are
the **FDA Human-Factors guidance** [@fda_hf2016] and **IEC 60601-1-6** [@iec60601_1_6],
which make this display a validated, not merely tasteful, design. (conf: med — the
$\chi^2$/TRE math and the §24.6 covariance are exact; the specific $\tau$-fractions and the
GREEN/AMBER/RED cut-points are a *proposed* scheme to be tuned per indication and validated
summatively (§46.5). A Phase-6 demo rendering live $\mathbf P$→ellipsoid is the natural
companion.)

> **Engineering takeaway.** The clinician is part of the navigated system, so a correct
> pose can still cause harm through **use error** — and usability engineering
> (IEC 62366) is therefore a safety discipline, not a polish step. EMT's defining
> human-factors risk is **automation bias** fed by a display that **over-promises
> precision**; the remedy is to **show uncertainty** (error ellipsoid, predicted TRE,
> confidence that visibly drops under distortion) so the operator's trust **tracks the
> system's actual reliability** (Parasuraman & Riley). Make failure indications
> unmissable (blank, don't freeze), keep alarms tiered and sparse, fit the workflow, and
> **validate the critical tasks with real users** — because detect-and-flag only reduces
> risk if a human reliably perceives and acts on the flag, and a use error that recurs
> is a design defect to fix, not a user to blame.

---

## Open questions / to verify
- ✅ **Resolved (§46.6, T2.24):** concrete uncertainty-display spec — $\chi^2_{3,0.95}$
  ellipsoid/cone scaling on the **orientation-marginalized** §24.6 covariance (the
  optimistic block under-draws by ~2.95×), quadrature composition with TRE, and a
  $\tau$-relative GREEN/AMBER/RED navigation-confidence state. Remaining: a Phase-6 demo
  rendering live $\mathbf P\to$ellipsoid, and per-indication tuning of the cut-points.
- ✅ **Resolved:** **FDA Human-Factors guidance** [@fda_hf2016] and **IEC 60601-1-6**
  [@iec60601_1_6] added as companion references (§46.5/§46.6).
- Build a representative **critical-task list** and **hazard-related use-scenario**
  set for EP and ENB, with summative acceptance criteria (ties Ch. 45 RMF).
- Source clinical evidence on **automation bias / over-trust in surgical navigation**
  and on alarm-fatigue thresholds to firm up §46.2/§46.3 (currently HF-principled,
  conf: med).

## Sources cited
- [@iec62366] usability-engineering process, critical tasks, summative validation.
  [@parasuraman1997] automation misuse/disuse and trust calibration — the basis for
  §46.3. [@fda_hf2016] FDA HF/usability guidance and [@iec60601_1_6] usability
  collateral standard — the regulatory anchors for §46.5/§46.6. The uncertainty to be displayed comes from Ch. 11/24 (covariance), Ch. 39 (TRE),
  Ch. 43 (propagated chain); use-related hazards feed the ISO 14971 file (Ch. 45); the
  detect-and-flag control whose human boundary this chapter closes is Ch. 27/44; the
  benefit (radiation) and FRE-misuse ties are Ch. 45/39.
