"""Resolve the two missing numbers from a partial grid."""


class MissingNumberResolver:
    """Determine which values from 1..16 are absent from the grid."""

    def resolve(self, grid: list[list[int]]) -> tuple[int, int]:
        """Return the two missing numbers in ascending order."""
        present = {value for row in grid for value in row if value != 0}
        missing = [number for number in range(1, 17) if number not in present]
        small, large = missing[0], missing[1]
        return small, large
