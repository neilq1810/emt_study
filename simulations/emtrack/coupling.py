"""Coupling tensor / matrix and the triad-triad forward model (Ch. 5)."""

from __future__ import annotations

import numpy as np
from scipy.spatial.transform import Rotation

from .fields import MU0


def coupling_tensor(r_vec: np.ndarray, m_t: float = 1.0) -> np.ndarray:
    """Dipole coupling tensor K(r) (Ch. 5, eq. 5.5).

    K = (mu0 m_t / 4pi) (3 rhat rhat^T - I) / r^3.
    The field of a transmitter dipole of moment m_t*e_i is K @ e_i (column i).
    K is symmetric and traceless; eigenvalues (mu0 m_t/4pi r^3) * {2, -1, -1}.
    """
    r_vec = np.asarray(r_vec, float)
    r = np.linalg.norm(r_vec)
    rhat = r_vec / r
    return (MU0 * m_t / (4 * np.pi)) * (3 * np.outer(rhat, rhat) - np.eye(3)) / r**3


def coupling_matrix(
    r_vec: np.ndarray, R: np.ndarray, na_s: float = 1.0, m_t: float = 1.0
) -> np.ndarray:
    """3x3 coupling matrix M (Ch. 5, eq. 5.6): M = na_s * R^T K(r).

    Entry M[j, i] is the signal on sensor axis j from transmit axis i, where R
    maps sensor-frame axes into the lab frame. `na_s` lumps the sensor
    effective area-turns (per-axis) constant.
    """
    return na_s * (np.asarray(R, float).T @ coupling_tensor(r_vec, m_t))


def _rotvec_to_R(rotvec: np.ndarray) -> np.ndarray:
    return Rotation.from_rotvec(np.asarray(rotvec, float)).as_matrix()


def forward_model(x: np.ndarray, na_s: float = 1.0, m_t: float = 1.0) -> np.ndarray:
    """Measurement model h(x): pose -> flattened 3x3 coupling matrix (9-vector).

    x = [px, py, pz, rx, ry, rz] with (rx,ry,rz) an SO(3) rotation vector.
    Returns the 9 coupling values a solver/CRLB operates on.
    """
    x = np.asarray(x, float)
    r_vec = x[:3]
    R = _rotvec_to_R(x[3:6])
    return coupling_matrix(r_vec, R, na_s=na_s, m_t=m_t).reshape(-1)
