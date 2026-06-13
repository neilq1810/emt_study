# Chapter 13 — Sensor Physics & Geometries

> **Status:** DEEPENED (awaiting review) · **Part IV — Sensor Engineering**
> Opens Part IV. Builds on Ch. 5 (coupling), Ch. 9 (sensor overview). Hands off
> to Ch. 14 (construction/technologies) and Part VIII (why DOF is lost).
> Citation keys resolve to [`../../citations/bibliography.json`](../../citations/bibliography.json).

The sensor is where the magnetic field becomes a number. This chapter establishes
the two fundamental sensing principles, then derives the geometry → degrees-of-
freedom mapping that determines whether a sensor reports 5-DOF or 6-DOF — the
single most consequential sensor-architecture choice in EMT. Construction
technologies (wire-wound, PCB, and solid-state **AMR/GMR/TMR**) are Ch. 14;
noise and tolerance are Ch. 15.

---

## 13.0 Two sensing principles: induction vs. direct field

Everything a sensor can do follows from *what physical quantity it transduces*.

- **Induction pickups (search coils).** A coil transduces the *rate of change*
  of flux: $\varepsilon = -N_sA_s\,\hat{\mathbf n}_s\!\cdot\!\dot{\mathbf B}$
  (Ch. 5, eq. 5.1). Output is proportional to $\omega B$, so sensitivity rises
  with frequency and **collapses to zero at DC**. Coils are passive, simple,
  cheap, robust, and have an extremely wide dynamic range and clean noise
  physics (Johnson noise of the winding, Ch. 15). They are the natural — and
  clinically dominant — sensor for **AC** architectures, and "miniature
  inductive coils are the gold standard in clinical settings" for passive
  field sensing (conf: high) [@yaniv2009; @lenz2006].
