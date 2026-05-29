"""AC-US-01-05/06 — Domain resolver call isolation via boundary spy."""

import pytest

from src.domain.exceptions import UnsolvableGrid
from tests.fixtures.grids import (
    GRID_1D,
    GRID_3_BY_4,
    GRID_BLANK_0,
    GRID_BLANK_1,
    GRID_DUPLICATE_NON_ZERO,
    GRID_JAGGED,
    VALID_GRID_TWO_BLANKS,
)


@pytest.mark.boundary
@pytest.mark.p0
@pytest.mark.parametrize(
    ("grid", "case_id"),
    [
        pytest.param(None, "EC1-01", id="none"),
        pytest.param([], "EC1-02", id="empty"),
        pytest.param(GRID_3_BY_4, "EC1-04", id="3x4"),
        pytest.param(GRID_1D, "EC1-06", id="1d"),
        pytest.param(GRID_JAGGED, "EC1-07", id="jagged"),
        pytest.param(
            [
                [1, 2, 3, 4],
                [5, 6, 0, 8],
                [9, 10, 11, 12],
                [13, 14, 15, 17],
            ],
            "EC2-01",
            id="value_17",
        ),
        pytest.param(GRID_BLANK_0, "EC3-01", id="blank_0"),
        pytest.param(GRID_BLANK_1, "EC3-02", id="blank_1"),
        pytest.param(GRID_DUPLICATE_NON_ZERO, "EC4-01", id="duplicate"),
    ],
)
def test_ic_violation_never_calls_domain_execute(
    boundary_resolver,
    domain_spy,
    grid: object,
    case_id: str,
) -> None:
    """AC-US-01-06 — every IC-1~IC-4 violation skips Domain execute."""
    # AC-US-01-06
    # Given
    # grid from parametrize

    # When
    boundary_resolver.solve(grid)

    # Then
    domain_spy.execute.assert_not_called()
    assert case_id


@pytest.mark.boundary
@pytest.mark.p0
def test_valid_grid_calls_domain_execute_exactly_once(
    boundary_resolver,
    domain_spy,
) -> None:
    """AC-US-01-05 — valid grid invokes Domain execute once."""
    # AC-US-01-05
    # Given
    grid = VALID_GRID_TWO_BLANKS

    # When
    boundary_resolver.solve(grid)

    # Then
    domain_spy.execute.assert_called_once_with(grid)


@pytest.mark.boundary
@pytest.mark.p1
def test_domain_unsolvable_still_calls_execute_once(
    boundary_resolver,
    domain_spy,
) -> None:
    """AC-US-01-05 — Domain failure after valid IC still means one execute call."""
    # AC-US-01-05
    # Given
    grid = VALID_GRID_TWO_BLANKS
    domain_spy.execute.side_effect = UnsolvableGrid()

    # When
    boundary_resolver.solve(grid)

    # Then
    domain_spy.execute.assert_called_once_with(grid)
