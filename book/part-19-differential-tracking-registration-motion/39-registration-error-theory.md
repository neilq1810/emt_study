# Chapter 39 — Registration Error Theory: FLE, FRE & TRE

> **Status:** DEEPENED (awaiting review) · **Part XIX — Differential Tracking, Registration & Motion**
> The mathematical backbone of registration accuracy, and the chapter that converts
> the vague "registration error" of the clinical accuracy chain (Ch. 29 §29.7,
> Ch. 38) into a *predictable, designable* quantity. Citation keys resolve to
> [`../../citations/bibliography.json`](../../citations/bibliography.json).

Registration — aligning the preoperative image to the patient/reference frame
(Ch. 38) — is, by the book's own budgets, **often the dominant clinical error**
(Ch. 25, 29, 33). Yet every prior mention has treated it as a *number you are handed*.
It is not: registration error has a **theory** that predicts its magnitude at any
target from the fiducial geometry and the localization noise, and that theory carries
a result so counter-intuitive, and so routinely violated in the operating room, that
it must be stated plainly: **the registration-quality number the system displays
(FRE) is statistically uncorrelated with the error you actually care about (TRE)**
[@fitzpatrick2009]. This chapter develops the three errors (FLE → FRE → TRE), the
Fitzpatrick prediction formula, that uncorrelatedness, and — the reason it lives in
*this* book — why electromagnetic tracking makes the localization error
**spatially varying and anisotropic**, and the clinical geometry (superficial
fiducials, deep targets) inherently unfavorable.

---

## 39.1 Three distinct errors — do not conflate them

Point-based registration aligns $N$ corresponding **fiducial** pairs — the same
landmarks located in image space $\{\mathbf x_i\}$ and in physical/tracker space
$\{\mathbf y_i\}$ — by the rigid transform $(\mathbf R,\mathbf t)$ minimizing
$\sum_i \lVert \mathbf R\mathbf x_i+\mathbf t-\mathbf y_i\rVert^2$ (the Procrustes/
Horn solution; the *algorithms* are Ch. 40). Three errors arise, and clinicians and
engineers routinely confuse them:

- **FLE — Fiducial Localization Error.** The error in *locating each fiducial* (image
  voxel pick ⊕ tracker pose error ⊕ distortion at that point). It is the **input**
  noise, ~zero-mean, RMS magnitude $\text{FLE}$. *You never see it directly.*
- **FRE — Fiducial Registration Error.** After fitting, the **RMS residual distance**
  between the registered fiducials, $\text{FRE}^2=\frac1N\sum_i\lVert\mathbf R\mathbf
  x_i+\mathbf t-\mathbf y_i\rVert^2$. It is **measurable** — and it is what the system
  displays.
- **TRE — Target Registration Error.** The registration error evaluated at a
  **target** point $\mathbf r$ that is *not* a fiducial — the actual lesion, ablation
  site, or vessel. It is **what you care about** and **cannot measure**
  intraoperatively.

The entire clinical misuse of registration flows from treating the *measurable* FRE
as a proxy for the *unmeasurable, decision-relevant* TRE.

## 39.2 The TRE prediction formula

Fitzpatrick, West & Maurer derived the expected TRE at a target, to first order in
FLE, for $N$ fiducials [@fitzpatrick1998]:
$$
\big\langle \text{TRE}^2(\mathbf r)\big\rangle \;\approx\;
\frac{\text{FLE}^2}{N}\left(1+\frac{1}{3}\sum_{k=1}^{3}\frac{d_k^2}{f_k^2}\right),
\tag{39.1}
$$
where, for the fiducial configuration's three **principal axes** $k$:
- $f_k$ = RMS distance of the **fiducials** from principal axis $k$ (the configuration
  spread along/around that axis), and
- $d_k$ = distance of the **target** $\mathbf r$ from principal axis $k$.

Read it term by term — this is the whole design guidance for registration:
- **TRE falls as $1/\sqrt{N}$:** more fiducials help, but only as a square root.
- **Minimum at the centroid:** with $d_k=0$, $\langle\text{TRE}^2\rangle=\text{FLE}^2/N$.
- **TRE grows as the target moves off the fiducial configuration**, and *catastrophically
  along a poorly-spread axis*: the $d_k/f_k$ ratios punish a target that is far from
  the centroid **in the direction the fiducials are not spread out**. Collinear or
  coplanar fiducials make some $f_k\to0$ → that axis is nearly unconstrained for
  rotation → TRE explodes for any target off it.
