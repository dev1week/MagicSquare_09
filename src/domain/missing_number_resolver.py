"""Resolve the two missing numbers from a partial grid."""

from src.domain.constants import BLANK_CELL, MAX_CELL_VALUE, MIN_FILLED_CELL_VALUE
from src.domain.exceptions import GridNotComplete


class MissingNumberResolver:
    """Determine which values from 1..16 are absent from the grid."""

    def resolve(self, grid: list[list[int]]) -> tuple[int, int]:
        """Return the two missing numbers in ascending order."""
        present = {value for row in grid for value in row if value != BLANK_CELL}
        missing = [
            number
            for number in range(MIN_FILLED_CELL_VALUE, MAX_CELL_VALUE + 1)
            if number not in present
        ]
        if len(missing) != 2:
            raise GridNotComplete(
                f"Expected 2 missing numbers, found {len(missing)}."
            )

        small, large = missing[0], missing[1]
        return small, large
