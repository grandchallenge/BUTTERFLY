# WP5 — Butterfly Neural Krylov Transport

Build the flagship architecture around

`A_u = damping * I + B_u^* B_u`.

Required components:

- butterfly transport `B_u` with shared topology;
- conditional diagonal or small-block gates;
- explicit adjoint;
- conjugate-gradient and MINRES interfaces;
- optional preconditioner;
- adaptive iteration horizon;
- residual-triggered fallback;
- differentiable PyTorch implementation;
- float32 and bfloat16 tests with float64 references.

Experiments must compare dense, global-low-rank, butterfly, and butterfly-plus-Krylov under equal parameter, memory, and measured-runtime budgets.

Primary outputs are residual convergence curves, task utility, memory traffic, and reuse-amortized speed.
