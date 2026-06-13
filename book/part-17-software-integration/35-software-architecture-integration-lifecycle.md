# Chapter 35 — Software Architecture, Integration & Lifecycle

> **Status:** DEEPENED (awaiting review) · **Part XVII — Software, Integration & Deployment**
> The software *around* the algorithms: how the pose engine is architected, how it
> integrates with clinical and robotic software, and how it is engineered to a
> medical-device lifecycle. This chapter deliberately **cross-references** Parts
> VII–VIII (algorithms) and Ch. 22 (real-time implementation) rather than repeating
> them. Citation keys resolve to
> [`../../citations/bibliography.json`](../../citations/bibliography.json).

This book has developed the **algorithms** of electromagnetic tracking (the DSP of
Part VII, the solvers of Part VIII) and their **real-time realization** in silicon
(Ch. 22). Those are necessary but not sufficient: a *deployable* tracker is a
layered software system that streams trustworthy pose into someone else's
application, and — in medicine — is built to a regulated software process. Two
things the rest of the book only gestures at ("Host / API," Ch. 8/12/22) are the
subject here: the **software architecture and integration/interoperability layer**
that makes a tracker usable, and the **medical-device software lifecycle**
(IEC 62304 [@iec62304]) that the safety case (Ch. 17, 29) requires. The recurring
theme — *never silently emit a wrong pose* — turns out to be, ultimately, a
**software** requirement.

---

## 35.1 The software stack

A deployable EMT system is a layered stack; each layer has a different real-time
character and a different owner:

```
Application      navigation UI · robot control · IGT therapy        (3rd-party)
   ▲  timestamped pose + covariance + status  │  config/commands ▼
Integration      OpenIGTLink · ROS · PLUS bridge                    [§35.3]
   ▲
SDK / API        public streaming + status + configuration         [§35.2]
   ▲
Pose engine      calibration → solve (Ch.23) → filter (Ch.21)       [§35.2]
   ▲              → covariance (Ch.24)   — floating-point back end
Driver / HAL     enumeration · transport (Ch.12) · timestamping
   ▲
Firmware         deterministic streaming demod (Ch.22)  — fixed-point front end
```

The **data contract** (Ch. 11 §11.6) flows *up* — a timestamped 6-DOF pose **with
its covariance and a status flag**, per tracked tool — and configuration flows
*down*. Everything in this chapter is about getting that contract across layer and
vendor boundaries without losing the timestamp, the uncertainty, or the honesty.

## 35.2 The pose-engine software architecture

- **Threading model.** A hard-real-time **acquisition** thread (Ch. 22) feeds, through
  **lock-free ring buffers**, a **pose** thread (calibrate → solve → filter) and an
  **output/streaming** thread. The real-time path must **never block**: no
  unbounded allocation, no garbage collection, preallocated buffers, pinned/priority
  threads, and backpressure rather than stalls. This is the software expression of
  the Ch. 12 latency budget and the Ch. 22 WCET requirement.
- **Timestamping & clock discipline (Ch. 10).** Stamp each sample at **acquisition**
  in hardware, then map to the host clock (PTP/NTP); every pose carries its
  **acquisition** time, not its arrival time — essential for fusion (Ch. 21) and for
  a robot closing a loop on it (Ch. 29 §29.5). A late but correctly-timestamped pose
  is recoverable; a wrongly-timestamped one is not.
- **State machine.** `searching → tracking → degraded/distorted → lost` (Ch. 22
  §22.6, Ch. 27 detect-and-flag). The API must **expose** the state; a consumer must
  be able to tell "1 mm pose" from "distorted, do not trust" (Ch. 17 §17.3 essential
  performance).
- **Configuration & calibration data.** Field maps and per-unit calibration (Ch. 26)
  are **versioned, checksummed, and device-matched** artifacts with provenance for
  the regulatory file (§35.4) — loading the wrong or stale map is a silent accuracy
  failure.

## 35.3 Integration & interoperability — the API layer

This is the practically critical, currently-missing piece: how the tracker talks to
the world.

- **The pose data contract as a wire protocol.** Stream, per tool and per frame: the
  6-DOF pose, **its covariance** (Ch. 11 §11.6, Ch. 24 — so downstream gets honest
  error bars), a **quality/status** field, the **acquisition timestamp**, and an
  explicit **coordinate-frame** identifier. Dropping the covariance or the timestamp
  at the boundary is the most common integration sin.
- **OpenIGTLink** [@tokuda2009] — the de-facto open network protocol for image-guided
  therapy: `TRANSFORM`/`POSITION`/`STATUS` messages carry tracker pose to navigation
  software. It is the lingua franca between trackers and applications, used by the
  open-source **Anser** EMT [@jaeger2017], 3D Slicer, and PLUS.
