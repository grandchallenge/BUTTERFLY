import numpy as np

from bclosure.inspection import inspect_closure
from bclosure.operators.dense import DenseLinearOperator


def test_global_low_rank_operator_is_accepted() -> None:
    rng = np.random.default_rng(0)
    n, rank = 128, 4
    matrix = rng.standard_normal((n, rank)) @ rng.standard_normal((rank, n))
    report = inspect_closure(
        DenseLinearOperator(matrix),
        tolerance=1e-10,
        rank_budget=rank,
        blocks_per_level=4,
        seed=0,
    )
    assert report.accepted
    assert report.max_rank <= rank


def test_random_dense_operator_rejected_under_small_budget() -> None:
    rng = np.random.default_rng(1)
    n = 128
    matrix = rng.standard_normal((n, n))
    report = inspect_closure(
        DenseLinearOperator(matrix),
        tolerance=1e-3,
        rank_budget=2,
        blocks_per_level=8,
        seed=0,
    )
    assert not report.accepted
    assert report.max_rank > 2
