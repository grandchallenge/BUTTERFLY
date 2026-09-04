# GCL Agent Operating Protocol

Every work package is reviewed by the following council roles.

- **Axiomatist:** verifies definitions and preconditions.
- **Cartographer:** owns dependency and experiment graphs.
- **Compiler:** implements factorization and runtime paths.
- **Verifier:** owns tests, numerical tolerances, and certificates.
- **Adversary:** constructs counterexamples and failure cases.
- **Formalist:** identifies proof obligations and boundary assumptions.
- **Amanuensis:** maintains decisions, terminology, provenance, and cross-document consistency.
- **Referee:** determines whether evidence satisfies the acceptance gate.

## Required implementation sequence

1. Read the programme, architecture, contracts, metrics, and relevant work-package prompt.
2. Create or update an ADR before changing a public contract.
3. Implement the deterministic reference path first.
4. Add unit, numerical, adjoint, and negative-control tests.
5. Run the smallest relevant benchmark configuration.
6. Record results in `artifacts/` and update the review ledger.
7. Do not claim completion while unresolved acceptance obligations remain.

## Definition of done

A work package is complete only when code, tests, configuration, documentation, and review evidence are all present.
