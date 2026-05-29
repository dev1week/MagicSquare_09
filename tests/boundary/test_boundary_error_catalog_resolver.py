"""BT-08 — resolver errors match catalog and ErrorResponse schema."""

import pytest

from src.boundary.schemas import ErrorResponse
from tests.fixtures.error_catalog import ERROR_CATALOG
from tests.fixtures.grids import (
    GRID_BLANK_1,
    GRID_DUPLICATE_NON_ZERO,
    GRID_JAGGED,
    VALID_GRID_TWO_BLANKS,
)


@pytest.mark.boundary
@pytest.mark.p2
@pytest.mark.parametrize(
    ("grid", "expected_code"),
    [
        pytest.param(None, "INVALID_SIZE", id="invalid_size"),
        pytest.param(GRID_JAGGED, "INVALID_SIZE", id="jagged"),
        pytest.param(
            [
                [1, 2, 3, 4],
                [5, 6, 0, 8],
                [9, 10, 11, 12],
                [13, 14, 15, -1],
            ],
            "CELL_VALUE_OUT_OF_RANGE",
            id="out_of_range",
        ),
        pytest.param(GRID_BLANK_1, "EMPTY_CELL_COUNT_INVALID", id="blank_count"),
        pytest.param(GRID_DUPLICATE_NON_ZERO, "DUPLICATE_NON_ZERO", id="duplicate"),
    ],
)
def test_resolver_error_matches_catalog_and_schema(
    boundary_resolver,
    domain_spy,
    grid: object,
    expected_code: str,
) -> None:
    """BT-08 / AC-US-01-07 — resolver errors use fixed catalog + pydantic schema."""
    # AC-US-01-07
    # Given
    expected_message = ERROR_CATALOG[expected_code]

    # When
    result = boundary_resolver.solve(grid)

    # Then
    domain_spy.execute.assert_not_called()
    assert result.code == expected_code
    assert result.message == expected_message
    validated = ErrorResponse.model_validate(
        {"code": result.code, "message": result.message}
    )
    assert validated.code == expected_code


@pytest.mark.boundary
@pytest.mark.p2
def test_domain_unsolvable_error_matches_catalog(
    boundary_resolver,
    domain_spy,
) -> None:
    """BT-08 — DOMAIN_UNSOLVABLE uses catalog message."""
    # AC-US-01-07
    # Given
    from src.domain.exceptions import UnsolvableGrid

    grid = VALID_GRID_TWO_BLANKS
    domain_spy.execute.side_effect = UnsolvableGrid()

    # When
    result = boundary_resolver.solve(grid)

    # Then
    assert result.code == "DOMAIN_UNSOLVABLE"
    assert result.message == ERROR_CATALOG["DOMAIN_UNSOLVABLE"]
    ErrorResponse.model_validate({"code": result.code, "message": result.message})
