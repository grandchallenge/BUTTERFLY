# Contracts

## LinearOperatorContract

An operator must declare:

- immutable `(output_dim, input_dim)` shape;
- numeric dtype;
- deterministic `matvec` for deterministic inputs;
- `rmatvec` or an explicit `AdjointUnavailable` exception;
- batch-safe `matmat` semantics;
- device and precision assumptions in metadata.

## ComplementaryLowRankContract

```yaml
input_tree: identifier
output_tree: identifier
tolerance: 1.0e-4
rank_budget: 16
sampling:
  blocks_per_level: 16
  oversampling: 8
  power_iterations: 1
acceptance:
  max_rank: 16
  max_tail_energy: 1.0e-3
```

A report must include all sampled block coordinates, dimensions, estimated ranks, singular values or sketches, tail energies, and random seeds.

## ButterflyFactorContract

Each factor declares:

- input/output dimensions;
- sparse support or block topology;
- local block values;
- forward and adjoint application;
- exact parameter count and nonzero count;
- condition diagnostics;
- serialization version.

## CompilationContract

Compilation returns either:

- `CompiledButterfly(operator, certificate_stub, provenance)`; or
- `CompilationRejected(reason, measured_contract, alternatives)`.

Silent fallback to dense execution is forbidden.

## CertificationContract

A certificate contains:

- probe-relative forward error;
- probe-relative adjoint error;
- bilinear adjoint consistency error;
- estimated spectral residual;
- task-level delta when available;
- confidence metadata;
- and the exact target/approximation fingerprints.

## BenchmarkContract

Every benchmark records:

- git commit and dirty state;
- package/environment versions;
- hardware description;
- random seeds;
- warmup and timing protocol;
- compile and execution times separately;
- parameter, nonzero, FLOP, and byte estimates;
- task/operator accuracy;
- and produced artifact paths.
