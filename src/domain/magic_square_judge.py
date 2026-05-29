"""Validate whether a complete 4×4 grid is a magic square."""

from src.domain.constants import MAGIC_CONSTANT
from src.domain.exceptions import GridNotComplete, InvalidGridSize

_GRID_SIZE = 4


class MagicSquareJudge:
    """Check row, column, and diagonal sums against the magic constant."""

    def __init__(self) -> None:
        self._magic_constant = MAGIC_CONSTANT

    @property
    def magic_constant(self) -> int:
        """Return the configured magic constant."""
        return self._magic_constant

    def is_magic(self, grid: list[list[int]]) -> bool:
        """Return ``True`` when every line sum equals the magic constant."""
        self._ensure_complete_grid(grid)

        if not self._all_rows_equal_constant(grid):
            return False

        if not self._all_columns_equal_constant(grid):
            return False

        if not self._diagonal_equal_constant(
            [grid[index][index] for index in range(_GRID_SIZE)]
        ):
            return False

        if not self._diagonal_equal_constant(
            [grid[row_index][_GRID_SIZE - 1 - row_index] for row_index in range(_GRID_SIZE)]
        ):
            return False

        return True

    def _ensure_complete_grid(self, grid: list[list[int]]) -> None:
        if len(grid) != _GRID_SIZE or any(len(row) != _GRID_SIZE for row in grid):
            raise InvalidGridSize

        if any(value == 0 for row in grid for value in row):
            raise GridNotComplete

    def _all_rows_equal_constant(self, grid: list[list[int]]) -> bool:
        return all(self._line_equal_constant(row) for row in grid)

    def _all_columns_equal_constant(self, grid: list[list[int]]) -> bool:
        for column_index in range(_GRID_SIZE):
            column = [grid[row_index][column_index] for row_index in range(_GRID_SIZE)]
            if not self._line_equal_constant(column):
                return False
        return True

    def _diagonal_equal_constant(self, diagonal: list[int]) -> bool:
        return self._line_equal_constant(diagonal)

    def _line_equal_constant(self, line: list[int]) -> bool:
        return sum(line) == self._magic_constant
