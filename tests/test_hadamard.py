import numpy as np
from scipy.linalg import hadamard

from bclosure.factorization.hadamard import HadamardButterflyOperator


def test_hadamard_matches_dense() -> None:
    size = 64
    operator = HadamardButterflyOperator(size)
    rng = np.random.default_rng(0)
    x = rng.standard_normal(size)
    expected = hadamard(size) @ x / np.sqrt(size)
    np.testing.assert_allclose(operator.matvec(x), expected, rtol=1e-12, atol=1e-12)


def test_hadamard_is_self_adjoint_and_orthogonal() -> None:
    size = 128
    operator = HadamardButterflyOperator(size)
    rng = np.random.default_rng(1)
    x = rng.standard_normal(size)
    np.testing.assert_allclose(operator.rmatvec(x), operator.matvec(x), atol=1e-12)
    np.testing.assert_allclose(operator.matvec(operator.matvec(x)), x, atol=1e-12)
