"""Regression RED suite ??RG-US-01 (US-01 EC-1~EC-4)."""

import pytest

from src.boundary.input_validator import InputValidator
from tests.fixtures.grids import (
    GRID_1D,
    GRID_3_BY_4,
    GRID_BLANK_0,
    GRID_BLANK_3,
    GRID_DUPLICATE_NON_ZERO,
    GRID_JAGGED,
)


@pytest.fixture
def validator() -> InputValidator:
    """InputValidator SUT."""
    return InputValidator()


@pytest.mark.regression
@pytest.mark.boundary
@pytest.mark.parametrize(
    ("grid", "expected_code"),
    [
        pytest.param(None, "INVALID_SIZE", id="ec1_none"),
        pytest.param([], "INVALID_SIZE", id="ec1_empty"),
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
def test_us01_all_input_errors_return_expected_code(
    validator: InputValidator,
    grid: object,
    expected_code: str,
) -> None:
    """RG-US-01 ??EC-1~EC-4 regression matrix."""
    # AC-US-01-07
    # Given
    # grid from parametrize

    # When
    error = validator.validate(grid)

    # Then
    assert error is not None
    assert error.code == expected_code
