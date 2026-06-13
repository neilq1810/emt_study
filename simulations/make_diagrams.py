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
# Fig D — excitation/multiplexing schemes: TDM / FDM / CDM / pulsed-DC (Ch. 19, Ch. 10)
# ---------------------------------------------------------------------------
def diagram_excitation_schemes() -> None:
    t = np.linspace(0, 1, 1000)
    fig, axs = plt.subplots(4, 1, figsize=(8.2, 7.0), sharex=True)

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

    # CDM: all axes simultaneously, separated by orthogonal Walsh-Hadamard codes
    ax = axs[2]
    H = np.array([[1, 1, 1, 1], [1, -1, 1, -1], [1, 1, -1, -1], [1, -1, -1, 1]])
    codes = H[1:4]  # three non-trivial Hadamard rows -> three channels
    nchip = codes.shape[1]
    for i, code in enumerate(codes):
        chip = np.clip((t * nchip).astype(int), 0, nchip - 1)
        ax.step(t, code[chip] * 0.8 + (2 - i) * 2.2, where="post", lw=1.1, color=f"C{i}")
        ax.text(1.01, (2 - i) * 2.2, f"code {i+1}", va="center", fontsize=8, color=f"C{i}")
    for k in range(1, nchip):
        ax.axvline(k / nchip, color="#cbd5e1", lw=0.6, ls=":")
    ax.set_title("CDM — all axes simultaneously, separated by orthogonal (Hadamard) codes",
                 fontsize=9.5, loc="left")
    ax.set_ylim(-1.2, 5.6)

    # pulsed-DC: step then settle, sample after eddy decay
    ax = axs[3]
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


# ---------------------------------------------------------------------------
# Fig E — dipole hemisphere / parity ambiguity (Ch. 24 §24.7)
# ---------------------------------------------------------------------------
def diagram_hemisphere_ambiguity() -> None:
    fig, ax = plt.subplots(figsize=(7.6, 5.6))
    ax.set_xlim(-3.4, 3.4); ax.set_ylim(-2.7, 3.0); ax.set_aspect("equal"); ax.axis("off")

    th = np.linspace(0.05, np.pi - 0.05, 200)
    for L in (0.8, 1.4):
        r = L * np.sin(th) ** 2
        for sx in (1, -1):
            ax.plot(sx * r * np.sin(th), r * np.cos(th), color="#cbd5e1", lw=0.9, zorder=1)
    box(ax, 0, 0, 1.3, 0.5, "dipole generator", "#e2e8f0", fontsize=8)

    P = np.array([2.1, 1.3])
    for sign, fc, ec, lab, ls in ((+1, "#be123c", "#be123c", "sensor at $+\\vec r$", "-"),
                                  (-1, "white", "#64748b", "mirror at $-\\vec r$", (0, (4, 3)))):
        Q = sign * P
        arrow(ax, (0, 0), tuple(Q), style="-|>", color=ec, lw=1.6, ls=ls)
        ax.add_patch(plt.Circle(tuple(Q), 0.14, fc=fc, ec=ec, lw=1.5, zorder=5))
        nvec = sign * np.array([0.25, 0.7])
        arrow(ax, tuple(Q), tuple(Q + nvec), style="-|>", color=ec, lw=1.5, ls=ls)
        ax.text(*(Q + sign * np.array([0.15, 0.42])), lab, fontsize=9, color=ec,
                ha="left" if sign > 0 else "right")

    ax.text(0, 2.55, "Single dipole generator: $+\\vec r$ and $-\\vec r$ give "
            "IDENTICAL measurements", ha="center", fontsize=10)
    ax.text(0, 2.12, "$K(\\vec r)\\propto 3\\hat r\\hat r^{T}-I$ is invariant under "
            "$\\hat r\\to-\\hat r$ (global un-identifiability)", ha="center",
            fontsize=8.5, color="#475569")
    ax.add_patch(FancyBboxPatch((-3.2, -2.65), 6.4, 0.62, boxstyle="round,pad=0.02",
                                fc="#ecfeff", ec="#0e7490", lw=1.0, zorder=3))
    ax.text(0, -2.34, "Resolved by: asymmetric / planar generator (§9.7) · half-space prior · "
            "tracking continuity · fusion (§21.9)", ha="center", fontsize=8.5, color="#0e7490")
    ax.set_title("The dipole hemisphere / parity ambiguity (Ch. 24 §24.7)", fontsize=11)
    fig.tight_layout(); fig.savefig(FIG / "ch24_hemisphere_ambiguity.png", dpi=150); plt.close(fig)
    print("[figE] ch24_hemisphere_ambiguity.png")


