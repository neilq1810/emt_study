"""Fisher information and the Cramer-Rao lower bound (Ch. 24)."""

from __future__ import annotations

import numpy as np

from .coupling import forward_model


def jacobian(x: np.ndarray, na_s: float = 1.0, m_t: float = 1.0, eps: float = 1e-7) -> np.ndarray:
    """Numerical Jacobian J = dh/dx of the forward model at pose x (9x6)."""
    x = np.asarray(x, float)
    h0 = forward_model(x, na_s, m_t)
    J = np.zeros((h0.size, x.size))
    for k in range(x.size):
        dx = np.zeros_like(x)
        dx[k] = eps
        J[:, k] = (forward_model(x + dx, na_s, m_t) - forward_model(x - dx, na_s, m_t)) / (2 * eps)
    return J


def fisher_information(x: np.ndarray, sigma: float, **kw) -> np.ndarray:
    """Fisher information F = J^T J / sigma^2 (Gaussian model, Ch. 24 eq. 24.1)."""
    J = jacobian(x, **kw)
    return (J.T @ J) / sigma**2


def crlb_position_sigma(x: np.ndarray, sigma: float, **kw) -> float:
    """Lower bound on position RMS error: sqrt(trace of position block of F^-1).

    Returns +inf if the Fisher matrix is singular (unobservable pose).
    """
    F = fisher_information(x, sigma, **kw)
    try:
        cov = np.linalg.inv(F)
    except np.linalg.LinAlgError:
        return float("inf")
    pos = np.trace(cov[:3, :3])
    return float(np.sqrt(pos)) if pos >= 0 else float("inf")
