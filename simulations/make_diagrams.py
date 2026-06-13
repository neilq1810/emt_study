#!/usr/bin/env python3
"""Generate schematic diagrams (Phase 4) for the EM-Tracking-Definitive-Guide.

Unlike run_all.py (which plots *computed* data), this draws *conceptual* schematics
with matplotlib primitives so they stay version-controlled and reproducible. Output
PNGs go to /figures and are referenced from the manuscript.

Run:  cd simulations && python3 make_diagrams.py
Deps: numpy, matplotlib
"""
from __future__ import annotations

import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)

C_ANALOG = "#dbeafe"   # light blue
C_DIGITAL = "#dcfce7"  # light green
C_PHYS = "#fef3c7"     # amber
C_OUT = "#fce7f3"      # pink
EDGE = "#334155"


def box(ax, cx, cy, w, h, text, fc="#eef2ff", fontsize=9):
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                                boxstyle="round,pad=0.012,rounding_size=0.03",
                                fc=fc, ec=EDGE, lw=1.3, zorder=3))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fontsize, zorder=4)
    return (cx, cy)


def arrow(ax, p1, p2, style="-|>", color=EDGE, lw=1.6, ls="-", rad=0.0):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=14,
                                 color=color, lw=lw, linestyle=ls, zorder=2,
                                 connectionstyle=f"arc3,rad={rad}"))


# ---------------------------------------------------------------------------
# Fig A — full system signal chain / block diagram (Ch. 8, Ch. 11)
# ---------------------------------------------------------------------------
def diagram_system_block() -> None:
    fig, ax = plt.subplots(figsize=(10, 5.2))
    ax.set_xlim(0, 10); ax.set_ylim(0, 5.2); ax.axis("off")

    # domain bands
    ax.axhspan(3.4, 4.7, color=C_ANALOG, alpha=0.25, zorder=0)
    ax.axhspan(0.5, 2.6, color=C_DIGITAL, alpha=0.25, zorder=0)
    ax.text(0.15, 4.55, "analog", fontsize=8, style="italic", color="#1e40af")
    ax.text(0.15, 2.45, "digital", fontsize=8, style="italic", color="#166534")

    y1, y2 = 4.05, 1.55
    w, h = 1.45, 0.78
    # top row (left -> right): excitation/sense/convert
    g = box(ax, 1.0, y1, w, h, "Field\ngenerator\n(drive coils)", C_ANALOG)
    s = box(ax, 4.0, y1, w, h, "Sensor\ncoil(s)", C_ANALOG)
    afe = box(ax, 6.2, y1, w, h, "AFE\n(LNA, filter)", C_ANALOG)
    adc = box(ax, 8.4, y1, w, h, "ADC", C_ANALOG)
    # field coupling (physics) between generator and sensor
    arrow(ax, (g[0] + w / 2, y1), (s[0] - w / 2, y1), style="-|>", color="#b45309", lw=2.0)
    ax.text(2.5, y1 + 0.5, "magnetic field\n$B\\propto m_t/r^3$", ha="center",
            fontsize=8.5, color="#b45309")
    arrow(ax, (s[0] + w / 2, y1), (afe[0] - w / 2, y1))
    arrow(ax, (afe[0] + w / 2, y1), (adc[0] - w / 2, y1))

    # ADC -> DSP (drop to bottom row)
    dsp = box(ax, 8.4, y2, w, h, "DSP:\nlock-in /\ndemod", C_DIGITAL)
    arrow(ax, (adc[0], y1 - h / 2), (dsp[0], y2 + h / 2))
    # bottom row (right -> left): estimate
    solv = box(ax, 6.2, y2, w, h, "Pose solver\n(LM / MLE)", C_DIGITAL)
    fus = box(ax, 4.0, y2, w, h, "Kalman /\nfusion\n(+IMU/optical)", C_DIGITAL)
    disp = box(ax, 1.3, y2, 1.7, h, "Navigation\ndisplay\n+ confidence", C_OUT)
    arrow(ax, (dsp[0] - w / 2, y2), (solv[0] + w / 2, y2))
    arrow(ax, (solv[0] - w / 2, y2), (fus[0] + w / 2, y2))
    arrow(ax, (fus[0] - w / 2, y2), (disp[0] + 0.85, y2))
    ax.text(5.1, y2 + 0.52, "pose + covariance", ha="center", fontsize=8, color="#166534")

    # clock / sync (drives generator, ADC, DSP)
    clk = box(ax, 8.4, 3.0, 1.2, 0.5, "clock / sync", "#e2e8f0", fontsize=8)
    arrow(ax, (clk[0] - 0.6, 3.0), (1.0, y1 - h / 2), style="-|>", color="#64748b",
          lw=1.1, ls=(0, (4, 3)), rad=-0.18)
    arrow(ax, clk, (adc[0], y1 - h / 2), style="-|>", color="#64748b", lw=1.1, ls=(0, (4, 3)))
    arrow(ax, (clk[0], 3.0 - 0.25), (dsp[0], y2 + h / 2), style="-|>", color="#64748b",
          lw=1.1, ls=(0, (4, 3)))

    # detect-and-flag feedback (solver quality -> display)
    arrow(ax, (solv[0], y2 + h / 2), (disp[0], y2 + h / 2), style="-|>", color="#b91c1c",
          lw=1.3, ls=(0, (2, 2)), rad=0.35)
    ax.text(3.7, y2 + 1.15, "distortion / quality flag", ha="center", fontsize=8,
            color="#b91c1c")

    ax.set_title("EMT system signal chain: field $\\to$ sensor $\\to$ AFE/ADC $\\to$ "
                 "DSP $\\to$ pose $\\to$ display", fontsize=11)
    fig.tight_layout()
    fig.savefig(FIG / "ch08_system_block_diagram.png", dpi=150)
    plt.close(fig)
    print("[figA] ch08_system_block_diagram.png")


