"""Parse and format 4×4 grid values for the GUI."""

from typing import Final

GRID_SIZE: Final[int] = 4


class GridParseError(ValueError):
    """Raised when a cell text value cannot be converted to a grid integer."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


def parse_cell_text(text: str) -> int:
    """Parse one cell: empty or ``0`` → blank; otherwise 1..16."""
    stripped = text.strip()
    if stripped == "" or stripped == "0":
        return 0

    if not stripped.isdigit():
        raise GridParseError(f"Cell must be empty, 0, or 1–16 (got {text!r}).")

    value = int(stripped)
    if value < 0 or value > 16:
        raise GridParseError(f"Cell value must be 0 or 1–16 (got {value}).")

    return value


def read_grid(cell_texts: list[list[str]]) -> list[list[int]]:
    """Convert a 4×4 matrix of UI strings into integers."""
    if len(cell_texts) != GRID_SIZE:
        raise GridParseError("Grid must have exactly 4 rows.")

    grid: list[list[int]] = []
    for row_index, row in enumerate(cell_texts):
        if len(row) != GRID_SIZE:
            raise GridParseError(f"Row {row_index + 1} must have exactly 4 cells.")
        grid.append([parse_cell_text(cell) for cell in row])

    return grid


def format_cell(value: int) -> str:
    """Format a grid value for display; blank cells show empty text."""
    return "" if value == 0 else str(value)


def grid_to_cell_texts(grid: list[list[int]]) -> list[list[str]]:
    """Convert integers to UI strings."""
    return [[format_cell(value) for value in row] for row in grid]


def apply_solution(grid: list[list[int]], result: list[int]) -> list[list[int]]:
    """Fill blank cells using a 1-index ``[r1,c1,n1,r2,c2,n2]`` solution vector."""
    if len(result) != 6:
        raise ValueError("Solution vector must have length 6.")

    r1, c1, n1, r2, c2, n2 = result
    filled = [row[:] for row in grid]
    filled[r1 - 1][c1 - 1] = n1
    filled[r2 - 1][c2 - 1] = n2
    return filled
