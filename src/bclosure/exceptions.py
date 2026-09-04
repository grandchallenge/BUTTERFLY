class ButterflyClosureError(RuntimeError):
    """Base exception for the package."""


class AdjointUnavailable(ButterflyClosureError):
    """Raised when an operator does not expose an adjoint action."""


class CompilationRejected(ButterflyClosureError):
    """Raised when measured closure does not satisfy the compile contract."""
