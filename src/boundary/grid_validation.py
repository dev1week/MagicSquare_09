"""Shared grid structure validation for Boundary partial and complete paths."""

from dataclasses import dataclass

from src.domain.constants import (
    BLANK_CELL,
    CELL_COUNT,
    GRID_SIZE,
    MAX_CELL_VALUE,
    MIN_FILLED_CELL_VALUE,
    MIN_PARTIAL_CELL_VALUE,
    REQUIRED_BLANK_COUNT,
)


@dataclass(frozen=True, slots=True)
class GridValidationPolicy:
    """Cell-range and blank-count rules for a grid validation path."""

    min_cell_value: int
    max_cell_value: int
    required_blank_count: int | None
    require_full_unique_count: bool


PARTIAL_GRID_POLICY = GridValidationPolicy(
    min_cell_value=MIN_PARTIAL_CELL_VALUE,
    max_cell_value=MAX_CELL_VALUE,
    required_blank_count=REQUIRED_BLANK_COUNT,
    require_full_unique_count=False,
)

COMPLETE_GRID_POLICY = GridValidationPolicy(
    min_cell_value=MIN_FILLED_CELL_VALUE,
    max_cell_value=MAX_CELL_VALUE,
    required_blank_count=None,
    require_full_unique_count=True,
)


class GridStructureValidator:
    """Validate 4×4 grid structure; return the first EC code or ``None``."""

    def __init__(self, policy: GridValidationPolicy) -> None:
        self._policy = policy

    def validate(self, grid: object) -> str | None:
        """Return the first contract violation code, or ``None`` when valid."""
        size_error = self._validate_size(grid)
        if size_error is not None:
            return size_error

        assert isinstance(grid, list)

        range_error = self._validate_cell_range(grid)
        if range_error is not None:
            return range_error

        typed_grid: list[list[int]] = grid

        if self._policy.required_blank_count is not None:
            blank_error = self._validate_blank_count(typed_grid)
            if blank_error is not None:
                return blank_error

        return self._validate_duplicates(typed_grid)

    def _validate_size(self, grid: object) -> str | None:
        if not isinstance(grid, list):
            return "INVALID_SIZE"

        if len(grid) != GRID_SIZE:
            return "INVALID_SIZE"

        for row in grid:
            if not isinstance(row, list) or len(row) != GRID_SIZE:
                return "INVALID_SIZE"

        return None

    def _validate_cell_range(self, grid: list[list[object]]) -> str | None:
        for row in grid:
            for cell in row:
                if isinstance(cell, float):
                    return "INVALID_SIZE"
                if not isinstance(cell, int):
                    return "CELL_VALUE_OUT_OF_RANGE"
                if cell < self._policy.min_cell_value or cell > self._policy.max_cell_value:
                    return "CELL_VALUE_OUT_OF_RANGE"

        return None

    def _validate_blank_count(self, grid: list[list[int]]) -> str | None:
        assert self._policy.required_blank_count is not None
        blank_count = sum(cell == BLANK_CELL for row in grid for cell in row)
        if blank_count != self._policy.required_blank_count:
            return "EMPTY_CELL_COUNT_INVALID"

        return None

    def _validate_duplicates(self, grid: list[list[int]]) -> str | None:
        seen: set[int] = set()
        for row in grid:
            for cell in row:
                if cell == BLANK_CELL:
                    continue
                if cell in seen:
                    return "DUPLICATE_NON_ZERO"
                seen.add(cell)

        if self._policy.require_full_unique_count and len(seen) != CELL_COUNT:
            return "DUPLICATE_NON_ZERO"

        return None
