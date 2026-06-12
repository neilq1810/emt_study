# Chapter 43 — Coordinate-Frame Management & the System Transform Graph

> **Status:** DEEPENED (awaiting review) · **Part XIX — Differential Tracking, Registration & Motion**
> Closes Part XIX. The connective tissue beneath the reference frame (Ch. 38),
> registration (Ch. 39–40), and the integration layer (Ch. 35): the discipline of
> managing the many coordinate frames a clinical EMT system juggles, and propagating
> uncertainty through the chain that links them. Citation keys resolve to
> [`../../citations/bibliography.json`](../../citations/bibliography.json).

Every preceding chapter introduced a coordinate frame — the generator frame the
tracker measures in (Parts II–IX), the sensor and **tip** frames (Ch. 14–15), the
**patient reference** frame (Ch. 38), the **image** frame registration maps to
(Ch. 39–40), and the **robot** frames of image-guided therapy (Ch. 29). A navigated
pose is not any one of these; it is a **composition** of several, each from a
different source, with a different update rate, and a different uncertainty. Getting
that composition right — and disciplined about conventions, timestamps, ownership, and
error propagation — is where a large share of real integration bugs and silent
clinical errors live. This chapter formalises the **system transform graph**, the
properties of each edge, the convention pitfalls, the uncertainty propagation that
*is* the clinical accuracy chain, and the frame-management failure modes.

---

## 43.1 The frame zoo and the transform graph

A clinical system carries, at minimum:

| Frame | Meaning |
|---|---|
| **G** | field-generator (lab) frame — what the tracker natively measures in |
| **T** | tracked-sensor frame; **tip** — the instrument tip, offset from T (Ch. 14.2, 15.2) |
| **R** | patient **reference** frame (Ch. 38) |
| **I** | **image** frame (CT/MR voxel space) |
| **Rob** | robot base / end-effector frames (Ch. 29) |
| **D** | display frame |

Each ordered pair is related by a rigid transform $\mathbf T_A^B\in SE(3)$. The frames
are **nodes** and the known transforms are **edges** of a **transform graph**;
navigation is finding and composing a **path** through it. Composition and inversion
are the only operations:
$$
\mathbf T_A^C=\mathbf T_B^C\,\mathbf T_A^B,\qquad \mathbf T_B^A=(\mathbf T_A^B)^{-1}.
$$
To draw the instrument tip on the CT, compose the path **tip → T → G → R → I**:
$$
\mathbf T_\text{tip}^{I}
=\underbrace{(\mathbf T_I^{R})^{-1}}_{\text{registration}}\;
\underbrace{(\mathbf T_G^{R})^{-1}}_{\text{measured}}\;
\underbrace{\mathbf T_G^{T}}_{\text{measured}}\;
\underbrace{\mathbf T_T^{\text{tip}}}_{\text{calibration}} .
\tag{43.1}
$$
Read it right to left: the tip offset (calibration) takes the sensor to the tip; two
*measured* transforms take the tip into the reference frame (the differential
measurement of Ch. 38, eq. 38.1); the *registration* takes it into the image. Three
different kinds of knowledge, chained.

## 43.2 Every edge is different — the key engineering insight

The edges of (43.1) are not interchangeable; they differ in source, rate, and
uncertainty, and a robust system treats each accordingly:

| Edge | Source | Update rate | Uncertainty | Character |
|---|---|---|---|---|
| $\mathbf T_G^{T}$ | tracker measurement | real-time (100s Hz) | CRLB ⊕ distortion (Ch. 24, 42) | dynamic |
| $\mathbf T_G^{R}$ | tracker measurement | real-time | CRLB ⊕ distortion | dynamic (patient moves) |
| $\mathbf T_T^{\text{tip}}$ | tool/factory calibration | static | tolerance (Ch. 15.2) | static per tool |
| $\mathbf T_I^{R}$ | registration | once / on re-reg | **TRE** (Ch. 39) | static until re-registered |
| $\mathbf T_{Rob}^{G}$ | hand-eye calibration | static | calibration | static |

A single navigated pose therefore mixes **real-time measured** transforms, **static
calibrations**, and a **registration** — different rates and different error sources
composed into one number. The implications (time-alignment, ownership, propagation)
fill the rest of the chapter.

## 43.3 Conventions — where the silent gross errors hide

Most frame bugs are not arithmetic; they are **convention mismatches** that produce a
confidently wrong (often mirrored or rotated) pose:

- **Direction/active-vs-passive:** does $\mathbf T_A^B$ map A-points-into-B or
  represent A's *pose* in B? Fix one convention system-wide.
- **Rotation representation:** matrix vs **quaternion** vs Euler. The **Hamilton vs
  JPL quaternion** ambiguity is a notorious sign-flip bug (Ch. 21 §21.4, Solà
  [@sola2017]); Euler angles need a stated order and risk gimbal lock.
- **Handedness & units:** right- vs left-handed, mm vs m.
- **Medical-image axes:** DICOM uses the **LPS** (Left-Posterior-Superior) patient
  coordinate system while many toolkits use **RAS** — a left/right or
  anterior/posterior flip if confused, i.e. a *mirror-image* navigation error. This is
  an EMT-integration trap distinct from generic robotics.
- **Time:** every *dynamic* transform carries a **timestamp** (Ch. 10, 35); composing
  transforms sampled at different instants is wrong and must be time-aligned (Ch. 21,
  35). Disciplined coordinate-frame bookkeeping is the navigation-domain version of
  the inertial-navigation frame discipline of Groves [@groves2013].

## 43.4 Ownership and a single source of truth