- **Configuration is destiny:** spread the fiducials widely in all three dimensions
  and *surround* the target.

The companion result for the *measurable* quantity is
$\langle\text{FRE}^2\rangle\approx\text{FLE}^2\,(1-2/N)$ [@fitzpatrick1998] — so FRE
**under**-reports FLE for small $N$ and only approaches it as $N\to\infty$.

## 39.3 The dangerous result: FRE does not predict TRE

Here is the result every operator should know and most do not. Fitzpatrick proved, to
first order, that **FRE and TRE are statistically uncorrelated** — *all* measures of
goodness-of-fiducial-fit are independent of the true target error
[@fitzpatrick2009]. A small displayed FRE gives **no information** about TRE for that
patient.

The intuition: with $N$ fiducials and a 6-DOF rigid fit, the FLE noise projects into
two **orthogonal** subspaces — the part that survives as fit *residual* (→ FRE) and
the part that perturbs the *transform parameters* (→ TRE). They are independent. Worse,
a *low* FRE with few fiducials often signals **over-fitting**: the transform has
absorbed the noise into the parameters (small residual, *large* TRE). So a reassuring
"registration error: 0.8 mm" on screen can sit atop a multi-millimetre error at the
lesion — and a larger FRE does not mean a worse registration.

> **The rule:** never accept or rank a registration by its FRE. Judge it by the
> **predicted TRE at the actual target** (eq. 39.1), and design the fiducial
> configuration to minimize that — not the residual you happen to be shown.

## 39.4 Anisotropic and spatially varying FLE — the EMT reality

Equation (39.1) assumes isotropic, homogeneous FLE. **In electromagnetic tracking it
is neither**, which is exactly why TRE theory belongs in this book rather than only in
a surgical-navigation text. The tracker-space half of FLE is the system's own pose
error, and that error is (Parts IV–IX):
- **Spatially varying** — it grows toward the working-volume edge as the z⁴ CRLB
  (Ch. 24) and balloons near any distorter (Ch. 6, eq. 6.4). A fiducial picked at the
  volume edge carries far more FLE than one near the generator.
- **Anisotropic** — the pose covariance ellipsoid is elongated (the radial/field
  direction is typically worse), so FLE has direction-dependent magnitude.

The isotropic formula therefore *understates* TRE wherever fiducials sit in noisy or
distorted regions. The proper treatment is the **weighted/anisotropic** generalization
(heteroscedastic FLE → weighted Procrustes, target-dependent TRE), in which each
fiducial is weighted by the inverse of its (spatially evaluated) FLE covariance
(conf: med — the anisotropic extension is established in the registration literature;
the EMT-specific FLE map ties to Ch. 24/27). Practical consequence: **register using
fiducials in the clean, central field**, down-weight those near edges/metal, and
*predict* TRE with the local FLE, not a single nominal number.

## 39.5 The clinical geometry is inherently unfavorable

Combine eq. (39.1) with the realities of the body and EMT loses on every factor —
which is *why* clinical registration is hard:
- **Fiducials are superficial, targets are deep.** Skin/surface fiducials can only be
  placed where anatomy allows — often **clustered on one aspect** (the anterior chest,
  one side of the head), giving a small spread $f_k$ along the body axis. The target
  (a lung lesion, an ablation site, a deep vessel) sits **far from that surface**,
  i.e. large $d_k$ along the *weakest* axis. Both effects multiply the dominant term in
  (39.1).
- **FLE is large and inhomogeneous** in the EMT volume (§39.4).
- **The reference sensor is the anchor** (Ch. 38): registration computes the
  image→reference transform, so its TRE **propagates into every navigated pose** — the
  $\sigma_\text{reg}$ term of the Ch. 29/38 clinical chain *is* this TRE.

