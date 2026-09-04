from __future__ import annotations

import numpy as np

from bclosure.certification import certify_operator
from bclosure.inspection import inspect_closure
from bclosure.operators.dense import DenseLinearOperator


def test_complex_rectangular_adjoint_and_deterministic_inspection() -> None:
    rng = np.random.default_rng(17)
    matrix = rng.standard_normal((8, 16)) + 1j * rng.standard_normal((8, 16))
    operator = DenseLinearOperator(matrix)
    first = inspect_closure(operator, rank_budget=2, blocks_per_level=4, seed=23)
    second = inspect_closure(operator, rank_budget=2, blocks_per_level=4, seed=23)
    assert first.operator_fingerprint == second.operator_fingerprint
    assert first.max_rank == second.max_rank
    assert first.mean_rank == second.mean_rank
    assert first.max_tail_energy == second.max_tail_energy
    assert len(first.estimates) == len(second.estimates)
    for left, right in zip(first.estimates, second.estimates, strict=True):
        assert left.rank == right.rank
        assert left.rows == right.rows
        assert left.cols == right.cols
        assert left.tail_energy == right.tail_energy
        assert np.array_equal(left.singular_values, right.singular_values)

    x = rng.standard_normal(16) + 1j * rng.standard_normal(16)
    y = rng.standard_normal(8) + 1j * rng.standard_normal(8)
    assert np.allclose(np.vdot(operator.matvec(x), y), np.vdot(x, operator.rmatvec(y)))


def test_hidden_direction_is_detected_when_explicitly_probed() -> None:
    target_matrix = np.eye(16)
    approximation_matrix = target_matrix.copy()
    approximation_matrix[-1, -1] = 0.0
    target = DenseLinearOperator(target_matrix)
    approximation = DenseLinearOperator(approximation_matrix)
    certificate = certify_operator(target, approximation, probes=128, seed=31)
    assert certificate.forward_relative_error > 0.1
    assert certificate.adjoint_relative_error > 0.1


def test_dense_fingerprint_is_content_addressed_and_matrix_is_immutable() -> None:
    first_matrix = np.eye(4)
    second_matrix = np.eye(4)
    second_matrix[0, 0] = 2.0
    first = DenseLinearOperator(first_matrix)
    second = DenseLinearOperator(second_matrix)
    assert first.fingerprint().startswith("sha256:")
    assert first.fingerprint() != second.fingerprint()
    first_matrix[0, 0] = 9.0
    assert first.fingerprint() != DenseLinearOperator(first_matrix).fingerprint()
    with np.testing.assert_raises(ValueError):
        first.matrix[0, 0] = 7.0
    with np.testing.assert_raises(ValueError):
        first.matrix.setflags(write=True)
