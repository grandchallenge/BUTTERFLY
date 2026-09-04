# Numerical Policy

- Use float64 for reference ranks, certificates, and finite-difference checks.
- Rank is relative to the largest singular value unless an experiment explicitly states an absolute threshold.
- Zero blocks have rank zero and tail energy zero.
- Report the exact tolerance, rank budget, oversampling, power iterations, and seed.
- Adjoint consistency is tested through bilinear identities, not only reconstructed matrices.
- Random probes are evidence, not proof; ambiguous cases escalate to power or Lanczos search.
- Learned and hardware paths must be compared against deterministic small references.
- Tolerances must scale explicitly with dtype and operator dimension.
