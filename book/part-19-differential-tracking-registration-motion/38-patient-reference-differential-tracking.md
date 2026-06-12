# Chapter 38 — The Patient Reference Sensor & Differential Tracking

> **Status:** DEEPENED (awaiting review) · **Part XIX — Differential Tracking, Registration & Motion**
> Opens Part XIX and closes the manuscript's largest structural gap: clinical EMT is
> not an *absolute* measurement in the generator frame (Parts II–XVIII) but a
> **differential** one, reported relative to a sensor on the patient. Citation keys
> resolve to [`../../citations/bibliography.json`](../../citations/bibliography.json).

Every chapter so far has computed pose in the **generator frame** — the lab frame of
the field generator. No clinical system reports pose that way. Instead a second
**reference sensor** is fixed to the patient, and the tracked instrument's pose is
reported **relative to that reference**. This single architectural choice — borrowed
from the *dynamic reference frame* of optical surgical navigation — is what makes EMT
usable on a breathing, shifting patient on a moving table, and it changes the error
analysis of everything that precedes it. A reference sensor **rejects patient and
table motion and slow generator drift as common-mode**, anchors the image
registration (Ch. 39–40), and defines the coordinate frame all downstream software
consumes (Ch. 35, T1.7). It also **adds its own noise and can import its own
distortion**, so it is not free. This chapter develops the differential measurement,
its common-mode rejection, its costs, reference placement, and its failure modes.

---

## 38.1 Why absolute tracking fails in the clinic

The generator frame is fixed to the *generator*, not the *patient*. In a real
procedure the patient breathes (chest wall moves cm-scale), the heart beats, the
table tilts or translates, and the staff bump the bed. In the generator frame, all
of this appears as **instrument motion** even when the instrument is stationary
relative to the anatomy. An absolute tracker faithfully reports that the catheter
moved 10 mm — when in truth the *patient* moved 10 mm and the catheter held still
against the vessel wall. For navigation against a preoperative image, what matters is
the pose **relative to the anatomy**, not the lab. Absolute tracking answers the
wrong question.

## 38.2 The differential measurement

Attach a 6-DOF **reference sensor** $R$ rigidly (as far as possible) to the patient,
and track the **tool sensor** $T$ as before. The generator $G$ measures both poses as
homogeneous transforms,
$$
\mathbf T_{G}^{R}=\begin{bmatrix}\mathbf R_{GR}&\mathbf t_{GR}\\ \mathbf 0&1\end{bmatrix},\qquad
\mathbf T_{G}^{T}=\begin{bmatrix}\mathbf R_{GT}&\mathbf t_{GT}\\ \mathbf 0&1\end{bmatrix}.
$$
The **reported quantity** is the tool *in the reference (patient) frame*:
$$
\boxed{\;\mathbf T_{R}^{T} \;=\; \big(\mathbf T_{G}^{R}\big)^{-1}\,\mathbf T_{G}^{T}\;}
\tag{38.1}
$$
with rotation $\mathbf R_{RT}=\mathbf R_{GR}^{\!\top}\mathbf R_{GT}$ and translation
$\mathbf t_{RT}=\mathbf R_{GR}^{\!\top}(\mathbf t_{GT}-\mathbf t_{GR})$. Equation
(38.1) is the whole idea: the generator frame **cancels out**. Registration to a
preoperative image then maps image→reference once (Ch. 39), and because the tool is
expressed in the reference frame, the overlay stays valid as the patient moves — the
registration does not have to be redone every breath. The frame graph
$G\!\to\!R\!\to\!T$ (and $R\!\to\!\text{image}$, $R\!\to\!\text{robot}$) is the
subject of the coordinate-frame chapter (T1.7).

## 38.3 Common-mode rejection — what cancels, quantified

Write each measured pose as truth + a perturbation. For a **rigid bulk motion**
$\boldsymbol\delta$ of the patient (and anything attached to them) in the generator
frame, *both* $\mathbf T_G^R$ and $\mathbf T_G^T$ are left-multiplied by the same
$\boldsymbol\Delta(\boldsymbol\delta)$:
$$
\mathbf T_R^{T}=\big(\boldsymbol\Delta\,\mathbf T_G^{R}\big)^{-1}\big(\boldsymbol\Delta\,\mathbf T_G^{T}\big)
=\big(\mathbf T_G^{R}\big)^{-1}\boldsymbol\Delta^{-1}\boldsymbol\Delta\,\mathbf T_G^{T}
=\big(\mathbf T_G^{R}\big)^{-1}\mathbf T_G^{T}.
\tag{38.2}
$$
The bulk motion **cancels exactly**. Respiration (≈cm), table shifts, and patient
repositioning are rejected to first order. The same argument rejects **slow generator
drift** that is *common* to both sensors (a global field scale/phase drift, or a
bulk mechanical shift of the generator): it appears as a common left-multiply and
divides out — complementing the ratiometric rejection of drive-amplitude drift
(Ch. 25 §25.4). This is why a reference sensor, not a better generator, is the
practical answer to slow drift.

