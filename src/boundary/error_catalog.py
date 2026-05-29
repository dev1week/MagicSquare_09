"""Fixed error codes and messages for Boundary contract (BT-08)."""

from typing import Final

ERROR_CATALOG: Final[dict[str, str]] = {
    "INVALID_SIZE": "Grid must be 4x4.",
    "CELL_VALUE_OUT_OF_RANGE": "Cell value must be 0 or 1 through 16.",
    "DUPLICATE_NON_ZERO": "Non-zero values must not repeat.",
    "EMPTY_CELL_COUNT_INVALID": "Exactly two blank cells (0) are required.",
    "DOMAIN_UNSOLVABLE": "The grid cannot be completed into a magic square.",
}
