"""Boundary input validation (IC-1 through IC-4)."""

from src.boundary.error_catalog import ERROR_CATALOG
from src.boundary.schemas import ErrorResponse
from src.domain.constants import (
    BLANK_CELL,
    GRID_SIZE,
    MAX_CELL_VALUE,
    MIN_PARTIAL_CELL_VALUE,
    REQUIRED_BLANK_COUNT,
)


class InputValidator:
    """Validate partial grid input before Domain delegation."""

    def validate(self, grid: object) -> ErrorResponse | None:
        """Return the first contract violation, or ``None`` when input is valid."""
        size_error = self._validate_size(grid)
        if size_error is not None:
            return size_error

        assert isinstance(grid, list)

        range_error = self._validate_cell_range(grid)
        if range_error is not None:
            return range_error

        typed_grid: list[list[int]] = grid  # validated as int cells above
        blank_error = self._validate_blank_count(typed_grid)
        if blank_error is not None:
            return blank_error

        duplicate_error = self._validate_duplicates(typed_grid)
        if duplicate_error is not None:
            return duplicate_error

        return None

    def _validate_size(self, grid: object) -> ErrorResponse | None:
        if not isinstance(grid, list):
            return self._error("INVALID_SIZE")

        if len(grid) != GRID_SIZE:
            return self._error("INVALID_SIZE")

        for row in grid:
            if not isinstance(row, list) or len(row) != GRID_SIZE:
                return self._error("INVALID_SIZE")

        return None

    def _validate_cell_range(self, grid: list[list[object]]) -> ErrorResponse | None:
        for row in grid:
            for cell in row:
                if isinstance(cell, float):
                    return self._error("INVALID_SIZE")
                if not isinstance(cell, int):
                    return self._error("CELL_VALUE_OUT_OF_RANGE")
                if cell < MIN_PARTIAL_CELL_VALUE or cell > MAX_CELL_VALUE:
                    return self._error("CELL_VALUE_OUT_OF_RANGE")

        return None

    def _validate_blank_count(self, grid: list[list[int]]) -> ErrorResponse | None:
        blank_count = sum(cell == BLANK_CELL for row in grid for cell in row)
        if blank_count != REQUIRED_BLANK_COUNT:
            return self._error("EMPTY_CELL_COUNT_INVALID")

        return None

    def _validate_duplicates(self, grid: list[list[int]]) -> ErrorResponse | None:
        seen: set[int] = set()
        for row in grid:
            for cell in row:
                if cell == BLANK_CELL:
                    continue
                if cell in seen:
                    return self._error("DUPLICATE_NON_ZERO")
                seen.add(cell)

        return None

    def _error(self, code: str) -> ErrorResponse:
        return ErrorResponse(code=code, message=ERROR_CATALOG[code])
