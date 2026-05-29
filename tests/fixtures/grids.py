"""Shared grid fixtures for Magic Square tests."""

from typing import Final

VALID_GRID_TWO_BLANKS: Final[list[list[int]]] = [
    [1, 15, 14, 4],
    [12, 6, 0, 9],
    [8, 10, 11, 5],
    [13, 3, 2, 0],
]

# Boundary domain_spy mock return only — not real solver output (Golden: [2,3,7,4,4,16]).
VALID_GRID_SUCCESS_RESULT: Final[list[int]] = [2, 3, 5, 4, 1, 11]

KNOWN_MAGIC_SQUARE: Final[list[list[int]]] = [
    [1, 15, 14, 4],
    [12, 6, 7, 9],
    [8, 10, 11, 5],
    [13, 3, 2, 16],
]

# All row sums stay 34; column 0 breaks (Phase 0 — judge column branch).
GRID_ALL_ROWS_VALID_COLUMN_BROKEN: Final[list[list[int]]] = [
    [15, 1, 14, 4],
    [12, 6, 7, 9],
    [8, 10, 11, 5],
    [13, 3, 2, 16],
]

# Row and column sums stay 34; main diagonal breaks (Phase 5 — judge branch).
GRID_ALL_ROWS_VALID_MAIN_DIAG_BROKEN: Final[list[list[int]]] = [
    [2, 14, 14, 4],
    [11, 7, 7, 9],
    [8, 10, 11, 5],
    [13, 3, 2, 16],
]

# Row and column sums stay 34; anti diagonal breaks (Phase 5 — judge branch).
GRID_ALL_ROWS_VALID_ANTI_DIAG_BROKEN: Final[list[list[int]]] = [
    [1, 15, 15, 3],
    [12, 6, 6, 10],
    [8, 10, 11, 5],
    [13, 3, 2, 16],
]

GRID_3_BY_4: Final[list[list[int]]] = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
]

GRID_4_BY_5: Final[list[list[int]]] = [
    [1, 2, 3, 4, 5],
    [6, 7, 8, 9, 10],
    [11, 12, 13, 14, 15],
    [16, 1, 2, 3, 4],
]

GRID_1_BY_4: Final[list[list[int]]] = [[1, 2, 3, 4]]

GRID_1D: Final[list[int]] = list(range(1, 17))

GRID_JAGGED: Final[list[list[int]]] = [
    [1, 2, 3, 4],
    [5, 6, 7],
    [8, 9, 10, 11],
    [12, 13, 14, 15],
]

GRID_WITH_FLOAT: Final[list[list[float]]] = [
    [1.0, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16],
]

GRID_NESTED_DEPTH: Final[list[list[list[int]]]] = [[[1]]]

GRID_3_BY_4_WITH_17: Final[list[list[int]]] = [
    [17, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
]

GRID_BLANK_3_WITH_DUPLICATE: Final[list[list[int]]] = [
    [1, 2, 3, 4],
    [5, 6, 7, 7],
    [9, 10, 0, 12],
    [13, 0, 0, 16],
]

GRID_BLANK_0: Final[list[list[int]]] = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16],
]

GRID_BLANK_1: Final[list[list[int]]] = [
    [1, 2, 3, 4],
    [5, 6, 0, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16],
]

GRID_BLANK_3: Final[list[list[int]]] = [
    [1, 2, 3, 4],
    [5, 0, 7, 8],
    [9, 10, 0, 12],
    [13, 0, 15, 16],
]

GRID_DUPLICATE_NON_ZERO: Final[list[list[int]]] = [
    [1, 2, 3, 4],
    [5, 6, 7, 7],
    [9, 10, 0, 12],
    [13, 14, 0, 16],
]

GRID_INCOMPLETE_WITH_ZERO: Final[list[list[int]]] = [
    [1, 2, 3, 4],
    [5, 6, 0, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16],
]

GRID_BLANKS_0_0_3_3: Final[list[list[int]]] = [
    [0, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 0],
]

GRID_BLANKS_1_2_2_1: Final[list[list[int]]] = [
    [1, 2, 3, 4],
    [5, 6, 0, 8],
    [9, 0, 11, 12],
    [13, 14, 15, 16],
]

GRID_MISSING_15_16: Final[list[list[int]]] = [
    [1, 0, 14, 4],
    [12, 6, 7, 9],
    [8, 10, 11, 5],
    [13, 3, 2, 0],
]

GRID_MISSING_3_7: Final[list[list[int]]] = [
    [0, 2, 4, 5],
    [6, 8, 9, 10],
    [11, 12, 13, 14],
    [15, 16, 0, 1],
]

GRID_CORNER_BLANK_0_0: Final[list[list[int]]] = [
    [0, 15, 14, 4],
    [12, 6, 7, 9],
    [8, 10, 11, 5],
    [13, 3, 2, 0],
]

# First trial fails, second succeeds; blanks (1,2) and (2,0); missing 3 and 7.
GRID_PUZZLE_SECOND_TRIAL: Final[list[list[int]]] = [
    [16, 5, 9, 4],
    [2, 11, 0, 14],
    [0, 10, 6, 15],
    [13, 8, 12, 1],
]

GRID_UNSOLVABLE: Final[list[list[int]]] = [
    [1, 2, 3, 4],
    [5, 6, 0, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 0],
]
