# Metrics

## Structural

- maximum complementary rank `r_bf_max`;
- mean and quantile complementary rank;
- rank growth exponent versus problem size;
- normalized rank-tail energy;
- topology stability across states/checkpoints;
- fraction of blocks satisfying the contract.

## Approximation

- relative Frobenius error when materialization is feasible;
- probe-relative forward error;
- probe-relative adjoint error;
- bilinear adjoint consistency;
- spectral residual estimate;
- downstream task utility delta.

## Computational

- compile wall time;
- steady-state wall time;
- warm and cold latency;
- throughput;
- parameter and nonzero counts;
- estimated FLOPs;
- estimated and measured bytes moved;
- peak allocated memory;
- break-even reuse horizon.

## Stability

- local factor spectral norms;
- product norm upper bound;
- inverse sensitivity where applicable;
- gradient norm and gradient-check error;
- residual amplification under perturbations.

## Reporting formulae

Break-even reuse horizon:

\[
H^* = \frac{C_{compile}}{C_{dense}-C_{structured}}.
\]

Closure score at budget \(r\):

\[
C_r = 1 - \mathbb E_{I,J,\ell}\frac{\sum_{k>r}\sigma_k^2}{\|A_{I,J}\|_F^2+\delta}.
\]

No claim may use a single scalar speedup without its size, batch, precision, hardware, and reuse horizon.
