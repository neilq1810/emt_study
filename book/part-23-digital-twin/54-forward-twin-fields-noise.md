# Chapter 54 — The Forward Twin: Differentiable Fields, Noise, and Distorters

> **Status:** DRAFT (awaiting review) · **Part XXIII — Model-Based Engineering & the Digital Twin**
> The foundation layer of the twin: the forward model that everything else stands on. It
> builds the pose → measurement map as three outputs (mean, Jacobian, **covariance**),
> climbs the field-fidelity ladder (Ch. 4/7), insists on differentiability (Ch. 30 §30.6),
> and — the gap-closing core — turns the book's illustrative $\sigma_B$ into an explicit,
> measured, **structured** noise model (Ch. 16/18/25, Ch. 11 §11.6). Feeds identification
> (Ch. 55), the environment twin, and the system twin; governed by the credibility rule of
> Ch. 53. Citation keys resolve to [`../../citations/bibliography.json`](../../citations/bibliography.json).

A twin is only as good as the forward model under it, and an EM tracker is unusually
fortunate here: the physics is a cheap, analytic, differentiable map (Ch. 4) that the book
has already implemented (`emtrack`) and exercised across a dozen simulations. This chapter
makes that implicit forward model an explicit, layered **forward twin** — and uses the
construction to confront the single quietest way a real build fails: trusting the
$\sigma_B = 1\,\text{nT}$ that runs through every CRLB result in this book as if it were a
measured fact rather than a placeholder. The forward twin's discipline is that **every
layer takes a measured input**, and the noisiest of those inputs is the noise model itself.

---

## 54.1 What the forward twin must output

A pose-to-measurement function is not enough. The forward twin must emit **three** things,
because three different consumers need them:
$$
\boldsymbol\theta,\mathbf x\ \longmapsto\
\underbrace{h(\mathbf x;\boldsymbol\theta)}_{\text{mean (solver, Ch.23)}},\quad
\underbrace{\partial h/\partial\mathbf x}_{\text{Jacobian (CRLB, Ch.24)}},\quad
\underbrace{\mathbf R}_{\text{covariance (weighting + uncertainty)}}.
$$
`emtrack` already produces the first two (the `forward_model` and the numerical `jacobian`
behind every CRLB and Monte-Carlo result). The **third — the measurement covariance
$\mathbf R$ — is the one the book has so far supplied as a scalar**, and it is the layer
this chapter rebuilds (§54.4). All three must be consistent: the same model that predicts
the measurement must report how the measurement is weighted (Ch. 23) and how uncertain the
resulting pose is (Ch. 24, §46.6).

## 54.2 The field layer: a fidelity ladder distilled to a fast surrogate

The forward map's heart is the field model, and Ch. 4/7 already give it as a fidelity
ladder:
- **Point dipole** — analytic, instant, the book's default; accurate far from the coil.
- **Finite-loop / multipole correction** — the near-field error of the dipole
  approximation, quantified in sim 1: it falls as $(a/r)^2$, reaching a few percent only
  within a few coil radii (`figures/ch04_dipole_vs_loop_error.png`). This curve *is* the
  field layer's credibility statement — it tells the twin where the cheap model is trustworthy.
- **Full FEA/BEM** — truth, but too slow per evaluation for a solver or a calibration loop.

The forward twin reconciles "fast" with "faithful" the way Ch. 7 §7.2 prescribes:
**characterize the field once with FEA/BEM (or measurement), distil it into a
spherical-harmonic surrogate**, and evaluate that surrogate — millisecond-cheap and
analytic — at run time. The surrogate's coefficients are themselves twin parameters to be
*identified* (Ch. 55 §55.4); the field layer thus spans the whole ladder, choosing fidelity
by the Context of Use (Ch. 53).

## 54.3 The differentiability requirement

The twin must be **differentiable**, not merely evaluable, because gradients power
everything downstream: the LM solver's step (Ch. 23), the Fisher information and CRLB
(Ch. 24), the calibration fit (Ch. 55, eq. 55.1), and the learned-residual co-identification
of the differentiable-model frontier (Ch. 30 §30.6). `emtrack`'s **numerical** Jacobian is
adequate for analysis but slow and noise-prone; the analytic dipole gradient and the
analytically-differentiable harmonic surrogate (§54.2) make the twin both fast and exact —
the precondition for gradient-based calibration and for back-propagating through the solver.
This is why the forward twin and the §30.6 frontier are the same object viewed twice.

## 54.4 The noise layer — turning $\sigma_B$ from a constant into a measured matrix

Here is the chapter's gap-closing core. Every accuracy number in this book — the CRLB map,
the $z^4$ law, the 6-DOF coupling penalty — is computed at an **assumed**
$\sigma_B = 1\,\text{nT}$, a placeholder flagged as such (Ch. 24, RESULTS). A real build that
designs to it discovers a field-referred floor one to two orders worse, and because
accuracy degrades as $z^4$, the usable volume collapses. The forward twin's job is not to
*know* your floor — it cannot — but to **make $\sigma_B$ an explicit, composed, measurable
model output** instead of a buried constant.

