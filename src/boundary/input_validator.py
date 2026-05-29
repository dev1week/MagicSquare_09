"""Boundary input validation (IC-1 through IC-4)."""

from src.boundary.error_catalog import ERROR_CATALOG
from src.boundary.grid_validation import PARTIAL_GRID_POLICY, GridStructureValidator
from src.boundary.schemas import ErrorResponse


class InputValidator:
    """Validate partial grid input before Domain delegation."""

    def __init__(self) -> None:
        self._structure_validator = GridStructureValidator(PARTIAL_GRID_POLICY)

    def validate(self, grid: object) -> ErrorResponse | None:
        """Return the first contract violation, or ``None`` when input is valid."""
        error_code = self._structure_validator.validate(grid)
        if error_code is not None:
            return self._error(error_code)

        return None

    def _error(self, code: str) -> ErrorResponse:
        return ErrorResponse(code=code, message=ERROR_CATALOG[code])
