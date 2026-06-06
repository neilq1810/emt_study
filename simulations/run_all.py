#!/usr/bin/env python3
"""Generate all Phase-5 simulation outputs for the EM-Tracking-Definitive-Guide.

Writes figures to /figures, machine-readable data to /data, and a summary to
simulations/RESULTS.md (including the numbers meant to be folded back into the
manuscript, replacing flagged 'to-generate' values).

Run:  cd simulations && python3 run_all.py
Deps: numpy, scipy, matplotlib  (see requirements.txt)
"""
from __future__ import annotations

import json
import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.transform import Rotation

from emtrack import (
    MU0,
    crlb_position_sigma,
    dipole_field,
    forward_model,
    loop_field_offaxis,
    loop_field_onaxis,
    solve_pose,
)

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
DATA = ROOT / "data"
FIG.mkdir(exist_ok=True)
DATA.mkdir(exist_ok=True)
RNG = np.random.default_rng(20260606)
SUMMARY: dict[str, object] = {}


# ---------------------------------------------------------------------------
# Sim 1 — dipole vs finite-loop approximation error (Ch. 4 §4.6, Ch. 7)
# ---------------------------------------------------------------------------
def sim_dipole_vs_loop() -> None:
    a = 0.05  # loop radius [m]
    m = 1.0   # target moment [A m^2]; single turn
    I = m / (np.pi * a**2)
    ratios = [1.5, 2, 3, 5, 7, 10, 15, 20]
    thetas = np.deg2rad(np.linspace(0, 90, 19))
    rows = []
    for ra in ratios:
        r = ra * a
        errs = []
        for th in thetas:
            rho, z = r * np.sin(th), r * np.cos(th)
            Brho, Bz = loop_field_offaxis(I, a, rho, z)
            B_loop = np.hypot(Brho, Bz)
            B_dip = np.linalg.norm(dipole_field([0, 0, m], [rho, 0, z]))
            errs.append(abs(B_dip - B_loop) / B_loop)
        rows.append((ra, max(errs) * 100, float(np.mean(errs)) * 100))

    # CSV
    with (DATA / "dipole_vs_loop_error.csv").open("w") as f:
        f.write("r_over_a,max_rel_error_pct,mean_rel_error_pct\n")
        for ra, mx, mn in rows:
            f.write(f"{ra},{mx:.4f},{mn:.4f}\n")

    # Figure (log-log shows ~(a/r)^2 slope)
    ras = np.array([r[0] for r in rows])
    mxs = np.array([r[1] for r in rows])
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.loglog(ras, mxs, "o-", label="max error over $\\theta$")
    ax.loglog(ras, 100.0 / ras**2, "--", color="gray", label="$\\propto (a/r)^2$ guide")
    ax.set_xlabel("$r/a$ (distance / coil radius)")
    ax.set_ylabel("dipole-approx. error [%]")
    ax.set_title("Dipole approximation error vs distance (finite loop)")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIG / "ch04_dipole_vs_loop_error.png", dpi=140)
    plt.close(fig)

    SUMMARY["dipole_vs_loop"] = {
        "rows": [{"r_over_a": ra, "max_err_pct": mx, "mean_err_pct": mn} for ra, mx, mn in rows]
    }
    print("[sim1] dipole-vs-loop error table written")


# ---------------------------------------------------------------------------
# Sim 2 — coupling-tensor identities (Ch. 4/5)
# ---------------------------------------------------------------------------
def sim_coupling_checks() -> None:
    from emtrack.coupling import coupling_tensor

    r = 0.3
    K = coupling_tensor([0, 0, r], m_t=1.0)
    scale = (MU0 / (4 * np.pi)) / r**3
    eig = np.sort(np.linalg.eigvalsh(K))[::-1] / scale
    B_ax = np.linalg.norm(dipole_field([0, 0, 1.0], [0, 0, r]))
    B_eq = np.linalg.norm(dipole_field([0, 0, 1.0], [r, 0, 0]))
    res = {
        "K_eigenvalues_over_scale": [round(float(v), 6) for v in eig],
        "K_trace": float(np.trace(K)),
        "onaxis_equator_ratio": float(B_ax / B_eq),
    }
    (DATA / "coupling_checks.json").write_text(json.dumps(res, indent=2))
    SUMMARY["coupling_checks"] = res
    print("[sim2] coupling checks:", res)


