# Package Validation

The generated scaffold baseline has now been reproduced during candidate
onboarding. The authoritative candidate evidence is
`artifacts/BFC-BASELINE-QUALIFICATION-001.json`; it remains local and
unpromoted until bound to an exact commit and reproduced by protected CI.

## Automated tests

```text
15 passed on Python 3.10.19 and 3.12.10
```

Covered invariants:

- exact normalized Walsh-Hadamard execution;
- Hadamard self-adjointness and orthogonality;
- dense bilinear adjoint identity;
- exact factor-chain forward and adjoint actions;
- rank-budget acceptance for a global-low-rank operator;
- rejection of a random dense operator under a small budget;
- rank-one complementary closure of Hadamard under one-sided bit-reversal ordering;
- exact-target certification;
- conjugate-gradient solution of an SPD system;
- configuration loading.
- closed-schema governance validation and hostile-record rejection;
- deterministic complex rectangular inspection and adjoint consistency;
- detection of an explicitly probed hidden residual direction.

## Smoke observations

### Hadamard, size 1024

- input ordering: natural;
- output ordering: bit reversal;
- measured maximum complementary rank: `1`;
- mean measured rank: `1.0`;
- maximum reported rank-one tail energy: approximately `3.27e-29`;
- compile recommendation: accepted.

### Global low rank, size 1024, rank 8

- measured maximum complementary rank: `8`;
- compile recommendation under rank budget 8: accepted.

### Random dense control, size 512

- measured maximum sampled complementary rank: `16`;
- compile recommendation under rank budget 8: rejected.

## Deliberate research boundary

The canonical exact compiler and execution contracts are operational. The generic algebraic compiler for arbitrary complementarily low-rank operators is intentionally marked as WP3 rather than disguised by a dense fallback. This is the first principal Codex implementation target.
