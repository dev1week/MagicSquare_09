"""RG-US-01 — Boundary resolver path regression for EC-1~EC-4."""

import pytest

from tests.fixtures.error_catalog import ERROR_CATALOG
from tests.fixtures.grids import (
    GRID_1D,
    GRID_3_BY_4,
    GRID_BLANK_0,
    GRID_BLANK_3,
    GRID_DUPLICATE_NON_ZERO,
    GRID_JAGGED,
)


@pytest.mark.regression
@pytest.mark.boundary
@pytest.mark.parametrize(
    ("grid", "expected_code"),
    [
        pytest.param(None, "INVALID_SIZE", id="ec1_none"),
        pytest.param(GRID_3_BY_4, "INVALID_SIZE", id="ec1_3x4"),
        pytest.param(GRID_1D, "INVALID_SIZE", id="ec1_1d"),
        pytest.param(GRID_JAGGED, "INVALID_SIZE", id="ec1_jagged"),
        pytest.param(
            [
                [1, 2, 3, 4],
                [5, 6, 0, 8],
                [9, 10, 11, 12],
                [13, 14, 15, 17],
            ],
            "CELL_VALUE_OUT_OF_RANGE",
            id="ec2_17",
        ),
        pytest.param(GRID_BLANK_0, "EMPTY_CELL_COUNT_INVALID", id="ec3_zero"),
        pytest.param(GRID_BLANK_3, "EMPTY_CELL_COUNT_INVALID", id="ec3_three"),
        pytest.param(GRID_DUPLICATE_NON_ZERO, "DUPLICATE_NON_ZERO", id="ec4_dup"),
    ],
)
def test_boundary_resolver_regression_matrix(
    boundary_resolver,
    domain_spy,
    grid: object,
    expected_code: str,
) -> None:
    """RG-US-01 — resolver returns catalog code and never calls Domain on IC errors."""
    # AC-US-01-07
    # Given
    expected_message = ERROR_CATALOG[expected_code]

    # When
    result = boundary_resolver.solve(grid)

    # Then
    domain_spy.execute.assert_not_called()
    assert result.code == expected_code
    assert result.message == expected_message
