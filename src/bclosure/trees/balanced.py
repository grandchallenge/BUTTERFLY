from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


@dataclass(frozen=True)
class Cluster:
    level: int
    ordinal: int
    indices: NDArray[np.int64]


@dataclass(frozen=True)
class ClusterTree:
    size: int
    levels: tuple[tuple[Cluster, ...], ...]
    ordering: str = "natural"

    @property
    def depth(self) -> int:
        return len(self.levels) - 1

    def at(self, level: int) -> tuple[Cluster, ...]:
        return self.levels[level]


def bit_reversal_order(size: int) -> NDArray[np.int64]:
    if size <= 0 or size & (size - 1):
        raise ValueError("bit-reversal ordering requires a positive power-of-two size")
    bits = size.bit_length() - 1
    return np.asarray(
        [int(f"{index:0{bits}b}"[::-1], 2) for index in range(size)], dtype=np.int64
    )


def balanced_binary_tree(
    size: int,
    max_depth: int | None = None,
    order: NDArray[np.int64] | None = None,
    ordering: str = "natural",
) -> ClusterTree:
    if size <= 0:
        raise ValueError("size must be positive")
    if max_depth is None:
        max_depth = int(np.floor(np.log2(size)))
    if max_depth < 0:
        raise ValueError("max_depth must be nonnegative")

    root = np.arange(size, dtype=np.int64) if order is None else np.asarray(order, dtype=np.int64)
    if root.shape != (size,) or np.unique(root).size != size or min(root) < 0 or max(root) >= size:
        raise ValueError("order must be a permutation of range(size)")
    levels: list[tuple[Cluster, ...]] = []
    current = [root]
    for level in range(max_depth + 1):
        levels.append(
            tuple(Cluster(level=level, ordinal=i, indices=idx) for i, idx in enumerate(current))
        )
        if level == max_depth:
            break
        next_level: list[NDArray[np.int64]] = []
        for idx in current:
            left, right = np.array_split(idx, 2)
            if left.size:
                next_level.append(left)
            if right.size:
                next_level.append(right)
        current = next_level
    return ClusterTree(size=size, levels=tuple(levels), ordering=ordering)


def tree_from_ordering(size: int, ordering: str) -> ClusterTree:
    normalized = ordering.strip().lower()
    if normalized == "natural":
        return balanced_binary_tree(size, ordering="natural")
    if normalized in {"bit_reversal", "bit-reversal", "bitreverse"}:
        return balanced_binary_tree(
            size, order=bit_reversal_order(size), ordering="bit_reversal"
        )
    raise ValueError(f"unknown tree ordering: {ordering!r}")
