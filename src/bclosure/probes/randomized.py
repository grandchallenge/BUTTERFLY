from __future__ import annotations

from dataclasses import dataclass
from typing import Any, cast

import numpy as np
from numpy.typing import NDArray

from bclosure.operators.base import LinearOperator


@dataclass(frozen=True)
class BlockRankEstimate:
    rank: int
    singular_values: NDArray[np.float64]
    tail_energy: float
    rows: tuple[int, ...]
    cols: tuple[int, ...]


def _materialize_block(
    operator: LinearOperator,
    rows: NDArray[np.int64],
    cols: NDArray[np.int64],
) -> NDArray[Any]:
    explicit = getattr(operator, "matrix", None)
    if explicit is not None:
        return cast(NDArray[Any], np.asarray(explicit)[np.ix_(rows, cols)])
    basis = np.zeros((operator.shape[1], len(cols)), dtype=operator.dtype)
    basis[cols, np.arange(len(cols))] = 1
    return operator.matmat(basis)[rows, :]


def estimate_block_rank(
    operator: LinearOperator,
    rows: NDArray[np.int64],
    cols: NDArray[np.int64],
    tolerance: float,
    rank_budget: int,
    oversampling: int = 8,
    seed: int = 0,
    exact_threshold: int = 262_144,
) -> BlockRankEstimate:
    """Estimate relative numerical rank for one block.

    Small blocks are materialized exactly. Large blocks use a randomized range sketch,
    preserving matrix-free access to the full operator.
    """
    if tolerance <= 0:
        raise ValueError("tolerance must be positive")
    if rank_budget <= 0:
        raise ValueError("rank_budget must be positive")
    m, n = len(rows), len(cols)
    if m == 0 or n == 0:
        return BlockRankEstimate(0, np.zeros(0), 0.0, tuple(rows), tuple(cols))

    if m * n <= exact_threshold:
        block = _materialize_block(operator, rows, cols)
        singular = np.linalg.svd(block, compute_uv=False).astype(np.float64)
    else:
        rng = np.random.default_rng(seed)
        width = min(n, rank_budget + oversampling)
        omega_local = rng.standard_normal((n, width))
        omega = np.zeros((operator.shape[1], width), dtype=operator.dtype)
        omega[cols, :] = omega_local
        y = operator.matmat(omega)[rows, :]
        q, _ = np.linalg.qr(y, mode="reduced")
        # Project through the adjoint without materializing the full matrix.
        q_full = np.zeros((operator.shape[0], q.shape[1]), dtype=operator.dtype)
        q_full[rows, :] = q
        b = operator.rmatmat(q_full)[cols, :].conj().T
        singular = np.linalg.svd(b, compute_uv=False).astype(np.float64)

    if singular.size == 0 or singular[0] == 0:
        rank = 0
    else:
        rank = int(np.count_nonzero(singular > tolerance * singular[0]))

    retained = min(rank_budget, singular.size)
    denom = float(np.sum(singular**2))
    tail = float(np.sum(singular[retained:] ** 2) / denom) if denom > 0 else 0.0
    return BlockRankEstimate(rank, singular, tail, tuple(map(int, rows)), tuple(map(int, cols)))