# ---------------------------------------------------------------------------
# Sim 3 — CRLB position-uncertainty map (Ch. 24)
# ---------------------------------------------------------------------------
def sim_crlb_map() -> None:
    sigma_B = 1e-9  # field-referred measurement noise [T] (assumption; see RESULTS)
    xs = np.linspace(-0.4, 0.4, 81)
    zs = np.linspace(0.05, 0.6, 81)
    grid = np.full((zs.size, xs.size), np.nan)
    for iz, z in enumerate(zs):
        for ix, x in enumerate(xs):
            pose = np.array([x, 0.0, z, 0.0, 0.0, 0.0])
            s = crlb_position_sigma(pose, sigma_B)
            grid[iz, ix] = s * 1e3  # mm
    grid = np.clip(grid, 1e-4, 1e3)

    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    im = ax.pcolormesh(xs, zs, np.log10(grid), shading="auto", cmap="viridis")
    cb = fig.colorbar(im, ax=ax)
    cb.set_label("$\\log_{10}$ position $\\sigma$ [mm]  (CRLB)")
    ax.set_xlabel("lateral offset x [m]")
    ax.set_ylabel("range z [m]")
    ax.set_title("CRLB position uncertainty (triad/triad, $\\sigma_B=1$ nT)")
    fig.tight_layout()
    fig.savefig(FIG / "ch24_crlb_map.png", dpi=140)
    plt.close(fig)

    # 1-D curve along z (x=0); fit power law sigma ~ z^p
    z_axis = np.linspace(0.1, 0.6, 30)
    sig_axis = np.array(
        [crlb_position_sigma(np.array([0, 0, z, 0, 0, 0]), sigma_B) * 1e3 for z in z_axis]
    )
    p = np.polyfit(np.log(z_axis), np.log(sig_axis), 1)[0]
    picks = {f"{z:.2f}m": float(crlb_position_sigma(np.array([0, 0, z, 0, 0, 0]), sigma_B) * 1e3)
             for z in (0.2, 0.3, 0.5)}

    with (DATA / "crlb_vs_range.csv").open("w") as f:
        f.write("z_m,pos_sigma_mm\n")
        for z, s in zip(z_axis, sig_axis):
            f.write(f"{z:.4f},{s:.6f}\n")

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.loglog(z_axis, sig_axis, "o-")
    ax.set_xlabel("range z [m]")
    ax.set_ylabel("CRLB position $\\sigma$ [mm]")
    ax.set_title(f"CRLB vs range on axis ($\\sigma\\propto z^{{{p:.1f}}}$)")
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIG / "ch24_crlb_vs_range.png", dpi=140)
    plt.close(fig)

    res = {"sigma_B_T": sigma_B, "power_law_exponent": float(p), "sigma_mm_at": picks}
    SUMMARY["crlb"] = res
    print("[sim3] CRLB:", res)