# ---------------------------------------------------------------------------
# Fig F — the 5-DOF roll null and its dual-coil fix (Ch. 13)
# ---------------------------------------------------------------------------
def diagram_roll_null() -> None:
    from matplotlib.patches import Ellipse

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.4, 4.6))
    for ax in (a1, a2):
        ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.7, 2.0); ax.set_aspect("equal"); ax.axis("off")

    # panel 1: single coil, roll about its own axis is unobservable
    a1.add_patch(Ellipse((0, 0), 0.9, 0.32, angle=0, fc="#dbeafe", ec="#1e3a8a", lw=1.6))
    arrow(a1, (0, 0), (0, 1.2), style="-|>", color="#1e3a8a", lw=2.0)
    a1.text(0.08, 1.15, "$\\hat n$", color="#1e3a8a", fontsize=11)
    # roll arrow (circular) about n
    rr = np.linspace(-0.6, 3.6, 60)
    a1.plot(0.45 * np.cos(rr), 0.7 + 0.16 * np.sin(rr), color="#b91c1c", lw=1.6)
    arrow(a1, (0.45 * np.cos(3.4), 0.7 + 0.16 * np.sin(3.4)),
          (0.45 * np.cos(3.7), 0.7 + 0.16 * np.sin(3.7)), style="-|>", color="#b91c1c", lw=1.6)
    a1.text(0, -1.25, "Single-axis sensor:\nroll about $\\hat n$ leaves every\nmeasurement "
            "unchanged ✗ (rank-deficient $J$)", ha="center", fontsize=9, color="#b91c1c")
    a1.set_title("5-DOF: roll unobservable", fontsize=10)

    # panel 2: two coils at angle theta -> roll observable
    a2.add_patch(Ellipse((0, 0), 0.9, 0.32, angle=0, fc="#dbeafe", ec="#1e3a8a", lw=1.6))
    arrow(a2, (0, 0), (0, 1.2), style="-|>", color="#1e3a8a", lw=2.0)
    a2.add_patch(Ellipse((0, 0), 0.9, 0.32, angle=55, fc="#dcfce7", ec="#166534", lw=1.6))
    arrow(a2, (0, 0), (1.2 * np.sin(np.radians(35)), 1.2 * np.cos(np.radians(35))),
          style="-|>", color="#166534", lw=2.0)
    ang = np.linspace(np.pi / 2, np.radians(55), 24)
    a2.plot(0.5 * np.cos(ang), 0.5 * np.sin(ang), color="#475569", lw=1.0)
    a2.text(0.45, 0.5, "$\\theta$", fontsize=11, color="#475569")
    a2.text(0, -1.25, "Second (askew) element:\nroll now observable ✓\n(observability "
            "$\\propto\\sin\\theta$, sim 9)", ha="center", fontsize=9, color="#166534")
    a2.set_title("6-DOF: dual coil resolves roll", fontsize=10)
    fig.suptitle("The 5-DOF roll null and its dual-coil fix (Ch. 13)", fontsize=11)
    fig.tight_layout(); fig.savefig(FIG / "ch13_roll_null.png", dpi=150); plt.close(fig)
    print("[figF] ch13_roll_null.png")


# ---------------------------------------------------------------------------
# Fig G — design controls V-model (Ch. 48)
# ---------------------------------------------------------------------------
def diagram_design_controls() -> None:
    fig, ax = plt.subplots(figsize=(9.2, 5.4))
    ax.set_xlim(0, 10); ax.set_ylim(0, 5.4); ax.axis("off")

    # left (descending) arm
    un = box(ax, 1.6, 4.6, 2.2, 0.7, "User needs\n(intended use)", C_PHYS)
    di = box(ax, 1.6, 3.2, 2.2, 0.7, "Design inputs\n(requirements)", C_ANALOG)
    do = box(ax, 1.6, 1.8, 2.2, 0.7, "Design outputs\n(specs, code)", C_ANALOG)
    # bottom
    impl = box(ax, 5.0, 0.7, 2.4, 0.7, "Implementation\n& design transfer", "#e2e8f0")
    # right (ascending) arm
    ver = box(ax, 8.4, 1.8, 2.4, 0.7, "Verification\n(meets inputs?)", C_DIGITAL)
    val = box(ax, 8.4, 3.2, 2.4, 0.7, "Validation\n(meets user needs?)", C_DIGITAL)
    rel = box(ax, 8.4, 4.6, 2.4, 0.7, "Released device\n+ DHF", C_OUT)
    arrow(ax, (un[0], 4.25), (di[0], 3.55)); arrow(ax, (di[0], 2.85), (do[0], 2.15))
    arrow(ax, (do[0], 1.45), (impl[0] - 1.2, 0.85), rad=-0.1)
    arrow(ax, (impl[0] + 1.2, 0.85), (ver[0], 1.45), rad=-0.1)
    arrow(ax, (ver[0], 2.15), (val[0], 2.85)); arrow(ax, (val[0], 3.55), (rel[0], 4.25))
    # horizontal V&V correspondence links (dashed)
    arrow(ax, (do[0] + 1.1, 1.8), (ver[0] - 1.2, 1.8), style="<|-|>", color="#64748b",
          lw=1.1, ls=(0, (4, 3)))
    ax.text(5.0, 2.0, "verification: built it right", ha="center", fontsize=8, color="#475569")
    arrow(ax, (un[0] + 1.1, 4.6), (val[0] - 1.2, 4.6), style="<|-|>", color="#64748b",
          lw=1.1, ls=(0, (4, 3)), rad=-0.12)
    ax.text(5.0, 5.0, "validation: built the right thing", ha="center", fontsize=8,
            color="#475569")
    ax.text(5.0, 3.5, "ISO 13485 / 21 CFR 820.30\ndesign controls;\nall captured in the DHF",
            ha="center", fontsize=8.5, color="#7c3aed")
    ax.set_title("Design controls: the V&V V-model (Ch. 48 §48.4–48.5)", fontsize=11)
    fig.tight_layout(); fig.savefig(FIG / "ch48_design_controls.png", dpi=150); plt.close(fig)
    print("[figG] ch48_design_controls.png")


