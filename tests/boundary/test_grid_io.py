"""Tests for GUI grid parsing helpers."""

import pytest

from src.boundary.ui.grid_io import (
    GridParseError,
    apply_solution,
    format_cell,
    grid_to_cell_texts,
    parse_cell_text,
    read_grid,
)


@pytest.mark.boundary
def test_parse_cell_text_blank_as_zero() -> None:
    assert parse_cell_text("") == 0
    assert parse_cell_text("0") == 0


@pytest.mark.boundary
def test_parse_cell_text_rejects_non_numeric() -> None:
    with pytest.raises(GridParseError):
        parse_cell_text("x")


@pytest.mark.boundary
def test_read_grid_round_trip() -> None:
    grid = [[1, 0, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
    texts = grid_to_cell_texts(grid)
    assert read_grid(texts) == grid


@pytest.mark.boundary
def test_apply_solution_fills_blanks() -> None:
    grid = [
        [1, 15, 14, 4],
        [12, 6, 0, 9],
        [8, 10, 11, 5],
        [13, 3, 2, 0],
    ]
    filled = apply_solution(grid, [2, 3, 7, 4, 4, 16])
    assert filled[1][2] == 7
    assert filled[3][3] == 16


@pytest.mark.boundary
def test_format_cell_shows_blank_as_empty() -> None:
    assert format_cell(0) == ""
    assert format_cell(7) == "7"