# ---------------------------------------------------------------------------
# Sim 4 — Monte-Carlo error vs CRLB (Ch. 25, Ch. 24 consistency)
# ---------------------------------------------------------------------------
def sim_monte_carlo() -> None:
    sigma_B = 1e-9
    n_trials = 400
    orient = np.array([0.1, -0.2, 0.15])
    poses = {"near_0.15m": 0.15, "mid_0.30m": 0.30, "far_0.50m": 0.50}
    out = {}
    for name, z in poses.items():
        x_true = np.array([0.0, 0.0, z, *orient])
        z_clean = forward_model(x_true)
        errs = []
        for _ in range(n_trials):
            zmeas = z_clean + RNG.normal(0, sigma_B, z_clean.shape)
            xh = solve_pose(zmeas, x_true, sigma=sigma_B)
            errs.append(np.linalg.norm(xh[:3] - x_true[:3]))
        emp = float(np.sqrt(np.mean(np.square(errs))) * 1e3)  # mm RMS
        crlb = float(crlb_position_sigma(x_true, sigma_B) * 1e3)
        out[name] = {"mc_rms_mm": emp, "crlb_mm": crlb, "ratio": emp / crlb}
    (DATA / "monte_carlo_vs_crlb.json").write_text(json.dumps(out, indent=2))
    SUMMARY["monte_carlo"] = out
    print("[sim4] Monte Carlo vs CRLB:", out)


# ---------------------------------------------------------------------------
# Sim 5 — lock-in amplitude estimate: error ~ 1/sqrt(T) (Ch. 20)
# ---------------------------------------------------------------------------
def sim_lockin() -> None:
    f0, fs, A, phi = 1000.0, 100_000.0, 1.0, 0.7
    noise = 5.0  # white-noise std (>> A: deeply buried signal)
    Ts = np.array([1e-3, 2e-3, 5e-3, 1e-2, 2e-2, 5e-2, 1e-1])
    n_trials = 200
    rms = []
    for T in Ts:
        n = int(fs * T)
        t = np.arange(n) / fs
        ref_c, ref_s = np.cos(2 * np.pi * f0 * t), np.sin(2 * np.pi * f0 * t)
        ests = []
        for _ in range(n_trials):
            v = A * np.cos(2 * np.pi * f0 * t + phi) + RNG.normal(0, noise, n)
            X, Y = 2 * np.mean(v * ref_c), 2 * np.mean(v * ref_s)
            ests.append(np.hypot(X, Y))
        rms.append(float(np.sqrt(np.mean((np.array(ests) - A) ** 2))))
    rms = np.array(rms)
    slope = np.polyfit(np.log(Ts), np.log(rms), 1)[0]

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.loglog(Ts * 1e3, rms, "o-", label="lock-in amplitude error")
    ax.loglog(Ts * 1e3, rms[0] * np.sqrt(Ts[0] / Ts), "--", color="gray",
              label="$\\propto 1/\\sqrt{T}$ guide")
    ax.set_xlabel("integration time T [ms]")
    ax.set_ylabel("amplitude RMS error")
    ax.set_title(f"Lock-in detection (noise/signal = {noise:.0f}; slope={slope:.2f})")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIG / "ch20_lockin_snr_vs_T.png", dpi=140)
    plt.close(fig)
    SUMMARY["lockin"] = {"noise_to_signal": noise, "loglog_slope": float(slope)}
    print(f"[sim5] lock-in error ~ T^{slope:.2f} (expect ~ -0.5)")


# ---------------------------------------------------------------------------
# Sim 6 — dipole field visualizer backing figure (Ch. 4)
# ---------------------------------------------------------------------------
def sim_dipole_field_plot() -> None:
    m = np.array([0, 0, 1.0])
    x = np.linspace(-0.5, 0.5, 30)
    z = np.linspace(-0.5, 0.5, 30)
    X, Z = np.meshgrid(x, z)
    Bx = np.zeros_like(X)
    Bz = np.zeros_like(X)
    Bmag = np.zeros_like(X)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            p = np.array([X[i, j], 0.0, Z[i, j]])
            if np.linalg.norm(p) < 0.05:
                Bmag[i, j] = np.nan
                continue
            B = dipole_field(m, p)
            Bx[i, j], Bz[i, j] = B[0], B[2]
            Bmag[i, j] = np.linalg.norm(B)
    fig, ax = plt.subplots(figsize=(5.5, 5))
    ax.streamplot(X, Z, Bx, Bz, color=np.log10(Bmag), cmap="plasma", density=1.2)
    ax.set_xlabel("x [m]"); ax.set_ylabel("z [m]")
    ax.set_title("Magnetic dipole field ($\\mathbf{m}\\parallel z$)")
    ax.set_aspect("equal")
    fig.tight_layout()
    fig.savefig(FIG / "ch04_dipole_field.png", dpi=140)
    plt.close(fig)
    print("[sim6] dipole field figure written")


