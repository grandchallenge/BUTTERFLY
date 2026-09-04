from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
from numpy.typing import NDArray

from bclosure.operators.base import Array, LinearOperator


@dataclass(frozen=True)
class DenseFactor:
    """Reference factor; production work replaces this with block-sparse storage."""

    matrix: NDArray[Any]

    def __post_init__(self) -> None:
        if self.matrix.ndim != 2:
            raise ValueError("factor must be two-dimensional")

    @property
    def shape(self) -> tuple[int, int]:
        return int(self.matrix.shape[0]), int(self.matrix.shape[1])

    def forward(self, x: Array) -> Array:
        return self.matrix @ x

    def adjoint(self, x: Array) -> Array:
        return self.matrix.conj().T @ x


@dataclass(frozen=True, init=False)
class FactorChainOperator(LinearOperator):
    factors: tuple[DenseFactor, ...]

    def __init__(self, factors: tuple[DenseFactor, ...]) -> None:
        if not factors:
            raise ValueError("at least one factor is required")
        for left, right in zip(factors[1:], factors[:-1], strict=True):
            if left.shape[1] != right.shape[0]:
                raise ValueError(f"incompatible factors: {left.shape} after {right.shape}")
        object.__setattr__(self, "factors", factors)
        object.__setattr__(self, "shape", (factors[-1].shape[0], factors[0].shape[1]))
        object.__setattr__(self, "dtype", np.result_type(*[f.matrix.dtype for f in factors]))
        object.__setattr__(self, "metadata", {"factor_count": len(factors)})
        LinearOperator.__post_init__(self)

    def matvec(self, vector: Array) -> Array:
        x = np.asarray(vector)
        for factor in self.factors:
            x = factor.forward(x)
        return x

    def rmatvec(self, vector: Array) -> Array:
        x = np.asarray(vector)
        for factor in reversed(self.factors):
            x = factor.adjoint(x)
        return x
