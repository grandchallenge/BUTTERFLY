from __future__ import annotations

from dataclasses import asdict, dataclass
from time import perf_counter
from typing import Any

import numpy as np

from bclosure.operators.base import LinearOperator


@dataclass(frozen=True)
class BenchmarkResult:
    size: int
    repetitions: int
    warmup: int
    seconds_total: float
    seconds_per_apply: float
    output_norm: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def benchmark_operator(
    operator: LinearOperator,
    repetitions: int = 50,
    warmup: int = 5,
    seed: int = 0,
) -> BenchmarkResult:
    rng = np.random.default_rng(seed)
    x = rng.standard_normal(operator.shape[1]).astype(operator.dtype)
    for _ in range(warmup):
        operator.matvec(x)
    start = perf_counter()
    y = x
    for _ in range(repetitions):
        y = operator.matvec(x)
    elapsed = perf_counter() - start
    return BenchmarkResult(
        size=operator.shape[1],
        repetitions=repetitions,
        warmup=warmup,
        seconds_total=elapsed,
        seconds_per_apply=elapsed / repetitions,
        output_norm=float(np.linalg.norm(y)),
    )
