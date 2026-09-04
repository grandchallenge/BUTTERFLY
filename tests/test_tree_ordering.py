from bclosure.factorization.hadamard import HadamardButterflyOperator
from bclosure.inspection import inspect_closure
from bclosure.trees import tree_from_ordering


def test_bit_reversal_exposes_hadamard_rank_one_closure() -> None:
    n = 128
    report = inspect_closure(
        HadamardButterflyOperator(n),
        input_tree=tree_from_ordering(n, "natural"),
        output_tree=tree_from_ordering(n, "bit_reversal"),
        tolerance=1e-10,
        rank_budget=1,
        blocks_per_level=None,
        seed=0,
    )
    assert report.accepted
    assert report.max_rank == 1
