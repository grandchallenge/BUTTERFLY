import numpy as np
from scipy.linalg import hadamard

from bclosure.certification import certify_operator
from bclosure.factorization.hadamard import HadamardButterflyOperator
from bclosure.operators.dense import DenseLinearOperator


def test_exact_hadamard_certificate() -> None:
    n = 64
    target = DenseLinearOperator(hadamard(n) / np.sqrt(n))
    approximation = HadamardButterflyOperator(n)
    certificate = certify_operator(target, approximation, probes=8, seed=0)
    assert certificate.forward_relative_error < 1e-12
    assert certificate.adjoint_relative_error < 1e-12
    assert certificate.bilinear_adjoint_error < 1e-12
