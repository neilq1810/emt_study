# Appendix — Derivations

> **Reference.** The derivations the chapters defer or use in passing, collected for
> completeness. (This is the "Appendix C" the lock-in chapter points to for the ENBW result.)

## A.1 Equivalent noise bandwidth (ENBW)

A demodulator with impulse response $h(t)$ (normalized to unit DC gain,
$\int h\,dt=1$) passes input noise of one-sided PSD $S_n$ to an output variance
$\sigma^2 = S_n\!\int_0^\infty |H(f)|^2\,df = S_n\cdot\mathrm{ENBW}$, where the **equivalent
noise bandwidth** is the width of an ideal brick-wall filter of the same peak gain passing
the same noise:
$$
\mathrm{ENBW} = \frac{\int_0^\infty |H(f)|^2\,df}{|H(0)|^2}.
$$

- **Integrate-and-dump (boxcar)**, $h(t)=1/T$ on $[0,T)$: $H(f)=\operatorname{sinc}(fT)$, and
  $\int_0^\infty \operatorname{sinc}^2(fT)\,df = 1/(2T)$, so
  $$\boxed{\ \mathrm{ENBW}_\text{boxcar}=\frac{1}{2T}\ }\quad\text{(one-sided).}$$
- **First-order RC**, $H(f)=1/(1+j2\pi f\tau)$: $\int_0^\infty \frac{df}{1+(2\pi f\tau)^2}=\frac{1}{4\tau}$, so
  $$\boxed{\ \mathrm{ENBW}_\text{RC}=\frac{1}{4\tau}.\ }$$

This is the constant behind the lock-in's $\sigma_A\propto\sqrt{S_n\,\mathrm{ENBW}}\propto
1/\sqrt T$ law (Ch. 20 §20.2) and the processing gain $B/\mathrm{ENBW}=2BT$.

## A.2 The magnetic dipole field

From the vector potential of a point dipole $\mathbf m$ at the origin,
$\mathbf A=\frac{\mu_0}{4\pi}\frac{\mathbf m\times\hat{\mathbf r}}{r^2}$, taking
$\mathbf B=\nabla\times\mathbf A$ gives
$$
\mathbf B(\mathbf r)=\frac{\mu_0}{4\pi}\frac{3(\mathbf m\cdot\hat{\mathbf r})\hat{\mathbf r}-\mathbf m}{r^3}.
$$
The bracket defines the coupling tensor $\mathbf K=\frac{\mu_0}{4\pi}(3\hat{\mathbf r}\hat{\mathbf r}^\top-\mathbf I)/r^3$ (Ch. 5), symmetric and traceless with eigenvalues
$\frac{\mu_0}{4\pi r^3}\{2,-1,-1\}$ — the on-axis-to-equator $2{:}1$ anisotropy and the
$1/r^3$ falloff that set EMT's whole signal scale.

## A.3 The closed-form initializer eigenstructure ($4{:}1{:}1$)

For a co-located transmitter triad and sensor triad, the measured coupling is
$\mathbf M=\mathbf R^\top\mathbf K$. Then
$\mathbf M^\top\mathbf M=\mathbf K^\top\mathbf K$ (rotation drops out), and using
$\mathbf K\propto 3\hat{\mathbf r}\hat{\mathbf r}^\top-\mathbf I$,
$$
\mathbf K^\top\mathbf K\propto (3\hat{\mathbf r}\hat{\mathbf r}^\top-\mathbf I)^2
= 9\hat{\mathbf r}\hat{\mathbf r}^\top - 6\hat{\mathbf r}\hat{\mathbf r}^\top + \mathbf I
= 4\hat{\mathbf r}\hat{\mathbf r}^\top + (\mathbf I-\hat{\mathbf r}\hat{\mathbf r}^\top),
$$
whose eigenvalues are $\mathbf 4$ along $\hat{\mathbf r}$ and $\mathbf 1,\mathbf 1$
transverse — the **$4{:}1{:}1$** spectrum the Phase-5 sim confirms to machine precision
(Ch. 23 §23.5). The dominant eigenvector recovers the bearing $\hat{\mathbf r}$ (up to the
sign — the hemisphere ambiguity, Ch. 24 §24.7); range follows from the eigenvalue magnitude.

## A.4 The 6-DOF Fisher information & the marginalized position CRLB

For the Gaussian model the FIM is $\mathbf F=\mathbf J^\top\mathbf R^{-1}\mathbf J$, blocked
into position, orientation, and coupling:
$\mathbf F=\begin{bmatrix}\mathbf F_{pp}&\mathbf F_{p\varphi}\\\mathbf F_{\varphi p}&\mathbf F_{\varphi\varphi}\end{bmatrix}$.
The *honest* position CRLB is the position block of the full inverse, i.e. the **Schur
complement**
$$
[\mathbf F^{-1}]_{pp}=\big(\mathbf F_{pp}-\mathbf F_{p\varphi}\mathbf F_{\varphi\varphi}^{-1}\mathbf F_{\varphi p}\big)^{-1}\ \succeq\ \mathbf F_{pp}^{-1},
$$
the subtracted term being the information lost to estimating an unknown orientation. For the
co-located triad/triad geometry this inflates the position CRLB by a **pose-invariant
$\approx2.95\times$** (variance $\approx8.7\times$); orientation degrades as $z^3$ versus
position's $z^4$ (Ch. 24 §24.6, computed in `simulations/run_all.py`).
