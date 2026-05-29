"""Boundary resolver RED tests ??BT-01~03, BT-07, DOM-01~02."""

import pytest

from src.domain.exceptions import UnsolvableGrid
from tests.fixtures.grids import (
    GRID_1D,
    GRID_1_BY_4,
    GRID_3_BY_4,
    GRID_3_BY_4_WITH_17,
    GRID_4_BY_5,
    GRID_BLANK_0,
    GRID_BLANK_1,
    GRID_BLANK_3,
    GRID_BLANK_3_WITH_DUPLICATE,
    GRID_DUPLICATE_NON_ZERO,
    GRID_JAGGED,
    GRID_NESTED_DEPTH,
    GRID_WITH_FLOAT,
    VALID_GRID_SUCCESS_RESULT,
    VALID_GRID_TWO_BLANKS,
)


@pytest.mark.boundary
@pytest.mark.p0
def test_none_grid_returns_invalid_size_without_domain_call(
    boundary_resolver,
    domain_spy,
) -> None:
    """BT-01 ??seed AC: grid=None rejects before Domain."""
    # AC-US-01-01
    # Given
    grid = None

    # When
    result = boundary_resolver.solve(grid)

    # Then
    assert result.code == "INVALID_SIZE"
    assert result.message == "Grid must be 4x4."
    domain_spy.execute.assert_not_called()


@pytest.mark.boundary
@pytest.mark.p0
@pytest.mark.parametrize(
    ("grid", "case_id"),
    [
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
def test_non_4x4_grid_returns_invalid_size_no_domain_call(
    boundary_resolver,
    domain_spy,
    grid: object,
    case_id: str,
) -> None:
    """BT-02 ??invalid grid shape rejects at Boundary without Domain call."""
    # AC-US-01-01
    # Given
    # grid from parametrize

    # When
    result = boundary_resolver.solve(grid)

    # Then
    assert result.code == "INVALID_SIZE"
    domain_spy.execute.assert_not_called()
    assert case_id  # traceability anchor


@pytest.mark.boundary
@pytest.mark.p1
@pytest.mark.parametrize(
    ("grid", "expected_code", "case_id"),
    [
        pytest.param(
            [
                [1, 2, 3, 4],
                [5, 6, 0, 8],
                [9, 10, 11, 12],
                [13, 14, 15, 17],
            ],
            "CELL_VALUE_OUT_OF_RANGE",
            "EC2-01",
            id="seventeen",
        ),
        pytest.param(GRID_BLANK_0, "EMPTY_CELL_COUNT_INVALID", "EC3-01", id="zero_blanks"),
        pytest.param(GRID_BLANK_1, "EMPTY_CELL_COUNT_INVALID", "EC3-02", id="one_blank"),
        pytest.param(GRID_BLANK_3, "EMPTY_CELL_COUNT_INVALID", "EC3-03", id="three_blanks"),
        pytest.param(
            GRID_DUPLICATE_NON_ZERO,
            "DUPLICATE_NON_ZERO",
            "EC4-01",
            id="duplicate",
        ),
    ],
)
def test_contract_violation_returns_error_no_domain_call(
    boundary_resolver,
    domain_spy,
    grid: list[list[int]],
    expected_code: str,
    case_id: str,
) -> None:
    """BT-04~06 ??IC violations reject at Boundary without Domain call."""
    # AC-US-01-02
    # Given
    # grid from parametrize

    # When
    result = boundary_resolver.solve(grid)

    # Then
    assert result.code == expected_code
    domain_spy.execute.assert_not_called()
    assert case_id  # traceability anchor


@pytest.mark.boundary
@pytest.mark.p0
def test_valid_grid_delegates_once_to_domain(
    boundary_resolver,
    domain_spy,
) -> None:
    """BT-03 ??valid input invokes Domain exactly once."""
    # AC-US-01-05
    # Given
    grid = VALID_GRID_TWO_BLANKS

    # When
    result = boundary_resolver.solve(grid)

    # Then
    domain_spy.execute.assert_called_once_with(grid)
    assert result.result == VALID_GRID_SUCCESS_RESULT


@pytest.mark.boundary
@pytest.mark.p1
def test_unsolvable_domain_failure_maps_to_domain_unsolvable(
    boundary_resolver,
    domain_spy,
    mocker,
) -> None:
    """DOM-01 ??Domain UnsolvableGrid maps to DOMAIN_UNSOLVABLE."""
    # AC-US-01-05
    # Given
    grid = VALID_GRID_TWO_BLANKS
    domain_spy.execute.side_effect = UnsolvableGrid()

    # When
    result = boundary_resolver.solve(grid)

    # Then
    assert result.code == "DOMAIN_UNSOLVABLE"
    domain_spy.execute.assert_called_once_with(grid)


@pytest.mark.boundary
@pytest.mark.p1
def test_3_by_4_with_17_returns_invalid_size_not_out_of_range(
    boundary_resolver,
    domain_spy,
) -> None:
    """BT-07 / ORD-01 ??size check precedes value range check."""
    # AC-US-01-01
    # Given
    grid = GRID_3_BY_4_WITH_17

    # When
    result = boundary_resolver.solve(grid)

    # Then
    assert result.code == "INVALID_SIZE"
    domain_spy.execute.assert_not_called()


@pytest.mark.boundary
@pytest.mark.p1
def test_blank_3_with_duplicate_returns_empty_count_not_duplicate(
    boundary_resolver,
    domain_spy,
) -> None:
    """BT-07 / ORD-02 ??empty count check precedes duplicate check."""
    # AC-US-01-03
    # Given
    grid = GRID_BLANK_3_WITH_DUPLICATE

    # When
    result = boundary_resolver.solve(grid)

    # Then
    assert result.code == "EMPTY_CELL_COUNT_INVALID"
    domain_spy.execute.assert_not_called()


@pytest.mark.boundary
@pytest.mark.p1
@pytest.mark.parametrize(
    ("cell_value", "case_id"),
    [
        pytest.param(-1, "EC2-02", id="negative_one"),
        pytest.param("7", "EC2-03", id="string_seven"),
        pytest.param(None, "EC2-04", id="none_cell"),
    ],
)
def test_out_of_range_cell_returns_error_no_domain_call(
    boundary_resolver,
    domain_spy,
    cell_value: object,
    case_id: str,
) -> None:
    """BT-04 ??EC2-02~04 reject at Boundary without Domain call."""
    # AC-US-01-02
    # Given
    grid = [
        [1, 2, 3, 4],
        [5, 6, 0, 8],
        [9, 10, 11, 12],
        [13, 14, 15, cell_value],
    ]

    # When
    result = boundary_resolver.solve(grid)

    # Then
    assert result.code == "CELL_VALUE_OUT_OF_RANGE"
    domain_spy.execute.assert_not_called()
    assert case_id
