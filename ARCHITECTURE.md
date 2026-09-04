# Architecture

## Layer 1 — operator access

`bclosure.operators.LinearOperator` defines `matvec`, `rmatvec`, `matmat`, shape, and dtype. Concrete adapters support explicit arrays and callables.

## Layer 2 — hierarchy

`bclosure.trees.ClusterTree` describes balanced or learned partitions. Complementary block pairs are generated from level \(\ell\) on the output side and level \(L-\ell\) on the input side.

## Layer 3 — observatory

`inspect_closure` estimates numerical ranks and tail energies for sampled complementary blocks. The report includes uncertainty and a compile/reject recommendation.

## Layer 4 — compiler

The compiler owns three distinct paths:

1. exact factories for known structured operators;
2. algebraic initialization from block low-rank decompositions;
3. learned refinement under fixed, chainable sparsity supports.

The present repository implements path 1 and the factor-chain runtime. Paths 2 and 3 are work packages.

## Layer 5 — residual engine

The deployed approximation is

\[
\widehat A = A_{\mathrm{BF}} + R_{\mathrm{LR}} + R_{\mathrm{SP}} + R_{\mathrm{K}},
\]

with each term optional. Residual work must remain cheaper than the butterfly core in the claimed operating regime.

## Layer 6 — certification

Certification escalates from random probes to block Lanczos/power iterations, adjoint checks, and downstream task checks. A compiler result is not deployable until its certificate is serializable.

## Layer 7 — hardware runtime

The reference NumPy path establishes correctness. Production paths may use PyTorch, Triton, CUDA, or custom extensions, but must preserve equivalent semantics and reference tests.

## Layer 8 — adaptive controller

A no-regret controller may select dense, butterfly, or corrected execution based on state, predicted cost, and observed utility. The controller must include a safe dense fallback.

## Dependency direction

```text
operators <- trees <- probes <- reports
operators <- factorization <- certification
operators <- krylov <- layers
reports + factorization + certification <- cli/benchmarks
```

Circular dependencies are prohibited.
