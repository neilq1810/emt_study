"""Magnetic fields: point dipole and finite circular loop (Ch. 4).

Conventions: SI units, field in tesla, lengths in metres. A loop/coil lies in
the xy-plane with axis along +z unless otherwise transformed by the caller.
"""

from __future__ import annotations

import numpy as np
from scipy.special import ellipe, ellipk

MU0 = 4.0e-7 * np.pi  # vacuum permeability [H/m]


def magnetic_moment(turns: float, current: float, area: float) -> float:
    """m = N * I * A  [A*m^2]  (Ch. 5, eq. for dipole moment)."""
    return turns * current * area


def dipole_field(m_vec: np.ndarray, r_vec: np.ndarray) -> np.ndarray:
    """Point magnetic-dipole field B(r) (Ch. 4, eq. 4.1).

    B = (mu0/4pi) * (1/r^3) * [3 (m.rhat) rhat - m].
    `m_vec`: dipole moment vector [A*m^2]; `r_vec`: observation point [m].
    """
    m_vec = np.asarray(m_vec, float)
    r_vec = np.asarray(r_vec, float)
    r = np.linalg.norm(r_vec)
    if r == 0:
        raise ValueError("dipole_field singular at r=0")
    rhat = r_vec / r
    return (MU0 / (4 * np.pi)) * (3 * np.dot(m_vec, rhat) * rhat - m_vec) / r**3


def loop_field_onaxis(current: float, radius: float, z: float, turns: float = 1.0) -> float:
    """On-axis field of a circular loop (Ch. 4, eq. 4.3). Returns Bz [T]."""
    a = radius
    return MU0 * turns * current * a**2 / (2.0 * (a**2 + z**2) ** 1.5)


def loop_field_offaxis(
    current: float, radius: float, rho: float, z: float, turns: float = 1.0
) -> tuple[float, float]:
    """Exact off-axis field of a circular loop via complete elliptic integrals
    (Ch. 4, §4.5). Loop in xy-plane, axis +z. Returns (Brho, Bz) [T].

    Uses SciPy's convention K(m), E(m) with parameter m = k^2.
    """
    a = radius
    if rho == 0.0:
        return 0.0, loop_field_onaxis(current, a, z, turns)
    alpha_sq = a**2 + rho**2 + z**2 - 2 * a * rho
    beta_sq = a**2 + rho**2 + z**2 + 2 * a * rho
    beta = np.sqrt(beta_sq)
    k2 = 1.0 - alpha_sq / beta_sq  # = m parameter for SciPy
    C = MU0 * turns * current / np.pi
    Ek = ellipe(k2)
    Kk = ellipk(k2)
    Bz = (C / (2 * alpha_sq * beta)) * (
        (a**2 - rho**2 - z**2) * Ek + alpha_sq * Kk
    )
    Brho = (C * z / (2 * alpha_sq * beta * rho)) * (
        (a**2 + rho**2 + z**2) * Ek - alpha_sq * Kk
    )
    return Brho, Bz
