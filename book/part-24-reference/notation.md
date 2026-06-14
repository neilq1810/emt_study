# Notation & Symbols

> **Reference.** The recurring symbols of the book, grouped by domain, with the chapter where
> each is introduced. Where a symbol is overloaded by convention (e.g. $Q$), both meanings are
> noted.

## Fields, sources & coupling
| Symbol | Meaning | Intro |
|---|---|---|
| $\mathbf B$ | magnetic flux density (the tracked field) | Ch. 4 |
| $\mathbf m,\ m_t$ | magnetic dipole moment; transmitter moment | Ch. 4 |
| $\mu_0$ | permeability of free space | Ch. 4 |
| $\mathbf r,\ \hat{\mathbf r},\ r$ | source→sensor vector, its unit bearing, range | Ch. 4/5 |
| $\mathbf K(\mathbf r)$ | dipole coupling tensor $\propto(3\hat{\mathbf r}\hat{\mathbf r}^\top-\mathbf I)/r^3$ | Ch. 5 |
| $\mathbf M,\ M_{ij}$ | $3\times3$ coupling matrix; (sense $j$, transmit $i$) element | Ch. 5 |
| $N,\ A,\ NA$ | sensor turns, effective area, area-turns | Ch. 5/13 |
| $\delta$ | skin depth $=1/\sqrt{\pi f\mu\sigma}$ | Ch. 6 |
| $\tau_e$ | eddy-current decay time constant $\approx\mu_0\sigma a^2/\pi^2$ | Ch. 6 |
| $a_{lm}$ | solid/spherical-harmonic field-model coefficients | Ch. 7 |

## Pose, geometry & estimation
| Symbol | Meaning | Intro |
|---|---|---|
| $\mathbf x=(\mathbf p,\boldsymbol\varphi)$ | 6-DOF pose: position + orientation (rotation vector) | Ch. 23/24 |
| $\mathbf R$ | rotation matrix (sensor frame → lab) | Ch. 5/21 |
| $\theta,\ \phi$ | polar/azimuth angles; also signal phase (Ch. 20) | Ch. 4/20 |
| $h(\mathbf x;\boldsymbol\theta)$ | forward measurement model (params $\boldsymbol\theta$) | Ch. 23/53 |
| $\mathbf J=\partial h/\partial\mathbf x$ | measurement Jacobian | Ch. 23/24 |
| $\mathbf F=\mathbf J^\top\mathbf R^{-1}\mathbf J$ | Fisher information matrix | Ch. 24 |
| $\mathbf P,\ \operatorname{Cov}$ | estimate covariance; CRLB $=\mathbf F^{-1}$ | Ch. 24 |
| $\kappa(\mathbf J)$ | condition number $=\sigma_{\max}/\sigma_{\min}$ | Ch. 24 |
| PDOP | position dilution of precision | Ch. 24 |
| $z$ | on-axis range (the $z^4$ accuracy law) | Ch. 24 |

## Noise, SNR & detection
| Symbol | Meaning | Intro |
|---|---|---|
| $\sigma_B$ | field-referred measurement noise (the CRLB input; a *modeled* quantity) | Ch. 24/54 |
| $S_n$ | noise power spectral density | Ch. 20 |
| ENBW | equivalent noise bandwidth (boxcar $1/2T$, RC $1/4\tau$) | Ch. 20 |
| $T,\ \tau$ | integration time; filter time constant | Ch. 20 |
| $X,\ Y$ | lock-in in-phase / quadrature outputs; $A=2\sqrt{X^2+Y^2}$ | Ch. 20 |
| $Q$ | **(overloaded)** coil quality factor (Ch. 9) *and* quadrature component (Ch. 20) | Ch. 9/20 |
| SNR, ENOB | signal-to-noise ratio; effective number of bits | Ch. 18/20 |

## Clinical-system accuracy
| Symbol | Meaning | Intro |
|---|---|---|
| TRE, FRE | target / fiducial registration error | Ch. 39 |
| $T_{95}$ | predicted 95% target error $=2.80\,\sigma_\text{tgt}$ | Ch. 46 |
| $\tau$ (clinical) | the procedure's accuracy tolerance | Ch. 46/29 |
| $v,\ \Delta t$ | target velocity; cross-modality time skew ($\varepsilon\approx v\,\Delta t$) | Ch. 10 |
| $\boldsymbol\theta_\text{env}$ | environment (room/C-arm) twin parameters | Ch. 56 |

> **A note on $\sigma_B$.** Throughout, the CRLB is evaluated at an *assumed*
> $\sigma_B=1\,\text{nT}$ — a modeled placeholder, not a measured fact. The forward-twin
> chapter (Ch. 54) shows how to compose $\sigma_B$ (a *matrix*, not a scalar) from the
> measured sensor/AFE/ADC/generator/ambient chain; the absolute accuracy numbers scale with
> whatever floor your build actually achieves.
