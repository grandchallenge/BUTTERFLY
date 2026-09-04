from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from bclosure.exceptions import CompilationRejected
from bclosure.factorization.hadamard import HadamardButterflyOperator
from bclosure.inspection import ClosureReport
from bclosure.operators.base import LinearOperator


@dataclass(frozen=True)
class CompilationProvenance:
    method: str
    target_fingerprint: str
    settings: dict[str, Any]


@dataclass(frozen=True)
class CompiledButterfly:
    operator: LinearOperator
    provenance: CompilationProvenance


def compile_known_operator(kind: str, size: int) -> CompiledButterfly:
    normalized = kind.strip().lower()
    if normalized == "hadamard":
        operator = HadamardButterflyOperator(size)
        return CompiledButterfly(
            operator=operator,
            provenance=CompilationProvenance(
                method="exact-hadamard-factory",
                target_fingerprint=f"hadamard:{size}",
                settings={"normalized": True},
            ),
        )
    raise CompilationRejected(f"no exact compiler registered for operator kind {kind!r}")


def require_closure(report: ClosureReport) -> None:
    if not report.accepted:
        raise CompilationRejected(report.reason)


def compile_butterfly(target: LinearOperator, report: ClosureReport) -> CompiledButterfly:
    """Research compiler entry point.

    The contract and rejection path are operational. Generic algebraic compilation is a
    designated work package and deliberately not replaced by a silent dense fallback.
    """
    require_closure(report)
    raise NotImplementedError(
        "BFC-TODO WP3: implement generic algebraic initialization and sparse factor sweeping; "
        "use compile_known_operator for canonical exact factories"
    )
