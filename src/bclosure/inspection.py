from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import numpy as np

from bclosure.operators.base import LinearOperator
from bclosure.probes.randomized import BlockRankEstimate, estimate_block_rank
from bclosure.trees.balanced import ClusterTree, balanced_binary_tree


@dataclass(frozen=True)
class ClosureReport:
    operator_fingerprint: str
    tolerance: float
    rank_budget: int
    estimates: tuple[BlockRankEstimate, ...]
    max_rank: int
    mean_rank: float
    max_tail_energy: float
    accepted: bool
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def inspect_closure(
    operator: LinearOperator,
    input_tree: ClusterTree | None = None,
    output_tree: ClusterTree | None = None,
    tolerance: float = 1e-4,
    rank_budget: int = 16,
    blocks_per_level: int | None = 16,
    oversampling: int = 8,
    seed: int = 0,
) -> ClosureReport:
    output_dim, input_dim = operator.shape
    if input_tree is None:
        input_tree = balanced_binary_tree(input_dim)
    if output_tree is None:
        output_tree = balanced_binary_tree(output_dim)
    depth = min(input_tree.depth, output_tree.depth)
    rng = np.random.default_rng(seed)
    estimates: list[BlockRankEstimate] = []

    for level in range(depth + 1):
        rows = output_tree.at(level)
        cols = input_tree.at(depth - level)
        pairs = [(r, c) for r in rows for c in cols]
        if blocks_per_level is not None and len(pairs) > blocks_per_level:
            selected = rng.choice(len(pairs), size=blocks_per_level, replace=False)
            pairs = [pairs[int(i)] for i in selected]
        for pair_idx, (row_cluster, col_cluster) in enumerate(pairs):
            estimates.append(
                estimate_block_rank(
                    operator,
                    row_cluster.indices,
                    col_cluster.indices,
                    tolerance=tolerance,
                    rank_budget=rank_budget,
                    oversampling=oversampling,
                    seed=seed + 104729 * level + pair_idx,
                )
            )

    max_rank = max((e.rank for e in estimates), default=0)
    mean_rank = float(np.mean([e.rank for e in estimates])) if estimates else 0.0
    max_tail = max((e.tail_energy for e in estimates), default=0.0)
    accepted = max_rank <= rank_budget
    reason = (
        f"measured maximum complementary rank {max_rank} <= budget {rank_budget}"
        if accepted
        else f"measured maximum complementary rank {max_rank} exceeds budget {rank_budget}"
    )
    return ClosureReport(
        operator_fingerprint=operator.fingerprint(),
        tolerance=tolerance,
        rank_budget=rank_budget,
        estimates=tuple(estimates),
        max_rank=max_rank,
        mean_rank=mean_rank,
        max_tail_energy=max_tail,
        accepted=accepted,
        reason=reason,
    )