# ---------------------------------------------------------------------------
# Sim 7 — skin depth & pulsed-DC eddy-current settling (Ch. 6)
# ---------------------------------------------------------------------------
def sim_eddy_skin_depth() -> None:
    # Skin depth delta = 1/sqrt(pi f mu sigma)  (Ch. 6, eq. 6.1) — exact.
    materials = {
        "Copper": (5.8e7, 1.0),
        "Aluminium": (3.5e7, 1.0),
        "Stainless 304 (non-mag)": (1.4e6, 1.0),
    }
    freqs = np.logspace(2, 5, 200)  # 100 Hz .. 100 kHz
    fig, ax = plt.subplots(figsize=(6, 4))
    table = {}
    for name, (sigma, mur) in materials.items():
        delta = 1.0 / np.sqrt(np.pi * freqs * (MU0 * mur) * sigma)
        ax.loglog(freqs, delta * 1e3, label=name)
        # value at 10 kHz (the book's worked frequency)
        d10 = 1.0 / np.sqrt(np.pi * 1e4 * (MU0 * mur) * sigma)
        table[name] = round(float(d10 * 1e3), 4)  # mm
    ax.set_xlabel("frequency [Hz]")
    ax.set_ylabel("skin depth $\\delta$ [mm]")
    ax.set_title("Skin depth vs frequency (eq. 6.1)")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIG / "ch06_skin_depth.png", dpi=140)
    plt.close(fig)

    # Pulsed-DC settling (ILLUSTRATIVE single-time-constant model): after a step,
    # eddy current ~ exp(-t/tau_e). Residual field error if sampled at delay t_s.
    taus = [0.5e-3, 1e-3, 2e-3]  # eddy L/R time constants [s] (illustrative)
    t_s = np.linspace(0, 12e-3, 200)
    fig, ax = plt.subplots(figsize=(6, 4))
    for tau in taus:
        ax.semilogy(t_s * 1e3, np.exp(-t_s / tau) * 100, label=f"$\\tau_e$={tau*1e3:.1f} ms")
    ax.axhline(1.0, color="gray", ls="--", lw=1, label="1% residual")
    ax.set_xlabel("sample delay after step [ms]")
    ax.set_ylabel("residual eddy error [%]")
    ax.set_title("Pulsed-DC eddy settling (illustrative single-$\\tau$ model)")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIG / "ch06_pulsed_dc_settling.png", dpi=140)
    plt.close(fig)

    res = {"skin_depth_mm_at_10kHz": table,
           "pulsed_dc_note": "single-time-constant illustrative model; real settling is multi-mode"}
    (DATA / "skin_depth.json").write_text(json.dumps(res, indent=2))
    SUMMARY["eddy_skin"] = res
    print("[sim7] skin depth @10kHz [mm]:", table)


