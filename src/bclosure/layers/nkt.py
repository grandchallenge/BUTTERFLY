from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from bclosure.operators.base import Array, LinearOperator


@dataclass(frozen=True, init=False)
class NormalEquationOperator(LinearOperator):
    """A = damping * I + B* B, the core Butterfly NKT solve operator."""

    transport: LinearOperator
    damping: float

    def __init__(self, transport: LinearOperator, damping: float = 1e-3) -> None:
        if damping <= 0:
            raise ValueError("damping must be positive")
        input_dim = transport.shape[1]
        object.__setattr__(self, "transport", transport)
        object.__setattr__(self, "damping", damping)
        object.__setattr__(self, "shape", (input_dim, input_dim))
        object.__setattr__(self, "dtype", transport.dtype)
        object.__setattr__(self, "metadata", {"damping": damping})
        LinearOperator.__post_init__(self)

    def matvec(self, vector: Array) -> Array:
        x = np.asarray(vector)
        return self.damping * x + self.transport.rmatvec(self.transport.matvec(x))

    def rmatvec(self, vector: Array) -> Array:
        return self.matvec(vector)
