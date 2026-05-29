"""Boundary Error Contract RED tests ??AC-US-01-07 via resolver path."""

import pytest

from src.boundary.schemas import ErrorResponse
from tests.fixtures.grids import GRID_BLANK_1, GRID_DUPLICATE_NON_ZERO


@pytest.mark.boundary
@pytest.mark.p2
@pytest.mark.parametrize(
    ("grid", "expected_code"),
    [
        pytest.param(None, "INVALID_SIZE", id="invalid_size"),
        pytest.param(GRID_BLANK_1, "EMPTY_CELL_COUNT_INVALID", id="empty_count"),
        pytest.param(GRID_DUPLICATE_NON_ZERO, "DUPLICATE_NON_ZERO", id="duplicate"),
    ],
)
def test_resolver_errors_conform_to_error_response_schema(
    boundary_resolver,
    domain_spy,
    grid: object,
    expected_code: str,
) -> None:
    """AC-US-01-07 ??resolver errors validate as ErrorResponse with fixed code."""
    # AC-US-01-07
    # Given
    # grid from parametrize

    # When
    result = boundary_resolver.solve(grid)

    # Then
    domain_spy.execute.assert_not_called()
    validated = ErrorResponse.model_validate(
        {"code": result.code, "message": result.message}
    )
    assert validated.code == expected_code
