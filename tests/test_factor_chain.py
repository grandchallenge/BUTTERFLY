import numpy as np

from bclosure.factorization.factor_chain import DenseFactor, FactorChainOperator


def test_factor_chain_forward_and_adjoint() -> None:
    rng = np.random.default_rng(0)
    a = rng.standard_normal((7, 5))
    b = rng.standard_normal((11, 7))
    chain = FactorChainOperator((DenseFactor(a), DenseFactor(b)))
    x = rng.standard_normal(5)
    y = rng.standard_normal(11)
    np.testing.assert_allclose(chain.matvec(x), b @ a @ x)
    np.testing.assert_allclose(chain.rmatvec(y), a.T @ b.T @ y)
