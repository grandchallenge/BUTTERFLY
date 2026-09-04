# ADR-0002: Content-address dense operators used in certificates

- Status: accepted for the onboarding candidate
- Date: 2026-09-04
- Scope: operator fingerprint and mutation boundary

## Decision

`DenseLinearOperator` copies its input into an immutable C-contiguous array and
derives its fingerprint from the dtype, shape, matrix bytes, and canonicalized
metadata. The public constructor and numerical application APIs are preserved.

The generic `LinearOperator` fingerprint remains a structural diagnostic. A
future public contract change for callable content identities requires another
ADR. Admission claims are therefore limited to exact dense-operator identities;
callable fingerprints must not be represented as content-addressed certificates.

## Alternatives

Retaining shape-only fingerprints was rejected because different matrices could
share a certificate identity. Hashing the caller-owned array without copying was
rejected because later mutation could silently change the certified subject.

## Reversal conditions

This decision may be superseded by a versioned operator-identity protocol that
provides equally immutable, replayable identities for dense and matrix-free
operators without weakening existing certificate provenance.
