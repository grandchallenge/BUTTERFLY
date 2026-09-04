from __future__ import annotations

import platform
import subprocess
import sys
from dataclasses import asdict, dataclass
from time import perf_counter
from typing import Any

import numpy as np
import scipy

from bclosure.operators.base import LinearOperator


@dataclass(frozen=True)
class BenchmarkResult:
    git_commit: str
    git_dirty: bool
    python_version: str
    numpy_version: str
    scipy_version: str
    platform: str
    machine: str
    processor: str
    operator_fingerprint: str
    shape: tuple[int, int]
    dtype: str
    seed: int
    size: int
    repetitions: int
    warmup: int
    seconds_total: float
    seconds_per_apply: float
    output_norm: float
    compilation_seconds: float
    parameter_count: int | None
    nonzero_count: int | None
    estimated_flops_per_apply: int | None
    storage_bytes: int | None
    operator_error: float | None
    task_delta: float | None
    break_even_horizon: int | None
    artifact_path: str | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def benchmark_operator(
    operator: LinearOperator,
    repetitions: int = 50,
    warmup: int = 5,
    seed: int = 0,
    artifact_path: str | None = None,
) -> BenchmarkResult:
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], capture_output=True, check=False, text=True
    ).stdout.strip() or "unavailable"
    dirty = bool(
        subprocess.run(
            [
                "git", "status", "--porcelain", "--untracked-files=no", "--", ".",
                ":(exclude)artifacts/**",
            ],
            capture_output=True,
            check=False,
            text=True,
        ).stdout.strip()
    )
    rng = np.random.default_rng(seed)
    x = rng.standard_normal(operator.shape[1]).astype(operator.dtype)
    for _ in range(warmup):
        operator.matvec(x)
    start = perf_counter()
    y = x
    for _ in range(repetitions):
        y = operator.matvec(x)
    elapsed = perf_counter() - start
    matrix = getattr(operator, "matrix", None)
    parameter_count = int(matrix.size) if isinstance(matrix, np.ndarray) else None
    nonzero_count = int(np.count_nonzero(matrix)) if isinstance(matrix, np.ndarray) else None
    storage_bytes = int(matrix.nbytes) if isinstance(matrix, np.ndarray) else None
    flops = 2 * operator.shape[0] * operator.shape[1] if matrix is not None else None
    return BenchmarkResult(
        git_commit=commit,
        git_dirty=dirty,
        python_version=sys.version.split()[0],
        numpy_version=np.__version__,
        scipy_version=scipy.__version__,
        platform=platform.platform(),
        machine=platform.machine(),
        processor=platform.processor() or "unavailable",
        operator_fingerprint=operator.fingerprint(),
        shape=operator.shape,
        dtype=operator.dtype.str,
        seed=seed,
        size=operator.shape[1],
        repetitions=repetitions,
        warmup=warmup,
        seconds_total=elapsed,
        seconds_per_apply=elapsed / repetitions,
        output_norm=float(np.linalg.norm(y)),
        compilation_seconds=0.0,
        parameter_count=parameter_count,
        nonzero_count=nonzero_count,
        estimated_flops_per_apply=flops,
        storage_bytes=storage_bytes,
        operator_error=None,
        task_delta=None,
        break_even_horizon=None,
        artifact_path=artifact_path.replace("\\", "/") if artifact_path else None,
    )
