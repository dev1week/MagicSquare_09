"""Locate blank (zero) cells in a partial grid."""

from src.domain.constants import BLANK_CELL, REQUIRED_BLANK_COUNT
from src.domain.exceptions import GridNotComplete


class EmptyCellLocator:
    """Find the two blank cells in row-major 0-index order."""

    def locate(self, grid: list[list[int]]) -> tuple[tuple[int, int], tuple[int, int]]:
        """Return two blank coordinates in row-major order."""
        blanks = [
            (row_index, col_index)
            for row_index, row in enumerate(grid)
            for col_index, value in enumerate(row)
            if value == BLANK_CELL
        ]
        if len(blanks) != REQUIRED_BLANK_COUNT:
            raise GridNotComplete(
                f"Expected {REQUIRED_BLANK_COUNT} blank cells, found {len(blanks)}."
            )

        first, second = blanks[0], blanks[1]
        return first, second
