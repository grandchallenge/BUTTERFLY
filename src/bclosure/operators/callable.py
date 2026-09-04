from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import numpy as np

from bclosure.exceptions import AdjointUnavailable

from .base import DEFAULT_DTYPE, Array, LinearOperator


@dataclass(frozen=True, init=False)
class CallableLinearOperator(LinearOperator):
    _forward: Callable[[Array], Array]
    _adjoint: Callable[[Array], Array] | None

    def __init__(
        self,
        shape: tuple[int, int],
        forward: Callable[[Array], Array],
        adjoint: Callable[[Array], Array] | None = None,
        dtype: np.dtype[Any] = DEFAULT_DTYPE,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        object.__setattr__(self, "shape", shape)
        object.__setattr__(self, "dtype", np.dtype(dtype))
        object.__setattr__(self, "metadata", metadata or {})
        object.__setattr__(self, "_forward", forward)
        object.__setattr__(self, "_adjoint", adjoint)
        LinearOperator.__post_init__(self)

    def matvec(self, vector: Array) -> Array:
        result = np.asarray(self._forward(np.asarray(vector)))
        if result.shape != (self.shape[0],):
            raise ValueError(f"forward returned {result.shape}, expected {(self.shape[0],)}")
        return result

    def rmatvec(self, vector: Array) -> Array:
        if self._adjoint is None:
            raise AdjointUnavailable("operator was constructed without an adjoint")
        result = np.asarray(self._adjoint(np.asarray(vector)))
        if result.shape != (self.shape[1],):
            raise ValueError(f"adjoint returned {result.shape}, expected {(self.shape[1],)}")
        return result
