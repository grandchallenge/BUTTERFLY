# WP6 — Hardware Runtime

Implement hardware-effective block butterfly execution.

Order of work:

1. PyTorch reference with block-sparse tensors.
2. Fused permutation plus block mixing.
3. Triton kernels for fixed radix and block width.
4. Fused forward/adjoint traversal.
5. Autotuning over radix, block size, layout, and precision.
6. Accurate timing with warmups and device synchronization.

Report theoretical arithmetic separately from measured bytes and latency. Demonstrate the break-even problem size and reuse horizon. Preserve the NumPy reference path for correctness.