**The limit of cancellation.** Equation (38.2) is exact only for *rigid* motion in a
*perfectly known, spatially uniform-enough* field. Two residuals remain:
- **Field-nonuniformity residual.** After a displacement $d$, the tool sits at a
  different point of the (imperfectly mapped) field; the leftover error scales as the
  field-model error *gradient* times $d$, $\sim|\nabla\varepsilon_\text{field}|\,d$.
  Large patient excursions through a poorly-mapped volume are not fully rejected.
- **Non-rigid motion.** If the reference and the target do not move together — a
  sternal patch versus the beating heart — the *target-relative* motion is **not**
  common-mode and survives (§38.6); this is the residual that motion gating and
  modeling (T1.4) must handle. Borgert et al. quantify exactly this: a sternal
  (external) sensor predicts an internal needle sensor's respiratory motion with up
  to ~94 % correlation in steady breathing, cutting residual internal motion by
  ~4× — strong, but neither perfect nor instantaneous [@borgert2006].

## 38.4 The cost: the reference adds noise (and the gradiometer payoff)

Differential tracking is not free. The reference sensor has its own stochastic error
$\boldsymbol\Sigma_R$, and because (38.1) composes the two poses, the relative-pose
covariance is, to first order,
$$
\boldsymbol\Sigma_{RT}\approx \mathbf J_T\boldsymbol\Sigma_T\mathbf J_T^{\!\top}
+\mathbf J_R\boldsymbol\Sigma_R\mathbf J_R^{\!\top},
\tag{38.3}
$$
with Jacobians of (38.1). For independent sensors of comparable quality this is
**root-sum-square**: the reference *adds* noise. *Worked:* a tool sensor at
$\sigma_T=0.5$ mm referenced to a similar $\sigma_R=0.5$ mm gives
$\sigma_{RT}=\sqrt{0.5^2+0.5^2}=0.71$ mm — a ~40 % noise penalty. But weigh it against
what it buys: rejection of **cm-scale** respiratory motion and **mm-scale** generator
drift. Trading +0.2 mm of jitter to reject 5–10 mm of motion is overwhelmingly worth
it — the reference is the cheapest large error-reduction in the whole system.

**Distortion partially cancels too — the gradiometer view.** Distortion is a
*spatially structured* field error $\mathbf D(\mathbf r)$ (Ch. 6, 27). The tool sees
$\mathbf D(\mathbf r_T)$, the reference $\mathbf D(\mathbf r_R)$; the differential
measurement (38.1) carries approximately $\mathbf D(\mathbf r_T)-\mathbf D(\mathbf
r_R)$. If the two sensors are **close** compared with the distortion correlation
length $L_D$, this difference is small, $\sim|\nabla\mathbf D|\,\lVert\mathbf
r_T-\mathbf r_R\rVert$ — the reference acts as a **gradiometer reference**, rejecting
the common, slowly-varying part of the distortion (the same principle as the
witness sensor of Ch. 27, now defining the frame rather than observing it). If the
sensors are **far apart**, the difference approaches the *full* distortion of both,
and the reference offers no distortion relief while still adding noise. This tension
sets placement (§38.5).

## 38.5 Reference placement — the central design decision

Placement trades four competing demands:

| Want | Pulls the reference toward… |
|---|---|
| Clean, stable field (low, repeatable distortion) | the well-mapped centre of the volume, away from metal |
| Distortion correlation with the tool (gradiometer) | **near the working volume / the tool** |
| Faithful patient-motion reference | **rigidly coupled to the relevant anatomy** |
| Out of the way (workflow, sterility) | the periphery / skin |

These conflict. A **skin patch** (adhesive, on sternum/back) is practical and
non-invasive but couples to anatomy *softly* — skin slides over ribs, adding a
**skin-motion artifact** between the reference and the bone/organ it is meant to
represent. A **bite-block** (ENT/skull-base) or a **bone-anchored** frame is far more
rigid but invasive. The reference must also sit where the field is clean: a reference
placed in a distorted or edge region **corrupts the entire patient frame**, mapping
that corruption into *every* tool reading (§38.6). The practical rule: **as rigid to
the target anatomy as tolerable, as near the working volume as workflow allows, in
the cleanest field you can find** — and verify its quality during setup, not assume
it.