# ---------------------------------------------------------------------------
# Fig B — transmitter-sensor coupling geometry (Ch. 5)
# ---------------------------------------------------------------------------
def diagram_coupling_geometry() -> None:
    fig, ax = plt.subplots(figsize=(7.2, 5.4))
    ax.set_xlim(-1.4, 4.6); ax.set_ylim(-1.2, 4.0); ax.set_aspect("equal"); ax.axis("off")

    # dipole field lines (a few) for a z-oriented transmitter at origin
    th = np.linspace(0.05, np.pi - 0.05, 200)
    for L in (0.7, 1.2, 1.8):
        r = L * np.sin(th) ** 2
        ax.plot(r * np.sin(th), r * np.cos(th), color="#93c5fd", lw=1.0, zorder=1)
        ax.plot(-r * np.sin(th), r * np.cos(th), color="#93c5fd", lw=1.0, zorder=1)

    # transmitter triad at origin
    O = np.array([0, 0])
    arrow(ax, O, (0, 1.0), style="-|>", color="#1e3a8a", lw=2.2)
    arrow(ax, O, (1.0, 0), style="-|>", color="#1e3a8a", lw=2.2)
    arrow(ax, O, (-0.5, -0.5), style="-|>", color="#1e3a8a", lw=2.0)
    ax.text(0.06, 1.05, "$m_z$", color="#1e3a8a", fontsize=10)
    ax.text(1.03, 0.05, "$m_x$", color="#1e3a8a", fontsize=10)
    ax.text(-0.05, -0.32, "transmitter\ntriad", ha="right", fontsize=9)

    # sensor position vector r
    P = np.array([3.0, 2.4])
    arrow(ax, O, tuple(P), style="-|>", color="#334155", lw=1.8)
    ax.text(1.5, 1.45, "$\\vec r$", fontsize=12, color="#334155")
    ax.plot([P[0]], [P[1]], "o", color="#be123c", ms=4, zorder=5)

    # field direction at sensor (tangent to dipole field) + sensor coil axis n
    Bdir = np.array([0.85, 0.2]); Bdir = Bdir / np.linalg.norm(Bdir)
    arrow(ax, tuple(P), tuple(P + 0.9 * Bdir), style="-|>", color="#b45309", lw=1.8)
    ax.text(*(P + 0.9 * Bdir + np.array([0.05, 0.08])), "$\\vec B(\\vec r)$",
            color="#b45309", fontsize=11)
    n = np.array([0.3, 0.95]); n = n / np.linalg.norm(n)
    arrow(ax, tuple(P), tuple(P + 0.8 * n), style="-|>", color="#7c3aed", lw=1.8)
    ax.text(*(P + 0.8 * n + np.array([-0.35, 0.05])), "$\\hat{\\vec n}$ (sensor\naxis)",
            color="#7c3aed", fontsize=9)

    # angle theta at origin between m_z and r
    ang = np.linspace(np.pi / 2, np.arctan2(P[1], P[0]), 30)
    ax.plot(0.6 * np.cos(ang), 0.6 * np.sin(ang), color="#475569", lw=1.0)
    ax.text(0.72, 0.62, "$\\theta$", fontsize=11, color="#475569")

    ax.text(2.0, -0.9, "coupling $V \\propto \\hat{\\vec n}\\cdot\\vec B(\\vec r)$, "
            "$\\;|\\vec B|\\propto m_t/r^3$", ha="center", fontsize=10)
    ax.set_title("Transmitter–sensor coupling geometry (Ch. 5)", fontsize=11)
    fig.tight_layout(); fig.savefig(FIG / "ch05_coupling_geometry.png", dpi=150); plt.close(fig)
    print("[figB] ch05_coupling_geometry.png")


