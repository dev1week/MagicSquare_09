"""Domain-specific exception types."""


class GridNotComplete(Exception):
    """Raised when a grid still contains blank cells."""


class InvalidGridSize(Exception):
    """Raised when a grid is not 4×4."""


class UnsolvableGrid(Exception):
    """Raised when no valid magic square completion exists."""
