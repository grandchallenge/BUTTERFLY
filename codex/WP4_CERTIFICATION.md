# WP4 — Certification and Adversarial Residual Search

Extend `certification.py` into the CRV-BF ladder.

Implement:

- orthogonal probe banks;
- block power iteration;
- Lanczos spectral residual estimation;
- error confidence intervals;
- blockwise failure localization;
- target/approximation fingerprints;
- serialized certificates;
- downstream task-delta hooks.

The Adversary must construct operators for which naive Gaussian probing misses a narrow high-error subspace. The improved certificate must discover these cases reliably.