# ---------------------------------------------------------------------------
# Fig H — navigation-confidence error ellipsoid & the coupling penalty (Ch. 46 §46.6)
# ---------------------------------------------------------------------------
def diagram_error_ellipsoid() -> None:
    from matplotlib.patches import Ellipse

    fig, ax = plt.subplots(figsize=(7.4, 5.4))
    ax.set_xlim(-3.2, 3.6); ax.set_ylim(-2.8, 3.0); ax.set_aspect("equal"); ax.axis("off")

    # target crosshair
    ax.axhline(0, color="#cbd5e1", lw=0.8); ax.axvline(0, color="#cbd5e1", lw=0.8)
    ax.plot(0, 0, "+", color="#334155", ms=14, mew=2)

    # naive (orientation-known) 95% ellipse vs marginalized 6-DOF (x2.95)
    naive_w, naive_h, angle = 1.0, 0.6, 28
    ax.add_patch(Ellipse((0, 0), naive_w, naive_h, angle=angle, fill=False,
                         ec="#166534", lw=1.8))
    ax.add_patch(Ellipse((0, 0), naive_w * 2.95, naive_h * 2.95, angle=angle, fill=False,
                         ec="#b45309", lw=1.8, ls=(0, (5, 3))))
    ax.text(0.62, 0.30, "naive\n(orientation\nknown)", color="#166534", fontsize=8)
    ax.text(-3.1, 1.7, "marginalized 6-DOF\n($\\times$2.95 coupling\npenalty, §24.6)",
            color="#b45309", fontsize=8.5, ha="left")

    # tool-axis cone
    apex = np.array([-2.2, -1.8])
    for dth in (-9, 9):
        d = np.array([np.sin(np.radians(35 + dth)), np.cos(np.radians(35 + dth))])
        arrow(ax, tuple(apex), tuple(apex + 2.4 * d), style="-", color="#7c3aed", lw=1.3)
    ax.text(-1.2, -1.0, "tool-axis cone\n($\\pm2.8\\,\\sigma_\\varphi$)", color="#7c3aed",
            fontsize=8.5)

    # traffic-light confidence chip
    for i, (c, lab) in enumerate([("#16a34a", "GREEN"), ("#d97706", "AMBER"), ("#dc2626", "RED")]):
        ax.add_patch(plt.Circle((2.7, 2.4 - i * 0.5), 0.15, fc=c, ec="none"))
        ax.text(2.95, 2.4 - i * 0.5, lab, va="center", fontsize=8, color=c)
    ax.text(2.85, 2.78, "$T_{95}$ vs $\\tau$", fontsize=8, color="#334155", ha="center")

    ax.text(0.2, -2.55, "Display the 95% ellipsoid from the MARGINALIZED covariance "
            "(§24.6); using the naive block under-draws it ~3×", ha="center", fontsize=8.5,
            color="#475569")
    ax.set_title("Navigation-confidence display: honest error ellipsoid (Ch. 46 §46.6)",
                 fontsize=11)
    fig.tight_layout(); fig.savefig(FIG / "ch46_error_ellipsoid.png", dpi=150); plt.close(fig)
    print("[figH] ch46_error_ellipsoid.png")


def main() -> None:
    diagram_system_block()
    diagram_coupling_geometry()
    diagram_distortion_mechanism()
    diagram_excitation_schemes()
    diagram_hemisphere_ambiguity()
    diagram_roll_null()
    diagram_design_controls()
    diagram_error_ellipsoid()
    print("[done] schematic diagrams written to /figures")


if __name__ == "__main__":
    main()
