# Simulations (Phase 5)

Reference physics/DSP/estimation simulations that back the manuscript's figures
and supply its computed numbers. Pure NumPy/SciPy/Matplotlib; no GPU needed.

## Run

```bash
cd simulations
python3 -m pip install -r requirements.txt   # numpy, scipy, matplotlib
python3 run_all.py
```

Outputs (regenerated deterministically, seed `20260606`):
- **Figures** → `/figures/*.png`
- **Data** → `/data/*.{csv,json}`
- **Summary** → `simulations/RESULTS.md`, `/data/summary.json`

## Library: `emtrack/`

| Module | Backs | Contents |
|---|---|---|
| `fields.py` | Ch. 4 | dipole field (4.1), on-/off-axis loop (4.3, elliptic integrals) |
| `coupling.py` | Ch. 5 | coupling tensor K(r) (5.5), matrix M (5.6), forward model |
| `solver.py` | Ch. 23 | Levenberg–Marquardt pose solver |
| `crlb.py` | Ch. 24 | Jacobian, Fisher information, CRLB position σ (24.1) |

## What `run_all.py` computes (and which chapters it feeds)

1. **Dipole vs. finite-loop error** (Ch. 4 §4.6, Ch. 7) — error vs. `r/a`;
   confirms `(a/r)²` scaling. → replaces the Ch. 4 §4.6 table.
2. **Coupling identities** (Ch. 4/5) — K eigenvalues `{2,−1,−1}`, trace 0,
   on-axis/equator ratio 2.
3. **CRLB map & range curve** (Ch. 24) — position σ over the volume; finds
   on-axis `σ ∝ z⁴`; sub-mm to ~0.66 mm at 0.5 m for `σ_B = 1 nT`.
4. **Monte-Carlo vs. CRLB** (Ch. 24/25) — LM solver error matches CRLB to ~3%.
5. **Lock-in detection** (Ch. 20) — amplitude error `∝ 1/√T` (fitted `T^-0.49`).
6. **Dipole field plot** (Ch. 4) — streamline figure / visualizer backing.

> These are reference-grade, readable implementations, not optimized production
> code. Absolute CRLB/Monte-Carlo values scale with the assumed measurement
> noise `σ_B` (documented in `RESULTS.md`); the *scalings* and *identities* are
> assumption-free.