**Worked example (ENB-like).** $N=4$ chest-surface fiducials, well spread in the
coronal plane ($f_1=f_2\approx80$ mm) but flat through the chest ($f_3\approx20$ mm);
$\text{FLE}\approx1.5$ mm (EM localization incl. mild distortion). The target is a
lung lesion ~100 mm **deep** (off the fiducial plane), with offsets
$d_1=d_2\approx40$ mm, $d_3\approx100$ mm. Then
$$
\sum_k \frac{d_k^2}{f_k^2}=\Big(\tfrac{40}{80}\Big)^2+\Big(\tfrac{40}{80}\Big)^2+\Big(\tfrac{100}{20}\Big)^2
=0.25+0.25+25=25.5,
$$
$$
\langle\text{TRE}^2\rangle=\frac{1.5^2}{4}\Big(1+\tfrac{25.5}{3}\Big)=0.5625\times9.5=5.34\ \text{mm}^2
\;\Rightarrow\;\text{TRE}\approx2.3\ \text{mm},
$$
versus a centroid TRE of only $\text{FLE}/\sqrt N=0.75$ mm — a **3×** penalty driven
almost entirely by the $d_3/f_3=5$ term (deep target, thin through-chest spread).
Meanwhile the displayed $\text{FRE}\approx\text{FLE}\sqrt{1-2/N}=1.5\sqrt{0.5}\approx
1.06$ mm — small, reassuring, and **uninformative** about the 2.3 mm reality at the
lesion. This single example is the ENB accuracy story (Ch. 29) in one equation.

## 39.6 Reducing TRE — the design levers

From (39.1), in priority order:
1. **Surround the target and spread fiducials in 3-D** — maximize every $f_k$
   (no coplanar/collinear sets), minimize $d_k$ (place fiducials *near and around* the
   target where anatomy permits). This dominates everything else.
2. **Add fiducials** ($1/\sqrt N$) — useful but sublinear; configuration beats count.
3. **Reduce FLE** — localize in the **clean central field**, away from edges and metal
   (Ch. 6, 24, 27); use larger/averaged fiducial measurements.
4. **Weight by FLE** — down-weight noisy/distorted fiducials (§39.4).
5. **Accept/reject on predicted TRE at the target**, never on FRE (§39.3).

> **Engineering takeaway.** Registration accuracy is **predictable and designable**:
> TRE at a target follows eq. (39.1) from the fiducial geometry and the localization
> noise — falling as $1/\sqrt N$, minimized at the centroid, and exploding for deep
> targets off a poorly-spread fiducial set. The measured FRE the system shows is
> **uncorrelated with TRE** and must never be used as a confidence indicator. In EMT
> the localization error feeding FLE is itself spatially varying and anisotropic
> (z⁴ + distortion), and the clinical geometry (superficial fiducials, deep targets)
> is inherently adverse — so registration is hard for structural reasons, and the
> remedy is fiducial *configuration*, clean-field localization, and TRE-based
> acceptance, not a comforting FRE readout.

---

## Open questions / to verify
- Add the **anisotropic/weighted TRE** generalization with a primary citation
  (Wiles/Danilchenko & Fitzpatrick general first-order approach) and a worked
  EMT example using a spatially-evaluated FLE map (ties Ch. 24 CRLB + Ch. 27
  distortion).
- Phase-5 sim: generate the **FLE field** over the working volume (CRLB ⊕ distortion)
  and propagate eq. (39.1) into a **TRE map** for a representative fiducial set —
  a strong candidate Phase-6 "registration-accuracy explorer" tool.
- Source primary references for **surface (ICP) registration** TRE behaviour and for
  **deformable** registration error (forward link to Ch. 40 and the motion chapter).
- Quantify the EM-specific FLE budget for common fiducial types (skin markers,
  anatomical landmarks, touch-point digitization) with measured values.

## Sources cited
- [@fitzpatrick1998] TRE prediction formula (eq. 39.1) and ⟨FRE²⟩=FLE²(1−2/N).
  [@fitzpatrick2009] FRE and TRE are uncorrelated — the displayed-FRE misuse to
  correct. EMT-specific FLE (spatially varying/anisotropic) from Ch. 24/27; the
  reference-frame anchor from Ch. 38; the clinical chain this sizes is Ch. 29 §29.7;
  registration *algorithms* follow in Ch. 40.
