"""Sample grids for the GUI (mirrors tests/fixtures/grids.py)."""

from typing import Final

SAMPLE_PUZZLE: Final[list[list[int]]] = [
    [1, 15, 14, 4],
    [12, 6, 0, 9],
    [8, 10, 11, 5],
    [13, 3, 2, 0],
]

SAMPLE_MAGIC_SQUARE: Final[list[list[int]]] = [
    [1, 15, 14, 4],
    [12, 6, 7, 9],
    [8, 10, 11, 5],
    [13, 3, 2, 16],
]
