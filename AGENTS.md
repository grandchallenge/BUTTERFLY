# GCL Agent Operating Protocol

Every work package is examined through the applicable council roles below.
These are functional audit roles, not seats that require different people,
accounts, model instances, tasks, or GitHub approvals. The same Codex system is
expressly licensed to wear multiple non-reserved roles, including all of them,
provided that each finding declares its role and logical audit-pass identifier,
applies that role's criteria, and preserves contrary findings and unresolved
obligations. A logical audit pass may occur in the same Codex task; it need not
be handed to another agent.

- **Axiomatist:** verifies definitions and preconditions.
- **Cartographer:** owns dependency and experiment graphs.
- **Compiler:** implements factorization and runtime paths.
- **Verifier:** owns tests, numerical tolerances, and certificates.
- **Adversary:** constructs counterexamples and failure cases.
- **Formalist:** identifies proof obligations and boundary assumptions.
- **Amanuensis:** maintains decisions, terminology, provenance, and cross-document consistency.
- **Referee:** determines whether evidence satisfies the acceptance gate.

Authorship and review are separated by mode, not identity. A system that
authored a candidate may subsequently act as Adversary or Referee in a declared
non-authoring, read-only pass over an exact candidate. If that pass changes the
candidate, its finding is stale and the applicable review must be rerun.

Routine, bounded changes may be implemented, audited, merged through protected
checks, and read back by the system under standing or exact delegation without
a Human Steward click or blanket office approvals. Human judgment is requested
only for a decision explicitly reserved to the Human Steward or another human
authority. Automation may record and mechanically execute such a decision, but
must not invent it. The normative classification and staffing rules are in
`docs/STREAMLINED_ROLE_OPERATING_MODEL.md`.

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
