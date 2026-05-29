"""IT-01 — success output text format `OK [r1,c1,n1,r2,c2,n2]`."""

import pytest

from tests.fixtures.grids import VALID_GRID_TWO_BLANKS


@pytest.mark.integration
@pytest.mark.p2
def test_success_response_formats_ok_prefix_without_spaces(
    boundary_resolver_integration,
) -> None:
    """IT-01 — Boundary success uses `OK [r1,c1,n1,r2,c2,n2]` text format."""
    # AC-US-05-06
    # Given
    from src.boundary.response_formatter import ResponseFormatter

    grid = VALID_GRID_TWO_BLANKS

    # When
    result = boundary_resolver_integration.solve(grid)
    formatted = ResponseFormatter.format_success(result.result)

    # Then
    assert formatted.startswith("OK [")
    assert formatted.endswith("]")
    assert " " not in formatted.removeprefix("OK ")


@pytest.mark.integration
@pytest.mark.p2
def test_success_formatted_output_has_six_comma_separated_integers(
    boundary_resolver_integration,
) -> None:
    """OC-1~OC-2 — formatted success contains exactly six integers."""
    # AC-US-05-06
    # Given
    from src.boundary.response_formatter import ResponseFormatter

    grid = VALID_GRID_TWO_BLANKS

    # When
    result = boundary_resolver_integration.solve(grid)
    formatted = ResponseFormatter.format_success(result.result)
    payload = formatted.removeprefix("OK [").removesuffix("]")
    parts = payload.split(",")

    # Then
    assert len(parts) == 6
    assert all(part.isdigit() for part in parts)
