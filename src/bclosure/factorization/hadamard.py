from __future__ import annotations

from dataclasses import dataclass
from typing import Any, cast

import numpy as np

from bclosure.operators.base import DEFAULT_DTYPE, Array, LinearOperator


@dataclass(frozen=True, init=False)
class HadamardButterflyOperator(LinearOperator):
    """Exact normalized Walsh-Hadamard transform in O(N log N)."""

    size: int

    def __init__(self, size: int, dtype: np.dtype[Any] = DEFAULT_DTYPE) -> None:
        if size <= 0 or size & (size - 1):
            raise ValueError("size must be a positive power of two")
        object.__setattr__(self, "size", size)
        object.__setattr__(self, "shape", (size, size))
        object.__setattr__(self, "dtype", np.dtype(dtype))
        object.__setattr__(self, "metadata", {"normalized": True, "depth": size.bit_length() - 1})
        LinearOperator.__post_init__(self)

    def _apply_matrix(self, matrix: Array) -> Array:
        x = np.asarray(matrix, dtype=self.dtype).copy()
        if x.ndim != 2 or x.shape[0] != self.size:
            raise ValueError(f"expected ({self.size}, k), got {x.shape}")
        width = x.shape[1]
        stride = 1
        while stride < self.size:
            view = x.reshape(-1, 2, stride, width)
            left = view[:, 0, :, :].copy()
            right = view[:, 1, :, :].copy()
            view[:, 0, :, :] = left + right
            view[:, 1, :, :] = left - right
            stride *= 2
        return cast(Array, x / np.sqrt(self.size))

    def matvec(self, vector: Array) -> Array:
        x = np.asarray(vector)
        if x.shape != (self.size,):
            raise ValueError(f"expected {(self.size,)}, got {x.shape}")
        return self._apply_matrix(x[:, None])[:, 0]

    def rmatvec(self, vector: Array) -> Array:
        # The normalized Hadamard transform is real, symmetric, and orthogonal.
        return self.matvec(vector)

    def matmat(self, matrix: Array) -> Array:
        return self._apply_matrix(matrix)

    def rmatmat(self, matrix: Array) -> Array:
        return self._apply_matrix(matrix)