# ---------------------------------------------------------------------------
# Fig C — eddy-current distortion mechanism (Ch. 6)
# ---------------------------------------------------------------------------
def diagram_distortion_mechanism() -> None:
    fig, ax = plt.subplots(figsize=(8.4, 4.4))
    ax.set_xlim(0, 10); ax.set_ylim(0, 4.4); ax.axis("off")

    box(ax, 1.2, 2.2, 1.5, 1.0, "Field\ngenerator", C_ANALOG)
    cond = box(ax, 5.0, 2.2, 1.6, 1.1, "conductor\n(e.g. C-arm)", "#e5e7eb")
    box(ax, 8.7, 2.2, 1.5, 1.0, "Sensor", C_ANALOG)

    # primary field G -> conductor and G -> sensor
    arrow(ax, (2.0, 2.5), (4.2, 2.5), style="-|>", color="#b45309", lw=1.8)
    ax.text(3.0, 2.75, "primary $\\vec B_0$", fontsize=8.5, color="#b45309")
    arrow(ax, (1.9, 1.9), (7.95, 1.6), style="-|>", color="#b45309", lw=1.5, rad=-0.12)

    # eddy loops in conductor
    for dx in (-0.3, 0.3):
        e = plt.Circle((5.0 + dx, 2.2), 0.28, fill=False, ec="#0e7490", lw=1.6, zorder=4)
        ax.add_patch(e)
    ax.text(5.0, 0.95, "induced eddy\ncurrents", ha="center", fontsize=8.5, color="#0e7490")

    # secondary field conductor -> sensor
    arrow(ax, (5.8, 2.0), (7.95, 2.2), style="-|>", color="#be123c", lw=1.8, rad=-0.18)
    ax.text(6.9, 1.5, "secondary $\\vec B_s$", fontsize=8.5, color="#be123c")

    ax.text(5.0, 3.9, "Sensor reads $\\vec B_0+\\vec B_s$ — the distortion is the "
            "$\\vec B_s$ term (Ch. 6)", ha="center", fontsize=10)
    ax.text(5.0, 0.35, "$\\vec B_s$ grows with conductor size and proximity; for AC it lags "
            "in phase (eddy decay $\\tau_e=\\mu_0\\sigma a^2/\\pi^2$)", ha="center",
            fontsize=8.5, color="#475569")
    ax.set_title("Eddy-current distortion: primary + secondary field superposition (Ch. 6)",
                 fontsize=11)
    fig.tight_layout(); fig.savefig(FIG / "ch06_distortion_mechanism.png", dpi=150); plt.close(fig)
    print("[figC] ch06_distortion_mechanism.png")


