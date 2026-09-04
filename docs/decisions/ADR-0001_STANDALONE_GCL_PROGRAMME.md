# ADR-0001: Admit BUTTERFLY as a standalone GCL research programme

- Status: proposed
- Decision identifier: `BFC-ADR-0001`
- Admission package: `BFC-ADMISSION-001`

## Problem

BUTTERFLY-CLOSURE combines a research charter, deterministic numerical
reference implementation, experiment system, and a multi-work-package research
frontier. It needs an authority surface that preserves this integrated lineage
without confusing implementation evidence with mathematical certification.

## Alternatives

1. A standalone programme repository with bounded work-package promotion.
2. A campaign embedded in MATH-PROGRAMME and split across the mathematics
   pillars.
3. A provider repository with no claim-promotion role.

## Decision

Select option 1 at `grandchallenge/BUTTERFLY`. Use the `programme` profile,
`programme-research` workflow, high risk tier, `work_package_only` claim role,
and `immutable_admitted` release policy.

## Compatibility and migration

The `bclosure` Python API is unchanged. Existing documents and artifacts enter
as candidate source material. Only records explicitly admitted at exact
identities gain programme status. Mathematical certification remains external
to this repository.

## Reversal conditions

Return to private incubation or supersede this decision if the reference
baseline cannot be reproduced, authority records conflict, required repository
controls cannot be enforced, independent review rejects the charter, or the
Human Steward withholds public-admission authorization. Preserve all reasons
and evidence when reversing.