Who computes each edge? A clean architecture assigns **one owner per edge** — the pose
engine owns $\mathbf T_G^{T},\mathbf T_G^{R}$; the registration module owns $\mathbf
T_I^{R}$; the tool database owns $\mathbf T_T^{\text{tip}}$ — and routes all of them
through **one transform-graph service** that composes paths on demand with
time-alignment (the `tf`/`tf2` pattern, Ch. 35 §35.3). The anti-pattern is each module
keeping its **own copy** of a transform: copies drift out of sync, and two parts of the
UI disagree about where the tool is. The data contract of Ch. 11 §11.6 / Ch. 35 is the
formalisation: every streamed pose must carry its **frame ID, timestamp, and
covariance** — without all three it cannot be safely composed.

## 43.5 Uncertainty propagation — the chain *is* the clinical accuracy budget

Each edge has a covariance; the composed transform's covariance is the first-order sum
of the edge covariances mapped through the SE(3) **adjoints** (the Jacobians of
composition). To first order, and treating the edges as independent, the position
covariance at the tip in image space is
$$
\boldsymbol\Sigma_\text{tip}^{I}\approx
\boldsymbol\Sigma_\text{reg}(\text{TRE})+\boldsymbol\Sigma_\text{track}^{R}
+\boldsymbol\Sigma_\text{tip-cal}+\dots
$$
— which is **exactly the clinical accuracy chain** of Ch. 29 §29.7 / Ch. 38 §38.7,
now recognised as *uncertainty propagation through the transform graph*. Two
structural lessons fall out:
- **Lever-arm amplification.** A rotation error in an *early* edge maps to a position
  error downstream proportional to the **distance** to the point of interest — the tip
  lever-arm (Ch. 15.2), the TRE target-distance term (Ch. 39 eq. 39.1), and the
  $d_k/f_k$ geometry all being the same effect. **Long chains with lever arms amplify
  small angular errors into large position errors.**
- **The weakest edge dominates.** Registration TRE (mm-scale, Ch. 39) usually swamps
  the sub-mm tracking edge — so, as ever, *attack the dominant edge* (Ch. 12, 29),
  which the graph view makes obvious by inspection.

**Worked path.** With registration TRE ≈ 2.0 mm (Ch. 39), reference-differential
tracking ≈ 0.7 mm (Ch. 38 eq. 38.3), and a 0.9 mm tip lever-arm contribution
(Ch. 15.2), the composed tip-in-image error is
$\sqrt{2.0^2+0.7^2+0.9^2}\approx 2.3$ mm — the same clinical number (Ch. 29 §29.7),
derived here as a graph path so that *which edge to improve* is unambiguous (the
registration edge).

## 43.6 Failure modes of frame management

Frame management is a top integration-bug class precisely because its failures are
**silent and global**:
- **Wrong frame reported** — e.g. a pose left in the **generator** frame instead of the
  **reference** frame, so the entire bulk patient offset reappears (Ch. 38); or a tool
  mislabeled.
- **Convention mismatch** — Hamilton/JPL, LPS/RAS, active/passive → mirror or rotation
  flips that look plausible until something is obviously on the wrong side.
- **Stale transform** — using an old registration after the patient moved (or composing
  mismatched timestamps): the chain is internally consistent but temporally wrong.
- **Disconnected graph** — registration not yet done, or the **reference lost**
  (Ch. 38 dropout): there is *no path* from tool to image → the system must **flag**,
  never invent one.
- **Unit/handedness errors** — mm/m, left/right handed: gross, usually caught early,
  occasionally not.
- **Calibration drift in an edge** — tip-offset wear, hand-eye drift (Ch. 26 §26.6).

The defenses are the book's recurring ones, applied to frames: a single owned source
of truth (§43.4), mandatory frame-ID + timestamp + covariance on every pose (§43.4),
**detect-and-flag** on a broken/stale/disconnected edge (Ch. 27 §27.4, Ch. 38), and
consistency checks (a constant-by-construction transform that changes flags a fault).

> **Engineering takeaway.** A navigated pose is a **composition** of measured,
> calibrated, and registered transforms through the system **transform graph**
> (eq. 43.1) — each edge with its own rate, source, and uncertainty. Manage it with a
> single owned source of truth, rigid system-wide **conventions** (quaternion
> handedness, LPS/RAS, units, direction), **timestamps** on every dynamic edge, and
> first-order **uncertainty propagation** that reproduces — and explains — the
> clinical accuracy chain, lever-arm amplification and weakest-edge dominance included.
> Frame errors are silent and global; treat a broken or stale edge like a lost
> reference — **flag, never fabricate**.

---

## Open questions / to verify
- Add a worked **SE(3) covariance-propagation** example with explicit adjoints
  (turn §43.5 from first-order narrative into a numeric covariance through (43.1)),
  tying Ch. 24/38/39 covariances.
- Provide a concrete **frame-graph schema** (frame IDs, conventions, the tf-tree) as a
  reference figure and a worked OpenIGTLink/`tf` mapping (ties Ch. 35 §35.3).
- Add primary references for **hand-eye calibration** (robot↔generator) and for the
  DICOM patient coordinate system, to firm up §43.3/§43.5.
- A Phase-6 tool: an interactive **transform-graph explorer** showing the path
  composition and the propagated uncertainty for a configurable chain.

## Sources cited
- [@sola2017] quaternion kinematics and the Hamilton/JPL convention trap (§43.3).
  [@groves2013] coordinate-frame discipline and frame transformations in navigation
  (§43.3/§43.5). The transform chain composes the differential measurement of Ch. 38,
  the tip calibration of Ch. 14–15, and the registration/TRE of Ch. 39; the
  uncertainty propagation *is* the clinical chain of Ch. 29 §29.7; the integration/
  `tf` realisation is Ch. 35 §35.3.
