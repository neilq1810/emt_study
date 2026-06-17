# Error-Source Catalog

> **Reference.** A one-row-per-source lookup of every error mechanism in the book, with its
> class, scaling/behaviour, combination rule, and primary mitigation. This is the *findable*
> companion to the class-organized treatment of **Ch. 25** (which explains *why* the class
> sets the combination rule and the worked propagation); use Ch. 25 to understand, this to
> look up. "Combine" is how the term enters the budget: **RSS** (variances add), **bias**
> (signed; calibrate, don't average), or **correlated** (adds ~linearly across channels).

## Stochastic (the precision floor — averages as $1/\sqrt{T}$)
| Source | Scaling / behaviour | Combine | Mitigation | Where |
|---|---|---|---|---|
| Sensor self-noise (coil Johnson / MR–TMR 1/f) | white (coil) or 1/f (MR); the usual floor | RSS | moment, area, integration; low-noise device | 15, 14.3, 25.2 |
| Barkhausen / domain noise | low-freq, **non-Gaussian**; partly hysteretic | RSS (+bias) | single-domain/vortex layer, set/reset | 14.3, 25.2 |
| RTS / popcorn (MTJ) | discrete bursty switching; **fat tails** | RSS (+tails) | larger junction, set/reset, averaging | 14.3, 25.2 |
| Bias-reference noise (TMR) | multiplicative (∝ bias); + shot noise ∝√I | RSS, multiplicative | stable low-noise reference | 25.2 |
| AFE noise ($e_n,\,i_n\lvert Z_s\rvert$) | white + 1/f; voltage & current noise | RSS | keep below sensor floor; source-impedance match | 16, 25.2 |
| ADC quantization + thermal | white **if dithered**; else signal-correlated spurs | RSS | ENOB/oversampling, dither | 18, 25.2 |
| Clock / aperture jitter | $\propto f_\text{sig}\,\sigma_t$; usually tiny in EMT | RSS | clean reference; coherent clocking | 10, 18 |
| Cable microphonic / dielectric | random, vibration/flex-driven on the µV signal | RSS | low-tribo cable, strain relief, guarding | 16, 17 |

## Deterministic (the bias floor — calibrate, don't average)
| Source | Scaling / behaviour | Combine | Mitigation | Where |
|---|---|---|---|---|
| Sensor/generator tolerances | fixed per-unit (area-turns, axis, inter-element angle) | bias | per-unit calibration | 15, 26 |
| Forward-model mismatch | dipole vs real cored generator; map residual | bias | field mapping / harmonic model | 7, 26 |
| Calibration residual | the irreducible part calibration missed | bias | better cal; identifiability (Ch. 55) | 26, 55 |
| Crosstalk / spectral leakage | **correlated** bias on $M_{ij}$ (FDM/leakage) | bias (correlated) | TDM, guard bands, coherent sampling | 19, 20 |
| Thermal drift | drifts after cal (coil/core/MR/ref/gain) | bias (drifting) | stability spec, recalibration interval | 15, 26 |
| Numerical error | ill-conditioning, finite precision | bias | QR/SVD solve, conditioning, fixed-point WL | 22, 24 |
| Nonlinearity → harmonic/IMD | **signal-amplitude-dependent** (∝1/r³ swing) → pose-dependent bias + harmonic folding | bias + crosstalk | linear region, gain ranging, low-THD drive, sine ref, FDM plan | 14/16/18/20, 25.3 |
| Cross-axis / non-orthogonality | off-diagonal sensor-matrix terms; mixes DOF | bias | 3×3 sensor-matrix calibration | 14/15, 25.3 |
| Sensor offset & drift (field sensors) | additive; coil has none; drifts (temp/time/history) | bias | set/reset, chopping; AC & pulsed-DC reject *static* offset | 14.3, 25.3 |
| Hysteresis | **history-dependent** → non-repeatable (breaks single-value cal) | bias (non-repeatable) | soft/low-remanence materials, set/reset, linear minor loop | 14, 25.3 |
| Amplifier gain / offset | gain = multiplicative bias; offset additive | bias (offset AC-rejected) | per-channel gain cal; lock-in rejects offset | 16, 25.3 |
| Magnetostriction / stress | cored-sensor permeability shift under flex | bias | low-magnetostriction core, mechanical isolation | 14, 25.3 |

## Environmental (the wild card — detect, map, fuse, flag)
| Source | Scaling / behaviour | Combine | Mitigation | Where |
|---|---|---|---|---|
| Field distortion (eddy + ferromagnetic) | the dominant environmental term; bias + outliers; eddy shows in **quadrature** (§20.10) | bias + outliers | mapping, witness/redundancy, fusion, flag | 6, 27 |
| Ambient EM / susceptibility | broadband background; usually small (<~0.15 mm) | RSS | shielding, band-select, EMC (60601-1-2) | 17, 25.4 |
| Generator (transmitter-side) noise | **correlated across all channels** (scales $\mathbf M$) | correlated (~linear) | low-noise drive, ratiometric | 9, 25.4 |
| Motion / latency | dynamic bias $\approx v\,\Delta t$; intra-frame TDM skew | bias (dynamic) | simultaneity, prediction, fusion, sync | 12, 19, 10 |
| Cable effects (triboelectric / flex bias) | deterministic drift sibling of the stochastic microphonic term | bias + noise | cable discipline, strain relief | 16, 17 |
| Synchronization / phase-reference drift | leakage + unusable phase if asynchronous | bias | shared-clock coherent detection | 10, 20 |
| DC geomagnetic background | a large static offset a field sensor must reject | (rejected) | AC / pulsed-DC differencing; set/reset | 4, 25.3 |
| Overload / clipping | hard nonlinearity near generator / from interferer | bias/outlier | gain ranging, band-select, dynamic reserve | 16, 20 |

**Reading the catalog.** The single most useful column is **Combine**: independent stochastic
terms RSS (so the *largest* dominates and is the one to attack), deterministic terms add as
biases that calibration must remove (not averaging), and **correlated** terms (generator
noise, crosstalk) add nearly linearly across channels — which is why a correlated source can
dominate even when each channel's share looks small (Ch. 25 §25.5, GUM eq. 25.1). The
recurring EMT lesson across all three tables: **field distortion is usually the largest single
contributor**, and motion/latency is a *separate operating condition* that a static budget
does not cover.