- **PLUS toolkit** [@lasso2014] — an open-source toolkit unifying many tracking and
  imaging devices behind one interface, with calibration and OpenIGTLink streaming;
  a common substrate that spares integrators a bespoke driver per device.
- **3D Slicer + SlicerIGT** [@fedorov2012] — the open research navigation platform
  most trackers are first integrated against, over OpenIGTLink.
- **IGSTK** — a **state-machine-based, safety-by-design** C++ toolkit for image-guided
  surgery, notable because it *enforces* legal state transitions (the software-safety
  posture of §35.4). (conf: med — named for completeness; primary citation to add.)
- **ROS** for robotic integration — `tf` transform trees and time-stamped poses;
  mind the non-real-time middleware on any hard control loop (Ch. 22).
- **Coordinate frames and the registration handoff.** The tracker emits pose in the
  **generator frame**; the integrator must compose it with patient/image/robot
  frames (the clinical chain, Ch. 29 §29.7; the rig frames, Ch. 33 §33.6).
  **Frame discipline — who owns which transform — is where integration bugs and
  target-registration error live.**

## 35.4 Medical-device software lifecycle — IEC 62304

The software peer of the electrical-safety standard (IEC 60601, Ch. 17): a clinical
pose engine is regulated **software**.

- **IEC 62304** [@iec62304] defines the life-cycle processes — planning, requirements,
  architecture, detailed design, implementation, integration & verification, and
  release/maintenance.
- **Software safety classification (Class A/B/C),** risk-based on the harm a software
  failure could cause. A pose engine driving navigation or **ablation** is typically
  **Class B or C**, pulling in the full rigor of documentation, V&V, and traceability.
- **SOUP — software of unknown provenance.** Third-party libraries (an RTOS, a linear-
  algebra/solver library, the OpenIGTLink/ROS stack) must be **identified,
  version-pinned, risk-assessed, and monitored** for relevant anomalies — a real
  constraint on casually dropping in an arbitrary solver (Ch. 23) or filter (Ch. 21).
- **Risk management tie (ISO 14971).** Software contributions to hazards — a silently
  wrong pose (Ch. 27), a missed distortion, a latency overrun (Ch. 12) — become
  **software requirements** whose mitigations are the detect-and-flag and
  essential-performance behaviors defined in pose terms (Ch. 17 §17.3, Ch. 29 §29.7).
- **Verification & validation.** Unit/integration/system tests; the **bit-exact
  determinism** of the fixed-point front end (Ch. 22) is a *testable* property;
  fault injection (Ch. 22 §22.6); regression on stored calibration data; and the
  **no-testing-on-training-data** discipline carried over from calibration and
  characterization (Ch. 26 §26.5, Ch. 33 §33.1).
- **Cybersecurity.** A networked tracker (OpenIGTLink/ROS in the OR) has an attack
  surface, and a compromise is a **safety** event — developed fully in §35.7.

## 35.5 Numerical robustness, determinism & reproducibility

- **Fixed vs. floating point (Ch. 22).** The fixed-point streaming front end is
  bit-exact and therefore *certifiable*; the floating-point nonlinear back end needs
  guards — NaN/Inf traps, conditioning checks (Ch. 24), and **deterministic
  reduction ordering** so results are reproducible across runs and platforms.
- **Reproducibility.** Same input → same pose (no uncontrolled seeds), for V&V and
  audit; **log raw measurements + pose + software/calibration versions** for
  post-market investigation.
- **Robust numerics as a safety behavior.** Guard the solve (Ch. 23 basins/
  rank-deficiency); on a bad solve, **clamp-and-flag** rather than emit garbage. The
  honesty posture the whole book argues for is, at the end of the stack, a few lines
  of defensive code plus the requirement that mandates them.

## 35.6 Open-source & reference implementations

A maturing ecosystem already implements much of this stack: **Anser** EMT
[@jaeger2017] (OpenIGTLink-native), the **PLUS** toolkit [@lasso2014], **3D Slicer/
SlicerIGT** [@fedorov2012], and the safety-oriented **IGSTK** — plus this project's
own [`simulations/`](../../simulations) and [`dashboard/`](../../dashboard) (Ch. 31
§31.8, Ch. 32). A fully open, **IEC 62304-validated** medical-grade tracking stack
remains an opportunity rather than a reality (Ch. 30).

## 35.7 Cybersecurity for networked trackers

A clinical EMT system is **networked** — it streams pose over OpenIGTLink/ROS, talks to
imaging and navigation software (§35.3), pulls software updates, and is serviced remotely
(Ch. 52) — so it has an attack surface. The decisive framing is that for a tracker,
**security is a safety property**: the realistic threats do not steal data, they
**corrupt the pose**.

