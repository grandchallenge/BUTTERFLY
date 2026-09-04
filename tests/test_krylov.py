import numpy as np

from bclosure.krylov.cg import conjugate_gradient
from bclosure.operators.dense import DenseLinearOperator


def test_conjugate_gradient_solves_spd_system() -> None:
    rng = np.random.default_rng(0)
    q = rng.standard_normal((32, 32))
    matrix = q.T @ q + 0.5 * np.eye(32)
    rhs = rng.standard_normal(32)
    result = conjugate_gradient(
        DenseLinearOperator(matrix), rhs, tolerance=1e-10, max_iterations=64
    )
    expected = np.linalg.solve(matrix, rhs)
    assert result.converged
    np.testing.assert_allclose(result.solution, expected, rtol=1e-8, atol=1e-8)
