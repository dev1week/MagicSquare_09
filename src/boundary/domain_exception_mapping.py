"""Map Domain exceptions to Boundary error codes."""

from src.domain.exceptions import GridNotComplete, InvalidGridSize, UnsolvableGrid


def boundary_error_code_for(exc: BaseException) -> str | None:
    """Return a Boundary error code for a known Domain failure, else ``None``."""
    if isinstance(exc, UnsolvableGrid):
        return "DOMAIN_UNSOLVABLE"
    if isinstance(exc, (GridNotComplete, InvalidGridSize)):
        return "INVALID_SIZE"
    return None