# ---------------------------------------------------------------------------
# Fig D — excitation/multiplexing schemes: TDM / FDM / pulsed-DC (Ch. 19, Ch. 10)
# ---------------------------------------------------------------------------
def diagram_excitation_schemes() -> None:
    t = np.linspace(0, 1, 1000)
    fig, axs = plt.subplots(3, 1, figsize=(8.2, 5.6), sharex=True)

    # TDM: three axes active in sequence
    ax = axs[0]
    for i in range(3):
        seg = (t >= i / 3) & (t < (i + 1) / 3)
        ax.plot(t, np.where(seg, np.sin(2 * np.pi * 18 * t) * 0.8 + (2 - i) * 2.2, (2 - i) * 2.2),
                lw=1.0, color=f"C{i}")
        ax.text(1.01, (2 - i) * 2.2, f"axis {i+1}", va="center", fontsize=8, color=f"C{i}")
    ax.set_title("TDM — one axis at a time (time-multiplexed)", fontsize=9.5, loc="left")
    ax.set_ylim(-1.2, 5.6)

    # FDM: three simultaneous tones at different frequencies
    ax = axs[1]
    for i, f in enumerate((10, 16, 23)):
        ax.plot(t, np.sin(2 * np.pi * f * t) * 0.8 + (2 - i) * 2.2, lw=1.0, color=f"C{i}")
        ax.text(1.01, (2 - i) * 2.2, f"$f_{i+1}$", va="center", fontsize=8, color=f"C{i}")
    ax.set_title("FDM — all axes simultaneously, separated by frequency", fontsize=9.5, loc="left")
    ax.set_ylim(-1.2, 5.6)

    # pulsed-DC: step then settle, sample after eddy decay
    ax = axs[2]
    for i in range(3):
        base = (2 - i) * 2.2
        seg = (t >= i / 3) & (t < (i + 1) / 3)
        step = np.where(t >= i / 3, 1.0, 0.0) * np.where(t < (i + 1) / 3, 1.0, 0.0)
        settle = step * (1 - np.exp(-(t - i / 3).clip(0) * 40))
        ax.plot(t, settle * 0.9 + base, lw=1.1, color=f"C{i}")
        # sample marker near end of each slot (after settling)
        ts = (i + 0.92) / 3
        ax.plot([ts], [0.9 + base], "v", color="k", ms=5)
    ax.text(0.92 / 3, 5.0, "sample after\neddy settling", fontsize=7.5, ha="center")
    ax.set_title("Pulsed-DC — energize, wait for eddy settling, sample the static field",
                 fontsize=9.5, loc="left")
    ax.set_ylim(-0.4, 5.6); ax.set_xlabel("time (normalized frame)")
    for ax in axs:
        ax.set_yticks([]); ax.set_xlim(0, 1.08)
    fig.suptitle("Excitation / channel-separation schemes (Ch. 19, Ch. 10)", fontsize=11)
    fig.tight_layout(); fig.savefig(FIG / "ch19_excitation_schemes.png", dpi=150); plt.close(fig)
    print("[figD] ch19_excitation_schemes.png")


def main() -> None:
    diagram_system_block()
    diagram_coupling_geometry()
    diagram_distortion_mechanism()
    diagram_excitation_schemes()
    print("[done] schematic diagrams written to /figures")


if __name__ == "__main__":
    main()