- **Direct field sensors.** Hall, fluxgate, and the magnetoresistive family
  (AMR/GMR/**TMR**) transduce $B$ *itself*, with a **flat response down to DC**.
  This is exactly what a **pulsed-DC** architecture needs (it samples a static
  field after eddy-current settling, Ch. 6 §6.4, where a coil's EMF would be
  zero), and what enables chip-scale, array, and ultra-miniature sensing
  (Ch. 14.3). The cost is a higher and more complex noise floor — notably **1/f
  (flicker) noise** that dominates at the low frequencies EMT cares about
  [@lenz2006; @davies2021].

The taxonomy of all magnetic sensor types and the field/vector distinction is
laid out comprehensively by Lenz & Edelstein [@lenz2006]; we specialize it to
tracking. The induction-vs-field choice ripples through the entire system: it
sets the viable excitation scheme (Ch. 8), the AFE design (Part V), and the
calibration strategy (Part X).

## 13.1 Single-element sensing and the roll ambiguity (5-DOF)

Consider one sensing element with axis $\hat{\mathbf n}_s$. Whether a coil
(measuring $\dot{\mathbf B}\!\cdot\!\hat{\mathbf n}_s$) or a field sensor
(measuring $\mathbf B\!\cdot\!\hat{\mathbf n}_s$), it reports only the **scalar
projection of the field onto its own axis**. From a transmitter triad it
therefore yields a 3-vector (one number per transmit axis) — enough to determine

- **position** $\mathbf r$ (3 DOF), and
- the **direction** of its own axis $\hat{\mathbf n}_s$ (2 DOF: a unit vector
  has two free angles),

for a total of **5 DOF**. What it *cannot* sense is **rotation about its own
axis** $\hat{\mathbf n}_s$. The argument is exact: rolling the body by angle
$\varphi$ about its own axis replaces the orientation $\mathbf R\to\mathbf R\,\mathbf R_{\hat{\mathbf n}_s}(\varphi)$,
but since $\mathbf R_{\hat{\mathbf n}_s}(\varphi)\,\hat{\mathbf n}_s=\hat{\mathbf n}_s$,
the lab-frame axis $\mathbf R\hat{\mathbf n}_s$ is **unchanged**, so every
measurement $(\mathbf R\hat{\mathbf n}_s)\!\cdot\!\mathbf B_i$ is unchanged. The
roll direction is therefore an exact **null space of the orientation Jacobian**
($\partial(\text{measurement})/\partial\varphi\equiv0$): $\mathbf J$ is
rank-deficient by one and the CRLB for roll is infinite (Ch. 24 §24.1). This is
the **roll ambiguity** — geometric, not a processing failure; no algorithm
recovers information the sensor never encoded. The observable state is exactly
$(\mathbf r,\ \text{2 angles of }\hat{\mathbf n}_s)$ — five numbers. A single
straight coil or a single MR die is intrinsically a **5-DOF** sensor
[@yaniv2009]. The null and its dual-coil fix are sketched in
`figures/ch13_roll_null.png`.

> **Why this matters clinically.** A 5-DOF sensor fully localizes the *tip and
> pointing direction* of a needle or catheter — which is all many procedures
> need — and can be made far smaller than a 6-DOF sensor. The smallest medical
> sensors (sub-millimeter diameter, e.g. NDI's micro 5-DOF coil ~0.3 mm dia.)
> are 5-DOF for exactly this reason [@ndi_aurora]. (conf: med — vendor-reported
> dimension.)

## 13.2 Orthogonal triad sensing (6-DOF)

To recover the sixth DOF (roll), the sensor must measure more than one field
projection at the same point. The classic solution is the **orthogonal triad**:
three sensing elements with mutually perpendicular axes, reconstructing the full
local field *vector* $\mathbf B$ (not just one projection). Combined with a
transmitter triad, this yields the full $3\times3$ coupling matrix $\mathbf M$
(Ch. 5, eq. 5.6), whose factorization $\mathbf M=(N_sA_s)\mathbf R^{\top}\mathbf K(\mathbf r)$
exposes the complete orientation $\mathbf R\in SO(3)$ — all **6 DOF**. This is
the Raab et al. template [@raab1979] and the basis of most 6-DOF systems.

The penalty is **size**: three orthogonal coils (or three MR dies on orthogonal
faces) cannot be made as small as one, so 6-DOF sensors are bulkier than 5-DOF —
the central miniaturization tension of Ch. 14.

## 13.3 Non-orthogonal, dual-element, and over-determined arrangements

Strict orthogonality is a convenience, not a requirement. Practical variants:

- **Two askew 5-DOF elements → 6-DOF.** Two elements with body-frame axes
  $\hat{\mathbf n}_1,\hat{\mathbf n}_2$ separated by angle $\theta$ resolve roll
  because rolling about $\hat{\mathbf n}_1$ now *moves* $\hat{\mathbf n}_2$ (only a
  vector along the roll axis is invariant, §13.1), so the second element's
  projections vary with roll. The sensitivity scales with the component of
  $\hat{\mathbf n}_2$ perpendicular to the roll axis — i.e. **∝ sin θ** — so roll
  observability is **zero at $\theta=0$** (parallel axes ⇒ degenerate back to
  5-DOF) and **maximal at $\theta=90°$**. A Phase-5 simulation confirms this
  exactly: the normalized roll observability (smallest singular value of the
  orientation Jacobian) rises from $0.0$ at $0°$ through $0.55$ at $45°$ to $1.0$
  at $90°$, tracking $\sin\theta$ (`figures/ch13_dual_coil_observability.png`,
  `data/dual_coil_obs.json`). This is the rigorous basis for the patent claim that
  "larger angles give better accuracy" [@schneider2000]; in a catheter the two
  coils are tilted within the wall to maximize $\theta$ while staying thin.
  (conf: high — derived and numerically validated.)
- **Spatially separated 5-DOF pair.** Two 5-DOF sensors at known separation
  along a rigid shaft jointly determine 6-DOF of a base frame — used when the
  payload region must stay thin (conf: med — catheter shape/pose literature).
- **Over-determined (>3 elements).** Extra elements add redundancy for noise
  averaging and outlier rejection (Ch. 23), at the cost of size/wiring. The
  decode becomes a least-squares fit rather than a square inversion.

Non-orthogonality is handled by the calibration and forward model (the coupling
matrix simply uses the true element axes); it is *not* an error to be removed but
a design degree of freedom. The conditioning consequences (some geometries
resolve roll more robustly than others) are quantified in Ch. 24.

## 13.4 Hybrid sensors (EM + IMU)

A small **IMU** (MEMS gyro + accelerometer) co-located with the EM sensor
provides high-rate, low-latency orientation (and short-term position via double
integration) that is *complementary* to EM: the IMU is immune to field
distortion and has low latency but drifts; EM is drift-free and absolute but
slower and distortion-prone (Ch. 6). Fusing them (Ch. 21) yields a sensor that
is simultaneously fast, drift-free, and robust to momentary distortion — and can
*detect* distortion as an EM/IMU disagreement. Hybridization can also resolve a
5-DOF coil's roll using the IMU, effectively buying the sixth DOF without a
second coil. This is a major theme of the research frontier (Part XIII).

## 13.5 The geometry → DOF map (summary)

| Sensing elements | DOF | Mechanism | Typical use |
|---|---|---|---|
| 1 element | 5 | position + axis direction; roll lost | needles, microcatheters (smallest) |
| 2 askew elements | 6 | second axis resolves roll | catheters needing full orientation |
| 2 separated 5-DOF | 6 (of a frame) | baseline resolves roll | thin shafts, shape sensing |
| Orthogonal triad | 6 | full local field vector | rigid instruments, the classic template |
| 1 element + IMU | 6 | IMU supplies roll, EM supplies absolute | distortion-robust, low-latency hybrids |

The rule to remember: **DOF is set by how many independent field projections you
measure at (or near) a point.** One projection → 5-DOF; a full vector → 6-DOF.
Everything else is packaging and conditioning.

---

## Open questions / to verify
- ✅ **Resolved:** the "two askew coils → 6-DOF, accuracy ∝ sin θ" claim is now
  derived (§13.3) and numerically validated (`sim_dual_coil_obs`,
  `figures/ch13_dual_coil_observability.png`), and grounded in the Schneider
  dual-coil patent [@schneider2000]. The roll-ambiguity demonstration is the
  Phase-6 *5-DOF vs 6-DOF* and *3-D sensor-orientation* tools.
- Confirm the smallest-sensor dimension figures against a current NDI datasheet
  rather than the marketing page [@ndi_aurora].

## Sources cited
- [@lenz2006] magnetic-sensor taxonomy & field/vector distinction.
  [@yaniv2009] inductive coils as clinical gold standard; 5-DOF clinical use.
  [@raab1979] orthogonal-triad 6-DOF template. [@schneider2000] dual-coil 6-DOF
  sensor (angle/accuracy). [@davies2021] MR/TMR noise (Ch. 14). [@ndi_aurora]
  vendor sensor form factors.
