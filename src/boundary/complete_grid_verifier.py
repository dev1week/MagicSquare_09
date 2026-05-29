"""Boundary verification for complete 4×4 magic squares."""

from dataclasses import dataclass

from src.boundary.error_catalog import ERROR_CATALOG
from src.domain.constants import (
    CELL_COUNT,
    GRID_SIZE,
    MAGIC_CONSTANT,
    MAX_CELL_VALUE,
    MIN_FILLED_CELL_VALUE,
)
from src.domain.exceptions import GridNotComplete, InvalidGridSize
from src.domain.magic_square_judge import MagicSquareJudge


@dataclass(frozen=True, slots=True)
class VerifySuccess:
    """Complete grid passed structural checks; includes magic verdict."""

    is_magic: bool
    magic_constant: int


@dataclass(frozen=True, slots=True)
class VerifyError:
    """Verification could not run because input violates Boundary contract."""

    code: str
    message: str


class CompleteGridVerifier:
    """Validate a filled grid and delegate magic-square judgment to Domain."""

    def __init__(self, judge: MagicSquareJudge | None = None) -> None:
        self._judge = judge if judge is not None else MagicSquareJudge()

    def verify(self, grid: object) -> VerifySuccess | VerifyError:
        """Return whether a complete grid is a magic square, or a contract error."""
        structure_error = self._validate_structure(grid)
        if structure_error is not None:
            return structure_error

        assert isinstance(grid, list)
        typed_grid: list[list[int]] = grid

        try:
            is_magic = self._judge.is_magic(typed_grid)
        except (GridNotComplete, InvalidGridSize):
            return self._error("INVALID_SIZE")

        return VerifySuccess(is_magic=is_magic, magic_constant=MAGIC_CONSTANT)

    def _validate_structure(self, grid: object) -> VerifyError | None:
        if not isinstance(grid, list) or len(grid) != GRID_SIZE:
            return self._error("INVALID_SIZE")

        seen: set[int] = set()
        for row in grid:
            if not isinstance(row, list) or len(row) != GRID_SIZE:
                return self._error("INVALID_SIZE")

            for cell in row:
                if not isinstance(cell, int):
                    return self._error("CELL_VALUE_OUT_OF_RANGE")
                if cell < MIN_FILLED_CELL_VALUE or cell > MAX_CELL_VALUE:
                    return self._error("CELL_VALUE_OUT_OF_RANGE")
                if cell in seen:
                    return self._error("DUPLICATE_NON_ZERO")
                seen.add(cell)

        if len(seen) != CELL_COUNT:
            return self._error("DUPLICATE_NON_ZERO")

        return None

    def _error(self, code: str) -> VerifyError:
        return VerifyError(code=code, message=ERROR_CATALOG[code])
