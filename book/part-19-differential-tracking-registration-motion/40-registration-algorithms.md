# Chapter 40 — Registration Algorithms

> **Status:** DEEPENED (awaiting review) · **Part XIX — Differential Tracking, Registration & Motion**
> The methods that *produce* the image→reference transform whose error Ch. 39
> predicts. Together Ch. 39 (theory) and Ch. 40 (algorithms) close the registration
> story the budgets (Ch. 25, 29, 33, 38) depend on. Citation keys resolve to
> [`../../citations/bibliography.json`](../../citations/bibliography.json).

Registration computes the rigid (or non-rigid) transform that maps the preoperative
image into the patient/reference frame (Ch. 38), so a tracked instrument can be drawn
on the image. Chapter 39 told us how *accurate* that transform is at a target (TRE);
this chapter is *how to compute it*. The choice of algorithm is set by **what data
you have**: corresponding **points** (closed-form paired-point), an unlabelled
**surface** (iterative closest point), or a **deforming** anatomy (non-rigid). Each
has a standard, citable solution; each has EMT-specific failure modes because every
input point carries the tracker's spatially-varying, anisotropic localization error
(Ch. 39 §39.4) and correspondences can be wrong. The discipline is the same
throughout: solve optimally, **initialize and robustify**, and validate by the
**predicted TRE at the target — never the FRE** (Ch. 39 §39.3).

---

## 40.1 A taxonomy of the registration problem

| Have | Method | Output | §|
|---|---|---|---|
| Corresponding point pairs (fiducials/landmarks) | **paired-point** closed form | rigid (or similarity) | 40.2 |
| Unlabelled surface / point cloud | **ICP** (iterative) | rigid | 40.3 |
| Deforming anatomy | **non-rigid / deformable** | warp field | 40.4 |

In EMT the two point sets are the fiducials **located in image space** $\{\mathbf
x_i\}$ (CT/MR voxels) and the *same* fiducials **located in tracker space**
$\{\mathbf y_i\}$ — obtained by touching each with a tracked pointer or seating a
sensor at a known marker. The target frame is the **reference sensor** (Ch. 38).

## 40.2 Paired-point rigid registration (closed form)

Given correspondences, minimise the weighted residual
$$
(\mathbf R,\mathbf t)=\arg\min \sum_i w_i\,\lVert \mathbf R\mathbf x_i+\mathbf t-\mathbf y_i\rVert^2,
\qquad \mathbf R\in SO(3).
\tag{40.1}
$$
This is the **orthogonal Procrustes / Kabsch** problem, and it has an *exact*
closed-form solution — no iteration:

1. **Demean** to centroids $\bar{\mathbf x},\bar{\mathbf y}$; form the $3\times3$
   **cross-covariance** $\mathbf H=\sum_i w_i(\mathbf x_i-\bar{\mathbf x})(\mathbf
   y_i-\bar{\mathbf y})^{\!\top}$.
2. **SVD** $\mathbf H=\mathbf U\boldsymbol\Sigma\mathbf V^{\!\top}$ [@arun1987].
3. **Rotation** $\mathbf R=\mathbf V\,\mathrm{diag}(1,1,\det(\mathbf V\mathbf
   U^{\!\top}))\,\mathbf U^{\!\top}$; **translation** $\mathbf t=\bar{\mathbf
   y}-\mathbf R\bar{\mathbf x}$.

The $\det$ term is **not** cosmetic: without it, a noisy or near-degenerate
configuration can drive the bare $\mathbf{VU}^{\!\top}$ to a **reflection**
($\det=-1$) instead of a rotation — Umeyama's correction forces a proper rotation
(and extends the method to recover scale) [@umeyama1991]. The equivalent
**quaternion** formulation (Horn) obtains $\mathbf R$ as the leading eigenvector of a
$4\times4$ matrix built from $\mathbf H$ — numerically robust and reflection-free by
construction [@horn1987]. Use the quaternion form when conditioning is a concern.

**Weighting is where EMT enters.** Under isotropic Gaussian FLE the unweighted
solution is optimal and its error is *exactly* the TRE theory of Ch. 39. But EMT FLE
is **anisotropic and spatially varying** (z⁴ + distortion, Ch. 39 §39.4), so the
proper estimator is **weighted/heteroscedastic** Procrustes with $w_i$ (or a full
$3\times3$ weight matrix) set to the inverse of each fiducial's locally-evaluated FLE
covariance — down-weighting fiducials picked at the volume edge or near metal. This is
the algorithmic counterpart to "register in the clean central field."

## 40.3 Surface-based registration (ICP)

Often there are **no point correspondences** — instead a surface is traced with a
tracked pointer (skin, bone, an organ surface) to be matched against the same surface
segmented from the image. The **Iterative Closest Point** algorithm [@beslmckay1992]:

1. For each data point, find the **closest point** on the model surface (the
   provisional correspondence).
2. Solve the **paired-point** rigid problem (40.2) for those correspondences.
3. Apply, and **repeat** until the residual stops decreasing.

