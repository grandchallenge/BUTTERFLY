import numpy as np

from bclosure.operators.dense import DenseLinearOperator


def test_dense_adjoint_bilinear_identity() -> None:
    rng = np.random.default_rng(0)
    matrix = rng.standard_normal((17, 13))
    operator = DenseLinearOperator(matrix)
    x = rng.standard_normal(13)
    y = rng.standard_normal(17)
    left = np.vdot(operator.matvec(x), y)
    right = np.vdot(x, operator.rmatvec(y))
    np.testing.assert_allclose(left, right, rtol=1e-12, atol=1e-12)
