"""Levenberg-Marquardt pose solver (Ch. 23)."""

from __future__ import annotations

import numpy as np
from scipy.optimize import least_squares

from .coupling import forward_model


def solve_pose(
    z: np.ndarray,
    x0: np.ndarray,
    sigma: float = 1.0,
    na_s: float = 1.0,
    m_t: float = 1.0,
) -> np.ndarray:
    """Recover pose from a measured coupling vector `z` via Levenberg-Marquardt.

    Minimises the whitened residual (h(x) - z)/sigma (Ch. 23, eq. 23.2), seeded
    from `x0`. Returns the estimated pose x_hat = [p(3), rotvec(3)].
    """
    def residual(x):
        return (forward_model(x, na_s, m_t) - z) / sigma

    result = least_squares(residual, np.asarray(x0, float), method="lm", max_nfev=2000)
    return result.x
