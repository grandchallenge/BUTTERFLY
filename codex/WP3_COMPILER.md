# WP3 — Generic Butterfly Compiler

Implement the generic compiler currently marked `BFC-TODO`.

Required sequence:

1. Define block-sparse factor storage and exact adjoint traversal.
2. Implement middle-level randomized low-rank decomposition.
3. Sweep factorizations toward input and output leaves while sharing bases.
4. Add interpolative-decomposition initialization.
5. Add optional gradient refinement under fixed supports.
6. Emit provenance, parameter counts, nonzero counts, and conditioning diagnostics.
7. Reject compilation when measured closure or factor conditioning fails.

Required baselines:

- dense;
- truncated SVD;
- independent block low rank;
- exact Hadamard factory;
- random dense negative control.

No result is complete without end-to-end `matvec`, `rmatvec`, serialization, reconstruction, and gradient tests.
