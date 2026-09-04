from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import numpy as np

from bclosure.operators.base import LinearOperator


@dataclass(frozen=True)
class OperatorCertificate:
    forward_relative_error: float
    adjoint_relative_error: float
    bilinear_adjoint_error: float
    probes: int
    seed: int
    target_fingerprint: str
    approximation_fingerprint: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def certify_operator(
    target: LinearOperator,
    approximation: LinearOperator,
    probes: int = 16,
    seed: int = 0,
) -> OperatorCertificate:
    if target.shape != approximation.shape:
        raise ValueError("target and approximation shapes differ")
    rng = np.random.default_rng(seed)
    forward_num = forward_den = 0.0
    adj_num = adj_den = 0.0
    bilinear = 0.0
    for _ in range(probes):
        x = rng.standard_normal(target.shape[1])
        y = rng.standard_normal(target.shape[0])
        tx = target.matvec(x)
        ax = approximation.matvec(x)
        ty = target.rmatvec(y)
        ay = approximation.rmatvec(y)
        forward_num += float(np.linalg.norm(tx - ax) ** 2)
        forward_den += float(np.linalg.norm(tx) ** 2)
        adj_num += float(np.linalg.norm(ty - ay) ** 2)
        adj_den += float(np.linalg.norm(ty) ** 2)
        left = np.vdot(approximation.matvec(x), y)
        right = np.vdot(x, approximation.rmatvec(y))
        scale = abs(left) + abs(right) + 1e-15
        bilinear = max(bilinear, float(abs(left - right) / scale))
    return OperatorCertificate(
        forward_relative_error=float(np.sqrt(forward_num / max(forward_den, 1e-30))),
        adjoint_relative_error=float(np.sqrt(adj_num / max(adj_den, 1e-30))),
        bilinear_adjoint_error=bilinear,
        probes=probes,
        seed=seed,
        target_fingerprint=target.fingerprint(),
        approximation_fingerprint=approximation.fingerprint(),
    )
