# Mergeable Work Breakdown

## Dependency spine

```text
BFC-001 contracts and fixtures
  -> BFC-010 matrix-free observatory
  -> BFC-020 hierarchy discovery
  -> BFC-030 block-sparse factor storage
  -> BFC-040 algebraic compiler
  -> BFC-050 certification ladder
  -> BFC-060 PyTorch differentiable path
  -> BFC-070 Butterfly NKT
  -> BFC-080 Triton runtime
  -> BFC-090 experiment system
  -> BFC-100 learned-closure study
```

## Initial issues

### BFC-001 — Freeze operator and certificate schemas
Acceptance: JSON schema, typed Python objects, serialization round trip, ADR.

### BFC-010 — Randomized complementary-rank estimator
Acceptance: explicit-versus-matrix-free error study; complex rectangular tests; uncertainty intervals.

### BFC-020 — Topology candidate registry
Acceptance: natural, bit-reversal, geometry, spectral, and balanced-clustering candidates under one interface.

### BFC-030 — Block-sparse factor runtime
Acceptance: exact forward/adjoint; serialization; parameter/nonzero accounting; NumPy reference tests.

### BFC-040 — Algebraic butterfly initialization
Acceptance: compile at least one noncanonical synthetic complementary-low-rank operator without dense fallback.

### BFC-050 — CRV-BF certification ladder
Acceptance: detects adversarial hidden residual directions missed by basic probes.

### BFC-060 — Differentiable PyTorch implementation
Acceptance: forward, adjoint, gradcheck, mixed-precision comparison, state-dict round trip.

### BFC-070 — Butterfly Neural Krylov Transport
Acceptance: dense/LR/butterfly/corrected comparison with residual convergence and memory accounting.

### BFC-080 — Triton fixed-radix kernel
Acceptance: numerical parity and a declared accelerator break-even region.

### BFC-090 — Reproducible run matrix
Acceptance: multi-seed launch, machine-readable result store, consolidated report, environment provenance.

### BFC-100 — Learned-observable closure experiment
Acceptance: trained/untrained/shuffled controls and confidence intervals over at least five seeds.
