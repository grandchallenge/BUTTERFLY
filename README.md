# BUTTERFLY CLOSURE

Status: `ADOPTED_GCL_RESEARCH_PROGRAMME`

Authority repository: `grandchallenge/BUTTERFLY`

Programme identifier: `BFC`

**Discovering, certifying, and compiling complementarily low-rank computation.**

This repository is the Codex-ready implementation package for the GCL Research Programme **BUTTERFLY CLOSURE**. It contains a runnable reference stack, explicit contracts, numerical tests, benchmark configurations, and role-specific implementation prompts.

The programme was publicly adopted through protected onboarding and portfolio
records on 2026-09-04. Individual work packages, numerical evidence, and claims
retain their own recorded states: programme adoption does not promote a
scientific claim or constitute MATHCERT certification. The exact authority
boundary is defined in `GOVERNANCE.md` and the protected programme records.

## Programme loop

```text
operator access
  -> complementary-rank inspection
  -> hierarchy/topology selection
  -> butterfly compilation
  -> residual correction
  -> certification
  -> task and hardware evaluation
```

## Current reference scope

The repository intentionally separates verified reference functionality from research work still requiring implementation.

Implemented now:

- matrix-free `LinearOperator` protocol;
- dense and callable operator adapters;
- balanced complementary cluster trees;
- randomized block-rank estimation;
- closure reports and compile/reject policy;
- exact Walsh-Hadamard butterfly operator;
- generic sparse factor-chain operator;
- adjoint, reconstruction, rank-estimation, and rejection tests;
- benchmark and reporting harnesses;
- Neural Krylov Transport interfaces and a conjugate-gradient reference solver;
- experiment schemas and GCL review ledger.

Research targets are marked with `BFC-TODO` and assigned through the work-package prompts in `codex/`.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\\Scripts\\activate
pip install -e '.[dev]'
pytest -q
python -m bclosure.cli inspect configs/synthetic_hadamard.yaml
python -m bclosure.cli benchmark configs/synthetic_hadamard.yaml
```

## Non-negotiable rules

1. The compiler must be able to reject operators that do not satisfy the measured closure contract.
2. Every optimized path must preserve a deterministic reference path.
3. Every operator implementation must expose or explicitly decline an adjoint.
4. Results must report compilation cost and amortized break-even horizon.
5. FLOP estimates never substitute for measured latency and bytes moved.
6. Dense random controls are mandatory in every closure claim.

See `PROGRAMME_SPEC.md`, `ARCHITECTURE.md`, `CONTRACTS.md`, `RUN_MATRIX.md`, and `METRICS.md` before implementing a work package.