- **A spoofed or altered pose stream** → the navigation shows the instrument where it is
  not → **wrong-site therapy** (the master hazard, Ch. 45), with the operator
  over-trusting an authoritative-looking crosshair (Ch. 46).
- **Tampered calibration data** (in transit from the factory chain of Ch. 50, or at rest)
  → a **silent accuracy fault** indistinguishable from a calibration drift (Ch. 26 §26.6).
- **Denial of service** → frozen or dropped navigation mid-procedure → loss of the
  essential performance the safety case promised (Ch. 12/17).

So cybersecurity hazards enter the **ISO 14971 risk file** (Ch. 45) on the same footing
as a hardware fault or a use error (Ch. 46) — security and safety are one analysis.

**The secure-lifecycle obligation.** Security, like safety, is a *process*, not a feature:
- **IEC 81001-5-1** [@iec81001_5_1] defines the **secure product development lifecycle**
  for health software (adapting IEC 62443-4-1): threat modeling, secure design and coding,
  an **SBOM**, vulnerability and patch management, and **post-market** security monitoring —
  the security peer of the IEC 62304 safety lifecycle (§35.4).
- **US FDA** now makes this **mandatory**: FD&C Act **§524B** requires every premarket
  submission for a *cyber device* to include a threat model, an SBOM, a secure-development
  framework, and a vulnerability-management plan [@fda_cyber2023] — cybersecurity has moved
  from recommendation to **legal precondition for clearance** (Ch. 48). The EU MDR carries
  parallel security expectations within the GSPR, reinforced by the wider EU cyber regime.
- The **SBOM is the SOUP list with teeth** (§35.4): the same version-pinned third-party
  components (RTOS, linear-algebra/solver libraries, the OpenIGTLink/ROS stack) must be
  **continuously monitored for disclosed vulnerabilities** over the device's decade-long
  field life (Ch. 52), not assessed once.

**Defense in depth, EMT-specific.** Beyond generic hygiene (secure boot, **signed
updates**, network segmentation of the OR, least privilege, audit logging — which doubles
as the forensic log of §35.5): **integrity-protect and authenticate the pose stream and the
calibration data**, because those are the assets whose corruption injures a patient. And
the book's recurring **detect-and-flag** is also a security control — an implausible pose
injected by an attacker trips the *same* consistency / innovation (NIS) checks that catch
distortion (Ch. 21 §21.8, Ch. 27), so the honesty machinery built for physics also raises
the bar for spoofing. Security and the safety case are, once more, the same discipline.
(conf: high — standards/statute verified; the safety-security framing is the consensus
position.)

> **Engineering takeaway.** The algorithms are necessary but not sufficient. A
> deployable EMT system is a layered, real-time software architecture that streams
> **timestamped pose + covariance + status** through standard interfaces
> (OpenIGTLink/PLUS/ROS) into navigation or robotic software, engineered to a
> medical-device lifecycle (IEC 62304) with software safety classification, SOUP
> control, reproducible numerics, and pose-defined essential performance. The
> detect-and-flag honesty insisted on throughout this book is, in the end, a
> software requirement — written down, classified, tested, and traced.

---

## Open questions / to verify
- ✅ **Resolved (§35.7, T2.14):** premarket **cybersecurity** developed and cited —
  IEC 81001-5-1 secure lifecycle [@iec81001_5_1] and FDA §524B / guidance
  [@fda_cyber2023], framed as a safety property (spoofed pose / tampered calibration →
  patient harm). Remaining: a worked EMT **threat model + SBOM** example.
- Add a primary citation for **IGSTK** (e.g. the IGSTK architecture/state-machine
  paper) and for **SlicerIGT** to firm up §35.3/§35.6.
- Provide a concrete **OpenIGTLink message mapping** for pose + covariance + status
  (a worked schema), tying the Ch. 11 §11.6 data contract to the wire format.
- Add a worked **software-safety-classification** example (Class B vs C) for a named
  EMT use (navigation vs. ablation guidance), with the resulting 62304 process delta.
- Cross-reference a real **latency/jitter** software measurement methodology (ties
  Ch. 12, Ch. 33 dynamic tests).

## Sources cited
- [@tokuda2009] OpenIGTLink network protocol. [@lasso2014] PLUS integration toolkit.
  [@fedorov2012] 3D Slicer navigation platform. [@iec62304] medical-device software
  life-cycle standard (safety classes A/B/C, SOUP). [@jaeger2017] Anser
  (OpenIGTLink-native open-source EMT). [@iec81001_5_1] secure-software lifecycle and
  [@fda_cyber2023] FDA premarket cybersecurity (§524B) — the §35.7 security peer of
  IEC 62304. Real-time/algorithm ties to Ch. 21–24 and Ch. 22;
  regulatory/essential-performance ties to Ch. 17, 29; risk file Ch. 45; lifecycle Ch. 48/52.
