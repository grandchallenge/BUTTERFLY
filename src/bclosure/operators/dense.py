from __future__ import annotations

from dataclasses import dataclass
from typing import Any, cast

import numpy as np
from numpy.typing import NDArray

from .base import Array, LinearOperator


@dataclass(frozen=True, init=False)
class DenseLinearOperator(LinearOperator):
    matrix: NDArray[Any]

    def __init__(self, matrix: Array, metadata: dict[str, Any] | None = None) -> None:
        a = np.asarray(matrix)
        if a.ndim != 2:
            raise ValueError("matrix must be two-dimensional")
        object.__setattr__(self, "matrix", a)
        object.__setattr__(self, "shape", (int(a.shape[0]), int(a.shape[1])))
        object.__setattr__(self, "dtype", a.dtype)
        object.__setattr__(self, "metadata", metadata or {})
        LinearOperator.__post_init__(self)

    def matvec(self, vector: Array) -> Array:
        x = np.asarray(vector)
        if x.shape != (self.shape[1],):
            raise ValueError(f"expected {(self.shape[1],)}, got {x.shape}")
        return cast(Array, self.matrix @ x)

    def rmatvec(self, vector: Array) -> Array:
        x = np.asarray(vector)
        if x.shape != (self.shape[0],):
            raise ValueError(f"expected {(self.shape[0],)}, got {x.shape}")
        return cast(Array, self.matrix.conj().T @ x)
