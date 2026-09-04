from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

import numpy as np
from numpy.typing import NDArray

Array = NDArray[Any]
DEFAULT_DTYPE = np.dtype(np.float64)


@dataclass(frozen=True, kw_only=True)
class LinearOperator(ABC):
    """Matrix-free linear operator contract.

    Shape follows NumPy convention: `(output_dim, input_dim)`.
    """

    shape: tuple[int, int]
    dtype: np.dtype[Any] = DEFAULT_DTYPE
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if len(self.shape) != 2 or min(self.shape) <= 0:
            raise ValueError(f"invalid operator shape: {self.shape}")

    @abstractmethod
    def matvec(self, vector: Array) -> Array:
        """Apply the operator to one vector."""

    @abstractmethod
    def rmatvec(self, vector: Array) -> Array:
        """Apply the conjugate transpose to one vector."""

    def matmat(self, matrix: Array) -> Array:
        x = np.asarray(matrix)
        if x.ndim != 2 or x.shape[0] != self.shape[1]:
            raise ValueError(f"expected ({self.shape[1]}, k), got {x.shape}")
        return np.column_stack([self.matvec(x[:, j]) for j in range(x.shape[1])])

    def rmatmat(self, matrix: Array) -> Array:
        x = np.asarray(matrix)
        if x.ndim != 2 or x.shape[0] != self.shape[0]:
            raise ValueError(f"expected ({self.shape[0]}, k), got {x.shape}")
        return np.column_stack([self.rmatvec(x[:, j]) for j in range(x.shape[1])])

    def fingerprint(self) -> str:
        return f"{type(self).__name__}:{self.shape}:{self.dtype.str}:{sorted(self.metadata.items())}"