**Compose, don't assume.** The measurement covariance is built from the chain the book
already analyzes term by term:
$$
\mathbf R = \underbrace{\mathbf R_\text{sensor}}_{\text{Johnson + 1/}f\text{ / Barkhausen (Ch.14/15)}}
+ \underbrace{\mathbf R_\text{AFE}}_{\text{Ch.16}}
+ \underbrace{\mathbf R_\text{ADC}}_{\text{quant.+jitter (Ch.18)}}
+ \underbrace{\mathbf R_\text{gen}}_{\text{drive current/phase noise (Ch.37)}}
+ \underbrace{\mathbf R_\text{amb}}_{\text{mains/EMI (Ch.17)}},
$$
each term measurable on the bench, each a function of frequency, gain, and integration time
(Ch. 20). The Ch. 25 error budget is exactly this composition done once numerically
(→ 0.84 mm at 95%); the forward twin makes it a *live model input* the CRLB consumes.

**The structure matters, not just the scale (sim 14).** It is tempting to keep a scalar even
after measuring it. But $\mathbf R$ is a **matrix**: channels differ (per-axis signal
strength and AFE noise), and calibration induces **cross-channel correlations** (the
$\mathbf R_a\to\mathbf R_M$ contract of Ch. 11 §11.6). Holding *total* noise power fixed
(equal trace) and merely changing $\mathbf R$'s structure, the Phase-5 forward-twin sim
(`data/forward_twin_noise.json`) shifts the position CRLB **0.076 → 0.067 mm (×0.88, ~12 %)**
and the error-ellipsoid anisotropy from **30 to 37** — proof that a scalar $\sigma_B$, even a
correctly-measured one, throws away accuracy-relevant information. The honest forward twin
therefore composes and measures a **structured $\mathbf R$**, and the CRLB inherits the real
floor *and* its shape. (conf: high — computed; the structure used is representative, the
point is exact.)

## 54.5 The distorter layer

The forward twin optionally includes **modeled distorters** — the eddy/ferromagnetic
secondary-field superposition of Ch. 6, exactly the mechanism the flag-ROC sim (sim 12,
§33.9) used. A distorter is parameterized by its geometry, conductivity, and pose, and the
twin adds its secondary field to the clean prediction. This layer is what lets the twin
*predict* distortion at design time and — once the twin is reconciled against a real room
(the environment-twin chapter) — *detect* it as the divergence between predicted and
measured field. The distorter layer is therefore the bridge from the forward twin to the
environment twin and to detect-and-flag.

## 54.6 Credibility, layer by layer

Ch. 53's rule binds each layer, and usefully each has its **own** validation evidence:
- **Field layer** — validated against FEA/measured field maps (the MMS/V&V verification of
  Ch. 7; the $(a/r)^2$ error budget of sim 1).
- **Noise layer** — validated against **measured noise spectra** and the Monte-Carlo-vs-CRLB
  consistency already shown (sim 4, ~3%); an *unmeasured* noise layer ($\sigma_B$ assumed) is
  the credibility hole that produces the field-trial accuracy collapse.
- **Distorter layer** — validated against measured distortion (the environment-twin chapter,
  §33.9 benchmark).

The forward twin's overall credibility is that of its **weakest validated layer** — and for
most teams that is the noise layer, precisely because $\sigma_B$ is so easy to inherit as a
number rather than earn as a measurement.

> **Engineering takeaway.** The forward twin is `emtrack` made explicit and honest: a fast,
> **differentiable** pose → (mean, Jacobian, **covariance**) map built as a fidelity ladder
> — point dipole → harmonic surrogate distilled from FEA (Ch. 7), validated by the
> $(a/r)^2$ curve (sim 1) — whose gradients power the solver, the CRLB, and calibration
> (Ch. 30 §30.6). Its gap-closing layer is **noise**: the book's $\sigma_B=1\,\text{nT}$ is a
> placeholder, and the twin's discipline is to **compose $\mathbf R$ from the measured chain**
> (sensor + AFE + ADC + generator + ambient, Ch. 16/18/25/37) as a *structured matrix*, not a
> scalar — because at equal total noise power its structure alone shifts the CRLB ~12 % and
> reshapes the error ellipsoid (sim 14). The twin cannot measure your floor for you, but it
> converts gap 2 from a hidden assumption into an explicit, validatable model input — and its
> credibility is only ever that of its weakest *measured* layer.

---

## Open questions / to verify
- Add an **analytic/autodiff Jacobian** to `emtrack` (replacing the numerical one) and
  benchmark the speed/accuracy gain for solver and CRLB (ties §54.3).
- Provide a **worked $\mathbf R$-composition** example: from datasheet/bench numbers for a
  named coil + AFE + ADC, compose $\sigma_B(f, T)$ and propagate to the CRLB — the measured
  counterpart of the 1 nT placeholder (the values are the builder's; the recipe is §54.4).
- Distil a **harmonic surrogate from an FEA field** and report its accuracy vs the dipole
  across the volume (the field-layer credibility evidence, ties Ch. 7).

## Sources cited
- [@raissi2019] differentiable/physics-informed models (the §54.3 gradient requirement and
  the §30.6 tie); [@asme_vv40] per-layer credibility (§54.6). The field ladder is Ch. 4/7
  (sim 1); the noise chain is Ch. 16/18/25/37 and the $\mathbf R_a\to\mathbf R_M$ contract of
  Ch. 11 §11.6 (sim 14); the CRLB consumer is Ch. 24; distorters are Ch. 6/27 (sim 12); the
  credibility frame is Ch. 53; identification of these parameters is Ch. 55. Forward model
  implemented in [`simulations/`](../../simulations) (`emtrack`).
