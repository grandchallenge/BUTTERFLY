# WP1 — Matrix-Free Closure Observatory

Implement robust complementary-rank inspection without materializing the full operator.

Required work:

- randomized range and co-range sketches;
- optional power iteration;
- block sampling stratified by level and block size;
- confidence intervals from repeated sketches;
- exact verification for small blocks;
- singular-tail and closure-score reports;
- scaling study against explicit SVD;
- failure handling when the adjoint is unavailable.

Tests:

- exact low-rank blocks;
- rapidly decaying spectra;
- flat spectra;
- complex-valued operators;
- rectangular operators;
- adversarial missed-direction tests;
- deterministic seed replay.

Acceptance:

Median estimated rank must be within 20% of explicit rank on the synthetic suite, with false acceptance of random dense controls below 5% under the declared contract.
