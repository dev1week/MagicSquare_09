"""Input validator RED tests ??IC-1~IC-4, BT-02~06, EC-1 extensions."""

import pytest

from src.boundary.input_validator import InputValidator
from tests.fixtures.grids import (
    GRID_1D,
    GRID_1_BY_4,
    GRID_3_BY_4,
    GRID_4_BY_5,
    GRID_BLANK_0,
    GRID_BLANK_1,
    GRID_BLANK_3,
    GRID_DUPLICATE_NON_ZERO,
    GRID_JAGGED,
    GRID_NESTED_DEPTH,
    GRID_WITH_FLOAT,
)


@pytest.fixture
def validator() -> InputValidator:
    """InputValidator SUT."""
    return InputValidator()


@pytest.mark.boundary
@pytest.mark.p0
@pytest.mark.parametrize(
    ("grid", "case_id"),
    [
        pytest.param(None, "EC1-01", id="none"),
        pytest.param([], "EC1-02", id="empty_list"),
        pytest.param(GRID_1_BY_4, "EC1-03", id="one_by_four"),
        pytest.param(GRID_3_BY_4, "EC1-04", id="three_by_four"),
        pytest.param(GRID_4_BY_5, "EC1-05", id="four_by_five"),
        pytest.param(GRID_1D, "EC1-06", id="one_dimensional"),
        pytest.param(GRID_JAGGED, "EC1-07", id="jagged"),
        pytest.param(GRID_WITH_FLOAT, "EC1-08", id="float_cell"),
        pytest.param(GRID_NESTED_DEPTH, "EC1-09", id="nested_depth"),
    ],
)
def test_non_4x4_grid_returns_invalid_size(
    validator: InputValidator,
    grid: object,
    case_id: str,
) -> None:
    """BT-02 ??non 4x4 structures reject with INVALID_SIZE."""
    # AC-US-01-01
    # Given
    # grid from parametrize

    # When
    error = validator.validate(grid)

    # Then
    assert error is not None
    assert error.code == "INVALID_SIZE"
    assert case_id  # traceability anchor


@pytest.mark.boundary
@pytest.mark.p1
@pytest.mark.parametrize(
    ("value", "case_id"),
    [
        pytest.param(17, "EC2-01", id="seventeen"),
        pytest.param(-1, "EC2-02", id="negative_one"),
        pytest.param("7", "EC2-03", id="string_seven"),
        pytest.param(None, "EC2-04", id="none_cell"),
    ],
)
def test_out_of_range_cell_returns_cell_value_out_of_range(
    validator: InputValidator,
    value: object,
    case_id: str,
) -> None:
    """BT-04 ??cell value violations reject with CELL_VALUE_OUT_OF_RANGE."""
    # AC-US-01-02
    # Given
    grid = [
        [1, 2, 3, 4],
        [5, 6, 0, 8],
        [9, 10, 11, 12],
        [13, 14, 15, value],
    ]

    # When
    error = validator.validate(grid)

    # Then
    assert error is not None
    assert error.code == "CELL_VALUE_OUT_OF_RANGE"
    assert case_id  # traceability anchor


@pytest.mark.boundary
@pytest.mark.p1
@pytest.mark.parametrize(
    ("grid", "case_id"),
    [
        pytest.param(GRID_BLANK_0, "EC3-01", id="zero_blanks"),
        pytest.param(GRID_BLANK_1, "EC3-02", id="one_blank"),
        pytest.param(GRID_BLANK_3, "EC3-03", id="three_blanks"),
    ],
)
def test_invalid_blank_count_returns_empty_cell_count_invalid(
    validator: InputValidator,
    grid: list[list[int]],
    case_id: str,
) -> None:
    """BT-05 ??blank count != 2 rejects with EMPTY_CELL_COUNT_INVALID."""
    # AC-US-01-03
    # Given
    # grid from parametrize

    # When
    error = validator.validate(grid)

    # Then
    assert error is not None
    assert error.code == "EMPTY_CELL_COUNT_INVALID"
    assert case_id  # traceability anchor


@pytest.mark.boundary
@pytest.mark.p1
def test_duplicate_non_zero_returns_duplicate_non_zero(
    validator: InputValidator,
) -> None:
    """BT-06 ??duplicate non-zero values reject with DUPLICATE_NON_ZERO."""
    # AC-US-01-04
    # Given
    grid = GRID_DUPLICATE_NON_ZERO

    # When
    error = validator.validate(grid)

    # Then
    assert error is not None
    assert error.code == "DUPLICATE_NON_ZERO"
