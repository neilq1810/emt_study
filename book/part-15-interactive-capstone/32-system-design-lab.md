# Chapter 32 — Interactive System-Design Lab

> **Status:** DEEPENED (awaiting review) · **Part XV — Interactive Capstone**
> The companion to Ch. 31: the worked design made *manipulable*. On the web
> edition, the four dashboards described below are embedded live beneath this
> text; in the manuscript they are documented so the reasoning is complete on
> its own. Citation keys resolve to
> [`../../citations/bibliography.json`](../../citations/bibliography.json).

Chapter 31 walked a single end-to-end design and carried the numbers through.
This chapter turns those same equations into instruments you can *play*: four
integrated dashboards, each tying together several chapters through one live
model. They share the validated physics of [`simulations/emtrack`](../../simulations)
(the website's `physics.ts` reproduces it), so every slider moves a number that
the Python suite would agree with — the dashboards are not illustrations bolted
on after the fact, they are the book's equations with the constants exposed.

Use them in the order below: the **system-design dashboard** is the synthesizer
(it *is* Ch. 31 with knobs); the other three zoom into the three places the
design is actually won or lost — the **error budget** across the volume, the
**clinical accuracy chain**, and **distortion with its compensation limit**.

---

## 32.1 System-design dashboard — the synthesizer

The capstone tool. It joins the **system link budget** (Ch. 8, eq. 8.1) to the
**accuracy / rate / latency trilemma** (Ch. 12) in a single view. Six knobs —
generator moment, sensor area-turns, excitation frequency, AFE noise density,
integration time τ, and geometry (PDOP) — drive the field-referred noise σ_B,
the position accuracy σ_pos across the working volume, and the resulting update
rate and latency, with a live pass/fail verdict against the Ch. 31 requirement
(≤ 1 mm at 0.5 m, ≥ 100 Hz, ≤ 20 ms).

**What to try.** Push the integration time τ up: accuracy improves while the
update rate falls and latency rises — the trilemma is a budget, not a slogan.
Then recover the rate by spending generator moment or sensor area-turns instead
(the eq. 8.1 levers). The default state reproduces the Ch. 31 worked design
(σ_B ≈ 1 nT, ≈ 0.69 mm at the far edge, ≈ 8.7 ms latency).

## 32.2 Error-budget dashboard — which class dominates, and where

The Ch. 31 §31.6 error budget, made live. Position error is the root-sum-square
of three independent **error classes** (Ch. 25): stochastic (the CRLB, set by
σ_B), deterministic (tolerance ⊕ calibration residual), and environmental
(post-compensation distortion). The stacked bars show the budget at near, mid,
and far positions.

**What to try.** Halve σ_B and watch the mid-volume total barely move —
calibration and distortion dominate there, so the high-value engineering is in
the field map and compensation, not a quieter amplifier. Only at the far edge
does the z⁴ CRLB take over, and only there do moment and area-turns buy accuracy.
*Attack the dominant term.*

## 32.3 Clinical accuracy-chain dashboard — the tracker is rarely the limit

**Clinical accuracy ≠ sensor accuracy** (Ch. 29 §29.7). The patient-facing error
is the root-sum-square of five terms: tracking, patient-to-image registration,
tip/instrument offset, target motion, and residual distortion. The bars show
each term's *variance share* — what actually drives the total.

**What to try.** Set a 1 mm tracker behind a 2 mm registration and a 0.9 mm tip
lever, then press *halve the tracker*: the clinical number moves from ≈ 2.4 mm to
≈ 2.3 mm. Engineering the sensor is the wrong lever when registration or motion
dominates — the clinical lesson that mirrors the system trilemma.

## 32.4 Distortion & compensation dashboard — and the honest failure mode

Bring a conductor or ferromagnet near the volume and watch the whole error path:
the induced-dipole **distortion fraction** (Ch. 6, eq. 6.4, scaling as
a³r³/d_t³d_s³), the position error it causes, the **post-compensation residual**
(Ch. 27 — compensation buys about 5–10×, never zero), and the **detect-and-flag**
NIS alarm (Ch. 21, 27) that must fire when the residual exceeds the tracking
budget.

**What to try.** Double the distorter's distance and watch the perturbation fall
~8× (the cube law on both legs). Then grow the distorter until even maximum
compensation cannot get the residual under budget — the alarm turns red. The
honest system flags rather than reporting a confidently wrong pose.

---

> **Takeaway.** Chapter 31 proved the design closes on paper; this lab lets you
> feel *why* it closes and where it would break. Every slider is an equation from
> Parts II–X, and every readout traces back to the same physics the simulations
> validate. That is the whole book in your hands at once.

---

## Open questions / to verify
- Back the error-budget dashboard's deterministic/environmental defaults with a
  tolerance Monte Carlo and a measured distortion-residual map (shared with the
  Ch. 31 open question), so those columns stop being illustrative.
- Add a "save/share configuration" feature (URL-encoded slider state) so a design
  point can be cited in the text.

## Sources cited
- System link budget and trilemma from Ch. 8, 12; CRLB from Ch. 24
  [@hummel2005]; error classes/GUM from Ch. 25 [@gum2008]; clinical chain from
  Ch. 29 [@franz2014]; distortion/compensation from Ch. 6, 27 [@cavaliere2023].