ICP **decreases the error monotonically** and converges — but only to a **local**
minimum, so it needs a **good initialisation** (a coarse paired-point/landmark
prealignment) and fails on symmetric anatomy (a sphere or a smooth tube has many
near-equivalent fits). Standard variants matter in practice: **point-to-plane**
(Chen–Medioni) converges faster by penalising distance along the surface normal;
**trimmed/robust** ICP rejects outliers and tolerates partial overlap;
**normal-space sampling** avoids sliding along flat regions. *EMT specifics:* every
traced point carries the tracker's spatially-varying FLE (Ch. 39), the surface is
partial and noisy, and a distorted patch of the trace biases the whole fit — so
robust variants and clean-field tracing are not optional.

## 40.4 Deformable / non-rigid registration

The body is **not rigid**: breathing, organ shift, soft-tissue deformation, and the
posture difference between the (often breath-hold) scan and the procedure all break
the rigid assumption. Rigid registration then leaves a residual that **grows with the
deformation** and that the TRE theory of Ch. 39 *does not* bound. Non-rigid methods —
**thin-plate splines**, **B-spline free-form deformation**, and **biomechanical/FEM**
models — warp the image to the patient using more degrees of freedom. The cost is
real: many parameters invite **over-fitting**, the error is far harder to validate
than the rigid case, and **regularisation** is essential. In EMT navigation the warp
is frequently driven by *tracked* internal points or by the reference + a respiratory
**motion model** (Ch. 38; T1.4) — the same idea as the EP systems that use a few
magnetically-tracked points to warp an impedance field into real geometry (Ch. 28.5).
Treat deformable registration as powerful but **uncertainty-laden**: pair it with
explicit residual estimates and the detect-and-flag posture (Ch. 27).

## 40.5 Robustness — the single bad correspondence

Least squares (40.1) is **not robust**: one mis-picked fiducial or one wrong ICP
correspondence can dominate the fit and silently corrupt the transform. Defences,
borrowed from the solver chapter (Ch. 23 §23.5):
- **RANSAC** — fit on random minimal subsets, keep the consensus; rejects gross
  outliers.
- **Trimmed least squares / robust M-estimators** (Huber, Ch. 23) — down-weight large
  residuals.
- **Consistency checks** — a fiducial whose post-fit residual is a multiple of the
  expected FLE is flagged, not averaged in.
Because a clinical mis-registration is a *silent, global* error (it shifts every
navigated pose — cf. the reference-frame failures of Ch. 38 §38.6), robustness here is
a safety feature, not a nicety.

## 40.6 The EMT registration workflow & its failure modes

A representative workflow and where it breaks:
- **Fiducial-based:** image-visible markers, located in tracker space with a tracked
  pointer → paired-point (40.2). *Most accurate; needs markers placed before imaging.*
- **Anatomical-landmark-based:** no markers, pick known landmarks → paired-point with
  larger FLE. *Convenient, less accurate (landmark FLE is large).*
- **Surface-trace:** ICP (40.3). *No markers; needs good init and a feature-rich
  surface.*

Failure modes to design against: **wrong correspondence** (fiducial mismatch → gross
error, §40.5); **bad ICP initialisation** (local minimum); **degenerate fiducial
geometry** (collinear/clustered → huge TRE, Ch. 39 eq. 39.1); **distortion at fiducial
sites** (inflates FLE, Ch. 39 §39.4); **deformation between imaging and registration**
(breathing-phase mismatch → rigid residual, §40.4); and **patient motion after
registration** (handled by the reference frame, Ch. 38, or re-register). Validate on
**independent** landmarks and report the **predicted TRE at the target**, never the
FRE.

> **Engineering takeaway.** Registration algorithms come in three families matched to
> the data: **closed-form paired-point** (SVD/quaternion — optimal and instant given
> correspondences, with the $\det$ reflection fix mandatory), **ICP** (for surfaces —
> monotone but local, needs initialisation), and **deformable** (for non-rigidity —
> powerful but hard to bound). In EMT, weight every point by its spatially-varying
> FLE, **robustify** against the single bad correspondence (a silent global error),
> and judge the result by the predicted TRE of Ch. 39 — closing the registration loop
> that the clinical accuracy chain (Ch. 29 §29.7, Ch. 38) rests on.

---

## Open questions / to verify
- Phase-6 **registration playground** tool: paired-point vs. ICP on a configurable
  fiducial set, showing the resulting transform, FRE, and the *predicted TRE map*
  (Ch. 39 eq. 39.1) — directly visualising the FRE⊥TRE lesson.
- Add primary citations for **point-to-plane ICP** (Chen–Medioni), **robust/trimmed
  ICP**, and a **deformable-registration error** reference to firm up §40.3/§40.4.
- Worked **anisotropic weighted Procrustes** example using an EMT FLE map
  (CRLB ⊕ distortion), quantifying the accuracy gain over unweighted.
- Source EMT-specific **landmark-vs-fiducial FLE** values and a clinical
  registration-failure-rate dataset.

## Sources cited
- [@arun1987] SVD paired-point solution; [@umeyama1991] reflection/​scale correction;
  [@horn1987] quaternion closed form; [@beslmckay1992] ICP for surfaces. Robust
  estimation (Huber) from Ch. 23; anisotropic/spatially-varying FLE and the
  TRE/​FRE theory these algorithms feed from Ch. 39; the reference target frame from
  Ch. 38; deformable/motion link to T1.4 and the EP field-warp of Ch. 28.5.