## 38.6 Failure modes of the reference

Because the reference defines the frame, its failures are **global** — they corrupt
*every* tool pose, often silently:

- **Patch detachment / slippage.** Adhesive lifts or skin slides; the frame shifts
  with no fault on any single channel. Detection needs **redundancy** — two reference
  sensors whose relative pose should be constant; a sudden change flags slip
  (consistency check, cf. Ch. 27 §27.4 / Ch. 22 state machine).
- **Reference in distortion.** A reference parked near the C-arm, a tool tray, or the
  volume edge imports a biased frame into all measurements; the gradiometer argument
  (§38.4) *inverts* into a gradiometer *injection*. Baseline the reference site
  (Ch. 33 §33.7 empty-volume map).
- **Reference dropout / out of range.** Lose the reference and you lose the frame
  entirely → the only safe response is **flag and hold/​degrade**, never silently
  fall back to the generator frame (which would jump the displayed pose by the full
  patient offset).
- **Reference too far from the target (non-rigid residual).** A sternal patch does
  not capture cardiac motion of an ablation site; the target moves relative to the
  reference, leaving the residual that gating/modeling must remove (T1.4)
  [@borgert2006].
- **Wrong reference / multi-tool confusion.** With several tools and references in a
  multi-catheter procedure (T1.2 of the clinical workflow), mislabeling a reference
  silently re-frames the wrong tool.

## 38.7 Correcting the clinical accuracy chain

This chapter amends the clinical accuracy chain of Ch. 29 §29.7. The "tracking" term
there is really the **relative** error of (38.3) — *tool ⊕ reference*, partially
distortion-cancelled — not the single-sensor CRLB of Ch. 24. The honest budget is
$$
\sigma_\text{clinical}=\sqrt{\underbrace{\sigma_T^2+\sigma_R^2-2\,\rho_D\,\sigma_{T,D}\sigma_{R,D}}_{\text{differential tracking (38.3)}}
+\sigma_\text{reg}^2+\sigma_\text{tip}^2+\sigma_\text{motion}^2},
$$
where $\rho_D$ is the tool–reference distortion correlation (positive, large when
they are close — the gradiometer gain), and $\sigma_\text{motion}$ is now the
*non-rigid, target-relative* residual the reference cannot reach. The reference thus
*raises* the stochastic term but *lowers* the distortion and (bulk-)motion terms —
usually a large net win, and always a term that must be **budgeted explicitly**, not
hidden inside "tracking."

> **Engineering takeaway.** Clinical EMT is **differential**: pose is reported
> relative to a patient-mounted reference, which cancels patient/table bulk motion
> and common generator drift as common-mode (38.2), and — when placed near the tool —
> rejects the common part of distortion like a gradiometer. The price is the
> reference's own added noise (38.3) and a new class of **global, silent failures**
> (slip, dropout, reference-in-distortion) that demand redundancy and flag-and-hold.
> Place the reference as rigidly to the target anatomy and as near the clean working
> volume as workflow allows. Absolute tracking (Parts II–XVIII) is the *engine*;
> the reference frame is what makes it a *clinical* instrument.

---

## Open questions / to verify
- Quantify the **tool–reference distortion correlation** $\rho_D(d)$ vs. separation
  for representative OR distorters (Phase-5 sim of $\mathbf D(\mathbf r)$ field;
  ties Ch. 6 eq. 6.4 and the deferred reflected-impedance/​distortion sims).
- Add primary references for the **dynamic-reference-frame** concept in optical
  surgical navigation (the lineage EMT borrowed) and for **skin-motion artifact**
  magnitudes between a skin patch and underlying bone/organ.
- Source vendor-specific reference implementations (CARTO Ref-Star / back patch;
  EnSite surface patches; superDimension patient sensors; Aurora reference) with
  primary/regulatory documentation (ties Ch. 28, currently conf: med).
- Worked **multi-reference slip-detection** threshold (the constant-relative-pose
  consistency test) tied to the Ch. 27 §27.4 NIS framework.

## Sources cited
- [@borgert2006] external (sternal) + internal (needle) EM reference sensors,
  respiratory motion model, ~94 % correlation, ~4× residual-motion reduction — the
  primary quantitative basis for §38.3/§38.6. Clinical reference-sensor use and the
  lab-vs-in-situ gap from [@franz2014; @yaniv2009]. Frame algebra is standard;
  distortion structure from Ch. 6/27; differential covariance from Ch. 24/25; the
  clinical chain it amends is Ch. 29 §29.7.
