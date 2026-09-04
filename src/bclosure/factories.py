from __future__ import annotations

from typing import Any, cast

import numpy as np
from scipy.linalg import hadamard

from bclosure.factorization.hadamard import HadamardButterflyOperator
from bclosure.operators.base import LinearOperator
from bclosure.operators.dense import DenseLinearOperator


def make_operator(spec: dict[str, object]) -> LinearOperator:
    kind = str(spec.get("kind", "")).lower()
    size = int(cast(Any, spec.get("size", 0)))
    seed = int(cast(Any, spec.get("seed", 0)))
    if kind == "hadamard_butterfly":
        return HadamardButterflyOperator(size)
    if kind == "hadamard_dense":
        matrix = hadamard(size).astype(np.float64) / np.sqrt(size)
        return DenseLinearOperator(matrix, metadata={"kind": kind})
    if kind == "random_dense":
        rng = np.random.default_rng(seed)
        matrix = rng.standard_normal((size, size)) / np.sqrt(size)
        return DenseLinearOperator(matrix, metadata={"kind": kind, "seed": seed})
    if kind == "global_low_rank":
        rank = int(cast(Any, spec.get("rank", 8)))
        rng = np.random.default_rng(seed)
        left = rng.standard_normal((size, rank))
        right = rng.standard_normal((size, rank))
        return DenseLinearOperator(left @ right.T / np.sqrt(rank), metadata={"kind": kind})
    raise ValueError(f"unknown operator kind: {kind!r}")
