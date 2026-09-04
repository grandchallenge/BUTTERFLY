# Run Matrix

| Run ID | Family | Operator | Sizes | Tolerance | Rank budgets | Baselines | Required outputs |
|---|---|---|---|---:|---|---|---|
| SYN-HAD | canonical | normalized Hadamard | 256–65536 | 1e-10 | 1,2,4 | dense, exact butterfly | error, latency, bytes, scaling |
| SYN-FFT | canonical | complex FFT | 256–65536 | 1e-8 | 2,4,8 | FFT library, dense DFT | error, latency, compile cost |
| SYN-LR | control | global low rank | 512–16384 | 1e-5 | 4–64 | SVD, butterfly | closure profile, error |
| SYN-RND | negative control | random dense | 256–8192 | 1e-3 | 2–32 | dense, SVD | rejection rate, false-positive rate |
| OSC-CHIRP | oscillatory | chirp kernel | 1024–65536 | 1e-4 | 4–32 | dense, NFFT where relevant | rank growth, runtime |
| SPH-GEG | hyperspherical | Gegenbauer kernel | 1024–32768 | 1e-4 | 4–64 | dense, Nyström, RFF | error, memory, scaling |
| SPH-HEAT | hyperspherical | heat kernel | 1024–32768 | 1e-4 | 4–64 | Chebyshev, Nyström | error, runtime |
| NKT-CORE | learned/scientific | B*u and B*B | model dependent | 1e-3 | 4–64 | dense, LR, sparse | Krylov convergence, task utility |
| MOE-ROUTE | learned | token-expert score | 1k–64k tokens | 1e-3 | 4–64 | dense, hierarchical | regret, communication, utility |
| OBS-DEPTH | diagnostic | layer Jacobians | model dependent | 1e-3 | measured | random-init control | depthwise closure curves |

## Seed policy

- smoke: seed `0`;
- development: seeds `0,1,2`;
- release: seeds `0,1,2,3,4`;
- claims involving learned closure: at least five seeds and confidence intervals.

## Precision policy

- rank/certification reference: float64;
- training: float32 or bfloat16 with float32 accumulators;
- runtime comparisons: report all supported precisions separately.
