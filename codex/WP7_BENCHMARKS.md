# WP7 — Benchmark and Experiment System

Operationalize `RUN_MATRIX.md`.

Required features:

- Hydra or an equivalently explicit configuration system;
- multi-seed execution;
- local and scheduler-compatible launchers;
- JSONL and Parquet result stores;
- artifact versioning;
- optional Weights & Biases integration;
- scaling plots and confidence intervals;
- automatic dense-random negative controls;
- environment and git provenance.

Every report must distinguish compilation, warm execution, and cold execution. Generate one machine-readable record per run and one consolidated summary per experiment family.