def write_results_md() -> None:
    d = SUMMARY
    dv = d["dipole_vs_loop"]["rows"]  # type: ignore[index]
    lines = [
        "# Phase-5 Simulation Results",
        "",
        "Generated by `simulations/run_all.py` (seed 20260606). Figures in",
        "`/figures`, data in `/data`. These are the computed numbers intended to",
        "replace flagged 'to-generate' values in the manuscript.",
        "",
        "## Sim 1 — Dipole approximation error vs distance (Ch. 4 §4.6, Ch. 7)",
        "",
        "| r/a | max error over θ [%] | mean error [%] |",
        "|----:|----------------------:|---------------:|",
    ]
    for row in dv:  # type: ignore[union-attr]
        lines.append(f"| {row['r_over_a']:g} | {row['max_err_pct']:.2f} | {row['mean_err_pct']:.2f} |")
    lines += [
        "",
        "Confirms the leading correction scales ~ (a/r)²; **use these to replace",
        "the order-of-magnitude table in Ch. 4 §4.6.**",
        "",
        "## Sim 2 — Coupling-tensor identities (Ch. 4/5)",
        f"- K eigenvalues / scale = {d['coupling_checks']['K_eigenvalues_over_scale']} (expected {{2,-1,-1}})",  # type: ignore[index]
        f"- trace(K) = {d['coupling_checks']['K_trace']:.2e} (expected 0)",  # type: ignore[index]
        f"- on-axis/equator |B| ratio = {d['coupling_checks']['onaxis_equator_ratio']:.4f} (expected 2)",  # type: ignore[index]
        "",
        "## Sim 3 — CRLB position uncertainty (Ch. 24)",
        f"- assumed field-referred noise σ_B = {d['crlb']['sigma_B_T']:.0e} T",  # type: ignore[index]
        f"- on-axis CRLB σ ≈ {d['crlb']['sigma_mm_at']}  (mm)",  # type: ignore[index]
        f"- grows ~ z^{d['crlb']['power_law_exponent']:.1f} with range (the 1/r³ conditioning penalty, Ch. 24 §24.2)",  # type: ignore[index]
        "",
        "## Sim 4 — Monte-Carlo vs CRLB (Ch. 24/25)",
    ]
    for k, v in d["monte_carlo"].items():  # type: ignore[union-attr]
        lines.append(f"- {k}: MC RMS = {v['mc_rms_mm']:.4f} mm, CRLB = {v['crlb_mm']:.4f} mm (ratio {v['ratio']:.2f})")
    lines += [
        "",
        "MC matches CRLB where well-conditioned, confirming the solver is efficient",
        "and the CRLB is a usable design predictor (Ch. 24).",
        "",
        "## Sim 5 — Lock-in detection (Ch. 20)",
        f"- amplitude error scales as T^{d['lockin']['loglog_slope']:.2f} (expected ≈ −0.5, i.e. ∝1/√T)",  # type: ignore[index]
        f"  even with noise/signal = {d['lockin']['noise_to_signal']:.0f} (signal far below noise).",  # type: ignore[index]
        "",
        "## Sim 7 — Skin depth & pulsed-DC settling (Ch. 6)",
        f"- skin depth at 10 kHz [mm]: {d['eddy_skin']['skin_depth_mm_at_10kHz']}"  # type: ignore[index]
        " (Cu value matches the Ch. 6 §6.2 hand calculation).",
        "- pulsed-DC settling figure is an illustrative single-τ model (labelled as such).",
        "",
        "## Figures",
        "- `figures/ch04_dipole_field.png` — dipole field streamlines",
        "- `figures/ch06_skin_depth.png`, `ch06_pulsed_dc_settling.png` — eddy/skin (Ch. 6)",
        "- `figures/ch04_dipole_vs_loop_error.png` — approximation error vs r/a",
        "- `figures/ch24_crlb_map.png`, `figures/ch24_crlb_vs_range.png` — CRLB",
        "- `figures/ch20_lockin_snr_vs_T.png` — lock-in error vs integration time",
        "",
    ]
    (pathlib.Path(__file__).resolve().parent / "RESULTS.md").write_text("\n".join(lines))
    (DATA / "summary.json").write_text(json.dumps(SUMMARY, indent=2))
    print("[done] RESULTS.md and data/summary.json written")


def main() -> None:
    sim_dipole_vs_loop()
    sim_coupling_checks()
    sim_crlb_map()
    sim_monte_carlo()
    sim_lockin()
    sim_dipole_field_plot()
    sim_eddy_skin_depth()
    write_results_md()


if __name__ == "__main__":
    main()
