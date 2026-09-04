# ADR-0003: Streamlined multi-role agent staffing

- Status: accepted
- Date: 2026-09-04
- Decision authority: Human Steward direction in the onboarding task
- Scope: BUTTERFLY programme implementation, audit, review, and integration

## Context

Earlier onboarding language mixed two different safeguards: separation of
audit functions and multiplication of human or agent identities. That ambiguity
could be read to require a hand-off among people, tasks, accounts, or model
instances at every gate. It also conflicted with the repository's standing
delegation for deterministic protected transactions.

Repeated approval hand-offs do not themselves improve the evidence. The useful
separation is that a candidate is examined against different criteria, in
declared modes, with exact-subject findings that cannot silently survive a
material change.

## Decision

The Codex system is expressly licensed to staff any combination of the
Axiomatist, Cartographer, Compiler, Verifier, Adversary, Formalist, Amanuensis,
and Referee roles. One system may staff all applicable roles.

Role separation is satisfied by role-scoped evidence and logical audit passes,
not by different humans, agents, tasks, conversations, accounts, or model
instances. Each pass records its role, exact subject, criteria, finding,
unresolved obligations, and logical pass identifier. The identifier names an
audit phase and need not name a separate execution session.

When the system authored the subject, an Adversary or Referee pass must switch
to non-authoring, read-only review mode. It may report defects and obligations
but may not repair the candidate inside that pass. A repair creates a new
candidate and invalidates the affected findings.

Work is handled proportionally:

1. `routine_bounded` work may be classified, authored, tested, audited, merged
   through protected checks, and read back by the system under standing or
   exact delegation. It requires no fresh human action or blanket approval.
2. `substantive` work receives the applicable functional audit passes and
   evidence gates. It does not require identity multiplication.
3. `reserved` work receives human judgment only where a governing contract
   expressly reserves the decision. The system may prepare, transcribe, route,
   and mechanically execute that decision without adding ceremonial clicks.

The system must never fabricate human judgment or extend a decision beyond its
exact subject and stated authority. Programme admission does not confer
MATHCERT certification, scientific claim promotion, production, safety,
commercial, novelty, priority, or other excluded authority.

## Consequences

- Future agents receive the license and its limits directly from `AGENTS.md`.
- Routine changes can complete autonomously through protected controls.
- Audit independence is inspectable in the record rather than inferred from a
  count of identities or approvals.
- Reserved human authority remains real, narrow, and normally requires one
  consolidated decision rather than a gate-by-gate approval chain.

## Reversal conditions

Revisit this decision if an external binding rule requires organizationally
independent reviewers, evidence shows role-mode separation is insufficient, or
the protected automation cannot preserve exact-subject audit records.
