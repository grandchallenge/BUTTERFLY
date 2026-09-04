from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from bclosure.operators.base import LinearOperator


@dataclass(frozen=True)
class CGResult:
    solution: NDArray[np.generic]
    converged: bool
    iterations: int
    residual_norms: tuple[float, ...]


def conjugate_gradient(
    operator: LinearOperator,
    rhs: NDArray[np.generic],
    x0: NDArray[np.generic] | None = None,
    tolerance: float = 1e-6,
    max_iterations: int = 32,
) -> CGResult:
    """Reference conjugate-gradient solve for Hermitian positive-definite operators."""
    b = np.asarray(rhs)
    x = np.zeros_like(b) if x0 is None else np.asarray(x0).copy()
    r = b - operator.matvec(x)
    p = r.copy()
    rr = np.vdot(r, r)
    norms = [float(np.sqrt(np.real(rr)))]
    if norms[-1] <= tolerance:
        return CGResult(x, True, 0, tuple(norms))

    for iteration in range(1, max_iterations + 1):
        ap = operator.matvec(p)
        denom = np.vdot(p, ap)
        if abs(denom) < 1e-30:
            break
        alpha = rr / denom
        x = x + alpha * p
        r = r - alpha * ap
        rr_new = np.vdot(r, r)
        norm = float(np.sqrt(max(float(np.real(rr_new)), 0.0)))
        norms.append(norm)
        if norm <= tolerance:
            return CGResult(x, True, iteration, tuple(norms))
        beta = rr_new / rr
        p = r + beta * p
        rr = rr_new
    return CGResult(x, False, len(norms) - 1, tuple(norms))
