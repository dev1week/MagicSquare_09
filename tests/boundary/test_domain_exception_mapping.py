"""Tests for Domain exception to Boundary error code mapping."""

import pytest

from src.boundary.domain_exception_mapping import boundary_error_code_for
from src.domain.exceptions import GridNotComplete, InvalidGridSize, UnsolvableGrid


@pytest.mark.boundary
@pytest.mark.parametrize(
    ("exc", "expected_code"),
    [
        pytest.param(UnsolvableGrid(), "DOMAIN_UNSOLVABLE", id="unsolvable"),
        pytest.param(GridNotComplete(), "INVALID_SIZE", id="grid_not_complete"),
        pytest.param(InvalidGridSize(), "INVALID_SIZE", id="invalid_grid_size"),
    ],
)
def test_boundary_error_code_for_domain_failures(
    exc: BaseException,
    expected_code: str,
) -> None:
    assert boundary_error_code_for(exc) == expected_code


@pytest.mark.boundary
def test_boundary_error_code_for_unknown_exception_returns_none() -> None:
    assert boundary_error_code_for(ValueError("unknown")) is None
