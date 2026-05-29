"""AC-US-02-06 — BlankFinder does not perform Boundary input validation."""

import pytest

from src.domain.empty_cell_locator import EmptyCellLocator


@pytest.fixture
def locator() -> EmptyCellLocator:
    """EmptyCellLocator SUT."""
    return EmptyCellLocator()


@pytest.mark.domain
@pytest.mark.p0
def test_locator_has_no_input_validation_method(locator: EmptyCellLocator) -> None:
    """AC-US-02-06 — EmptyCellLocator exposes locate only, not validate."""
    # AC-US-02-06
    # Given / Then
    assert hasattr(locator, "locate")
    assert not hasattr(locator, "validate")


@pytest.mark.domain
@pytest.mark.p0
def test_out_of_range_cell_grid_still_returns_two_blank_coordinates(
    locator: EmptyCellLocator,
) -> None:
    """AC-US-02-06 — out-of-range values do not trigger Boundary-style rejection."""
    # AC-US-02-06
    # Given
    grid = [
        [17, 2, 3, 4],
        [5, 6, 0, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 0],
    ]

    # When
    first, second = locator.locate(grid)

    # Then
    assert grid[first[0]][first[1]] == 0
    assert grid[second[0]][second[1]] == 0
    assert first != second


@pytest.mark.domain
@pytest.mark.p0
def test_blanks_0_0_and_3_3_returns_corner_pair(
    locator: EmptyCellLocator,
) -> None:
    """BL-01 — blanks at (0,0) and (3,3) return [(0,0), (3,3)]."""
    # AC-US-02-03
    # Given
    from tests.fixtures.grids import GRID_BLANKS_0_0_3_3

    grid = GRID_BLANKS_0_0_3_3

    # When
    first, second = locator.locate(grid)

    # Then
    assert first == (0, 0)
    assert second == (3, 3)
