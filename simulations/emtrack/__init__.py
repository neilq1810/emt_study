"""emtrack — reference simulation library for the EM-Tracking-Definitive-Guide.

Pure NumPy/SciPy implementations of the physics and estimation used in the book:
magnetic dipole and finite-loop fields (Ch. 4), the coupling tensor/matrix
(Ch. 5), a Levenberg-Marquardt pose solver (Ch. 23), and Fisher-information /
CRLB analysis (Ch. 24).  These back the figures (/figures) and computed numbers
(/data) and are deliberately small and readable rather than optimized.
"""

from .fields import MU0, magnetic_moment, dipole_field, loop_field_onaxis, loop_field_offaxis
from .coupling import coupling_tensor, coupling_matrix, forward_model
from .solver import solve_pose
from .crlb import jacobian, fisher_information, crlb_position_sigma

__all__ = [
    "MU0",
    "magnetic_moment",
    "dipole_field",
    "loop_field_onaxis",
    "loop_field_offaxis",
    "coupling_tensor",
    "coupling_matrix",
    "forward_model",
    "solve_pose",
    "jacobian",
    "fisher_information",
    "crlb_position_sigma",
]
