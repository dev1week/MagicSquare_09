"""Parse and format 4×4 grid values for the GUI."""

from src.domain.constants import (
    BLANK_CELL,
    GRID_SIZE,
    MAX_CELL_VALUE,
    MIN_PARTIAL_CELL_VALUE,
    SOLUTION_VECTOR_LENGTH,
)


class GridParseError(ValueError):
    """Raised when a cell text value cannot be converted to a grid integer."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


def parse_cell_text(text: str) -> int:
    """Parse one cell: empty or ``0`` → blank; otherwise 1..16."""
    stripped = text.strip()
    if stripped == "" or stripped == str(BLANK_CELL):
        return BLANK_CELL

    if not stripped.isdigit():
        raise GridParseError(f"Cell must be empty, 0, or 1–16 (got {text!r}).")

    value = int(stripped)
    if value < MIN_PARTIAL_CELL_VALUE or value > MAX_CELL_VALUE:
        raise GridParseError(f"Cell value must be 0 or 1–16 (got {value}).")

    return value


def read_grid(cell_texts: list[list[str]]) -> list[list[int]]:
    """Convert a 4×4 matrix of UI strings into integers."""
    if len(cell_texts) != GRID_SIZE:
        raise GridParseError(f"Grid must have exactly {GRID_SIZE} rows.")

    grid: list[list[int]] = []
    for row_index, row in enumerate(cell_texts):
        if len(row) != GRID_SIZE:
            raise GridParseError(
                f"Row {row_index + 1} must have exactly {GRID_SIZE} cells."
            )
        grid.append([parse_cell_text(cell) for cell in row])

    return grid


def format_cell(value: int) -> str:
    """Format a grid value for display; blank cells show empty text."""
    return "" if value == BLANK_CELL else str(value)


def grid_to_cell_texts(grid: list[list[int]]) -> list[list[str]]:
    """Convert integers to UI strings."""
    return [[format_cell(value) for value in row] for row in grid]


def apply_solution(grid: list[list[int]], result: list[int]) -> list[list[int]]:
    """Fill blank cells using a 1-index ``[r1,c1,n1,r2,c2,n2]`` solution vector."""
    if len(result) != SOLUTION_VECTOR_LENGTH:
        raise ValueError(f"Solution vector must have length {SOLUTION_VECTOR_LENGTH}.")

    r1, c1, n1, r2, c2, n2 = result
    filled = [row[:] for row in grid]
    filled[r1 - 1][c1 - 1] = n1
    filled[r2 - 1][c2 - 1] = n2
    return filled
