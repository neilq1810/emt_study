# Decision Frameworks

> **Reference.** Two recurring design choices the book develops across several chapters,
> consolidated here as quick-reference tables.

## D.1 Excitation waveform / mode

The choice of how the field is driven is the most architecture-defining decision in EMT. The
induction sensor differentiates (EMF $\propto\dot B$, Ch. 5), so the *sensor output waveform
is the time-derivative of the excitation* — which is why the rows differ in their detection
and distortion behaviour (Ch. 6/9 §9.9/19/20/28).

| | **AC sinusoidal** | **AC triangular** | **Pulsed-DC (step)** |
|---|---|---|---|
| Field $B(t)$ | sinusoid | triangle | step + hold |
| Sensor EMF | sinusoid (90° shifted) | **square wave** (constant $\dot B$ segments) | impulse → decay; read settled static field |
| Detection | sine lock-in | square-wave lock-in / sign-flip-and-average | sample after eddy settling (matched to the post-step waveform) |
| Conductive (eddy) distortion | present; appears in **quadrature** at $\omega\tau_e<1$ (a built-in flag, Ch. 20 §20.10) | same | **rejected** by waiting out the transient (Ch. 6 §6.4) |
| Drive/offset | precise sinusoid; AC (no DC-offset issue) | simple ramp; **polarity inversion rejects DC offset** | bipolar steps; DC-coupled sensing |
| Update-rate cost | integration time $T$ | $T$ | per-axis eddy-settling wait (slower) |
| Exemplar | Polhemus (Ch. 28.1) | NDI/Ascension patent family (Ch. 9 §9.9) | Ascension Bird / 3D Guidance (Ch. 28.2) |

**Rule of thumb.** Pulsed-DC trades update rate for conductive-distortion immunity; AC trades
distortion sensitivity for speed and a free *quadrature* distortion sentinel; the triangular
variant keeps AC's speed with a simpler drive and built-in offset rejection. None escapes
*ferromagnetic* distortion (in-phase, all modes).

## D.2 Standards → evidence (medical EMT)

Each concern below is a named input to the regulatory file; the table maps it to the standard
and the chapter where the engineering evidence is produced (consolidates Ch. 48 §48.7).

| Concern | Standard | Evidence in |
|---|---|---|
| Quality system & design controls | ISO 13485 / 21 CFR 820 (QMSR) | Ch. 48 |
| Risk management | ISO 14971 | Ch. 45 |
| Usability / use safety | IEC 62366-1; FDA HF guidance | Ch. 46 |
| Basic electrical safety | IEC 60601-1 | Ch. 17 |
| EMC | IEC 60601-1-2 | Ch. 17 |
| Software lifecycle | IEC 62304 | Ch. 35 |
| Cybersecurity | IEC 81001-5-1; FDA §524B | Ch. 35 §35.7 |
| Performance / accuracy | NEMA/Hummel-style; ASTM F2554 | Ch. 33 |
| Computational-model credibility | ASME V&V 40; FDA CM&S | Ch. 53 |
| Clinical evidence (US/EU) | FDA IDE / ISO 14155; MDR Annex XIV | Ch. 49 |
| Post-market | 21 CFR 803 (MDR); MDR vigilance/PMCF | Ch. 52 |

**US vs EU framing.** The US route is usually a **510(k)** on substantial equivalence to a
predicate (De Novo / PMA otherwise); the EU route demonstrates conformity to the **MDR GSPR**
via a Notified-Body QMS + dossier audit. Both are fed by one engine — an ISO 13485 / 21 CFR
820 quality system whose design controls make every requirement traceable to a verification
or validation record in the DHF (Ch. 48).
