"""EmptyCellLocator RED tests ??DT-01, US-02."""

import pytest

from src.domain.empty_cell_locator import EmptyCellLocator
from tests.fixtures.grids import VALID_GRID_TWO_BLANKS


@pytest.fixture
def locator() -> EmptyCellLocator:
    """EmptyCellLocator SUT."""
    return EmptyCellLocator()


@pytest.mark.domain
@pytest.mark.p0
def test_two_blanks_at_1_2_and_3_3_returns_row_major_zero_index(
    locator: EmptyCellLocator,
) -> None:
    """DT-01 ??returns two blank coordinates in row-major 0-index order."""
    # AC-US-02-02
    # Given
    grid = [
        [1, 2, 3, 4],
        [5, 6, 0, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 0],
    ]

    # When
    first, second = locator.locate(grid)

    # Then
    assert first == (1, 2)
    assert second == (3, 3)


@pytest.mark.domain
@pytest.mark.p0
def test_blanks_at_0_0_and_3_3_returns_row_major_order(
    locator: EmptyCellLocator,
) -> None:
    """DT-01 ??row-major ordering when blanks span corners."""
    # AC-US-02-03
    # Given
    grid = [
        [0, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 0],
    ]

    # When
    first, second = locator.locate(grid)

    # Then
    assert first == (0, 0)
    assert second == (3, 3)


@pytest.mark.domain
@pytest.mark.p0
def test_non_zero_cells_are_excluded_from_blank_results(
    locator: EmptyCellLocator,
) -> None:
    """DT-01 ??only value 0 cells are reported as blanks."""
    # AC-US-02-01
    # Given
    grid = VALID_GRID_TWO_BLANKS

    # When
    first, second = locator.locate(grid)

    # Then
    assert grid[first[0]][first[1]] == 0
    assert grid[second[0]][second[1]] == 0
    assert (0, 0) not in {first, second}


@pytest.mark.domain
@pytest.mark.p0
def test_locate_returns_exactly_two_coordinates(
    locator: EmptyCellLocator,
) -> None:
    """DT-01 ??valid input always yields exactly two blank coordinates."""
    # AC-US-02-02
    # Given
    grid = VALID_GRID_TWO_BLANKS

    # When
    coordinates = locator.locate(grid)

    # Then
    assert len(coordinates) == 2


@pytest.mark.domain
@pytest.mark.p0
def test_blanks_1_2_2_1_returns_row_major_order(
    locator: EmptyCellLocator,
) -> None:
    """BL-02 ??blanks at (1,2) and (2,1) return row-major [(1,2), (2,1)]."""
    # AC-US-02-03
    # Given
    from tests.fixtures.grids import GRID_BLANKS_1_2_2_1

    grid = GRID_BLANKS_1_2_2_1

    # When
    first, second = locator.locate(grid)

    # Then
    assert first == (1, 2)
    assert second == (2, 1)


@pytest.mark.domain
@pytest.mark.p0
def test_blank_coordinates_are_zero_index_within_bounds(
    locator: EmptyCellLocator,
) -> None:
    """AC-US-02-04 ??coordinates are 0-index with 0 <= row, col <= 3."""
    # AC-US-02-04
    # Given
    grid = VALID_GRID_TWO_BLANKS

    # When
    first, second = locator.locate(grid)

    # Then
    for row, col in (first, second):
        assert 0 <= row <= 3
        assert 0 <= col <= 3


@pytest.mark.domain
@pytest.mark.p0
def test_returned_coordinates_match_all_zero_cells_in_grid(
    locator: EmptyCellLocator,
) -> None:
    """AC-US-02-05 ??every returned coordinate points to a zero cell."""
    # AC-US-02-05
    # Given
    grid = VALID_GRID_TWO_BLANKS
    expected_zeros = {
        (row, col)
        for row, row_cells in enumerate(grid)
        for col, value in enumerate(row_cells)
        if value == 0
    }

    # When
    first, second = locator.locate(grid)

    # Then
    assert {first, second} == expected_zeros
