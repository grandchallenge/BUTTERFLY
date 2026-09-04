# Programme Specification

## Mission

Determine when globally high-rank operators admit low numerical rank across complementary input/output scales; certify the condition; compile the operator into sparse multiscale factors; and correct the residual when closure is incomplete.

## Core object

For input and output trees of common depth \(L\), define

\[
r_{\mathrm{BF}}(A;\varepsilon)
=
\max_{0\le \ell\le L}
\max_{I\in T_Y^\ell,\,J\in T_X^{L-\ell}}
r_\varepsilon(A_{I,J}).
\]

The operator satisfies an \((r,\varepsilon)\) closure contract when this maximum does not exceed \(r\).

## Programme deliverables

- BFC-D1: matrix-free complementary-rank observatory;
- BFC-D2: hierarchy and permutation discovery;
- BFC-D3: algebraic and learned butterfly compilers;
- BFC-D4: certification ladder with adversarial residual search;
- BFC-D5: block-sparse GPU runtime;
- BFC-D6: Butterfly Neural Krylov Transport;
- BFC-D7: learned-observable closure study;
- BFC-D8: no-regret execution controller;
- BFC-D9: benchmark corpus and reproducible reports;
- BFC-D10: theory and systems manuscripts.

## Falsification gates

### G0 — rank contract
At least two priority operator families must show bounded or slowly growing complementary rank. Otherwise narrow the programme to the operator families that pass.

### G1 — canonical recovery
Exact or near-exact recovery of Hadamard and FFT-like transforms; random dense matrices must be rejected at the same tolerance/rank budget.

### G2 — measured economy
At a declared size and reuse horizon, the structured implementation must reduce measured memory traffic or latency relative to a tuned dense baseline.

### G3 — corrected superiority
Butterfly plus residual correction must outperform equally budgeted global low-rank and uncorrected butterfly baselines.

### G4 — learned closure
At least one learned system must exhibit training- or depth-associated improvement in closure score under controls.

### G5 — end-to-end utility
Demonstrate improved task utility at fixed resources, reduced resources at fixed utility, or expanded problem size under a fixed hardware budget.

## Acceptance criteria for release 0.1

- Explicit and matrix-free closure estimates agree within 20% on synthetic targets.
- Canonical Hadamard reconstruction error is below `1e-10` in float64.
- Adjoint tests pass to numerical tolerance.
- Random dense controls are rejected under a deliberately small rank budget.
- Benchmark reports contain task/operator error, wall time, compilation time, peak memory estimate, and break-even horizon.
- All public APIs are typed and covered by smoke tests.
