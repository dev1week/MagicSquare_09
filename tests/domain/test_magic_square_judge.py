"""MagicSquareJudge RED tests ??DT-03, DM-E01~02, US-04."""

import pytest

from src.domain.constants import MAGIC_CONSTANT
from src.domain.exceptions import GridNotComplete, InvalidGridSize
from src.domain.magic_square_judge import MagicSquareJudge
from tests.fixtures.grids import (
    GRID_3_BY_4,
    GRID_ALL_ROWS_VALID_ANTI_DIAG_BROKEN,
    GRID_ALL_ROWS_VALID_COLUMN_BROKEN,
    GRID_ALL_ROWS_VALID_MAIN_DIAG_BROKEN,
    GRID_INCOMPLETE_WITH_ZERO,
    KNOWN_MAGIC_SQUARE,
)


@pytest.fixture
def judge() -> MagicSquareJudge:
    """MagicSquareJudge SUT."""
    return MagicSquareJudge()


@pytest.mark.domain
@pytest.mark.p0
def test_known_magic_square_returns_true(
    judge: MagicSquareJudge,
) -> None:
    """DT-03 ??complete valid magic square passes all line sums."""
    # AC-US-04-06
    # Given
    grid = KNOWN_MAGIC_SQUARE

    # When
    result = judge.is_magic(grid)

    # Then
    assert result is True


@pytest.mark.domain
@pytest.mark.p0
def test_row_sum_not_34_returns_false(
    judge: MagicSquareJudge,
) -> None:
    """DT-03 ??any row sum != MAGIC_CONSTANT returns false."""
    # AC-US-04-07
    # Given
    grid = [row[:] for row in KNOWN_MAGIC_SQUARE]
    grid[0][0] = 2

    # When
    result = judge.is_magic(grid)

    # Then
    assert result is False


@pytest.mark.domain
@pytest.mark.p0
def test_column_sum_not_34_returns_false(
    judge: MagicSquareJudge,
) -> None:
    """DT-03 — column branch fails while all row sums remain MAGIC_CONSTANT."""
    # AC-US-04-07
    # Given — row sums preserved, column 0 broken
    grid = GRID_ALL_ROWS_VALID_COLUMN_BROKEN
    row_sums = [sum(row) for row in grid]

    # When
    result = judge.is_magic(grid)

    # Then
    assert all(total == MAGIC_CONSTANT for total in row_sums)
    assert result is False


@pytest.mark.domain
@pytest.mark.p0
def test_main_diagonal_sum_not_34_returns_false(
    judge: MagicSquareJudge,
) -> None:
    """DT-03 — main diagonal branch fails while all row sums remain MAGIC_CONSTANT."""
    # AC-US-04-07
    # Given
    grid = GRID_ALL_ROWS_VALID_MAIN_DIAG_BROKEN
    row_sums = [sum(row) for row in grid]

    # When
    result = judge.is_magic(grid)

    # Then
    assert all(total == MAGIC_CONSTANT for total in row_sums)
    assert result is False


@pytest.mark.domain
@pytest.mark.p0
def test_anti_diagonal_sum_not_34_returns_false(
    judge: MagicSquareJudge,
) -> None:
    """DT-03 — anti diagonal branch fails while all row sums remain MAGIC_CONSTANT."""
    # AC-US-04-07
    # Given
    grid = GRID_ALL_ROWS_VALID_ANTI_DIAG_BROKEN
    row_sums = [sum(row) for row in grid]

    # When
    result = judge.is_magic(grid)

    # Then
    assert all(total == MAGIC_CONSTANT for total in row_sums)
    assert result is False


@pytest.mark.domain
@pytest.mark.p0
def test_legacy_column_failure_fixture_still_returns_false(
    judge: MagicSquareJudge,
) -> None:
    """Legacy fixture — row may fail before column; kept for regression."""
    grid = [row[:] for row in KNOWN_MAGIC_SQUARE]
    grid[0][0] = 2
    grid[1][0] = 14
    assert judge.is_magic(grid) is False


@pytest.mark.domain
@pytest.mark.p0
def test_legacy_main_diagonal_failure_fixture_still_returns_false(
    judge: MagicSquareJudge,
) -> None:
    """Legacy fixture — row may fail before diagonal; kept for regression."""
    grid = [row[:] for row in KNOWN_MAGIC_SQUARE]
    grid[0][0] = 2
    grid[1][1] = 5
    assert judge.is_magic(grid) is False


@pytest.mark.domain
@pytest.mark.p0
def test_legacy_anti_diagonal_failure_fixture_still_returns_false(
    judge: MagicSquareJudge,
) -> None:
    """Legacy fixture — row may fail before diagonal; kept for regression."""
    grid = [row[:] for row in KNOWN_MAGIC_SQUARE]
    grid[0][3] = 2
    grid[3][0] = 15
    assert judge.is_magic(grid) is False


@pytest.mark.domain
@pytest.mark.p0
def test_magic_constant_is_34_not_literal_in_judge(
    judge: MagicSquareJudge,
) -> None:
    """DT-03 ??judge uses MAGIC_CONSTANT named constant."""
    # AC-US-04-08
    # Given / Then
    assert MAGIC_CONSTANT == 34
    assert judge.magic_constant == MAGIC_CONSTANT


@pytest.mark.domain
@pytest.mark.p0
def test_grid_with_zero_raises_grid_not_complete(
    judge: MagicSquareJudge,
) -> None:
    """DM-E01 ??incomplete grid with zero is not validated."""
    # AC-US-04-01
    # Given
    grid = GRID_INCOMPLETE_WITH_ZERO

    # When / Then
    with pytest.raises(GridNotComplete):
        judge.is_magic(grid)


@pytest.mark.domain
@pytest.mark.p0
def test_3_by_4_grid_raises_invalid_grid_size(
    judge: MagicSquareJudge,
) -> None:
    """DM-E02 ??non 4x4 grid raises InvalidGridSize."""
    # AC-US-04-01
    # Given
    grid = GRID_3_BY_4

    # When / Then
    with pytest.raises(InvalidGridSize):
        judge.is_magic(grid)


@pytest.mark.domain
@pytest.mark.p0
def test_all_row_sums_equal_magic_constant_when_true(
    judge: MagicSquareJudge,
) -> None:
    """AC-US-04-02 ??each row sum equals MAGIC_CONSTANT when magic."""
    # AC-US-04-02
    # Given
    grid = KNOWN_MAGIC_SQUARE

    # When
    row_sums = [sum(row) for row in grid]

    # Then
    assert judge.is_magic(grid) is True
    assert all(total == MAGIC_CONSTANT for total in row_sums)


@pytest.mark.domain
@pytest.mark.p0
def test_all_column_sums_equal_magic_constant_when_true(
    judge: MagicSquareJudge,
) -> None:
    """AC-US-04-03 ??each column sum equals MAGIC_CONSTANT when magic."""
    # AC-US-04-03
    # Given
    grid = KNOWN_MAGIC_SQUARE

    # When
    col_sums = [sum(grid[row][col] for row in range(4)) for col in range(4)]

    # Then
    assert judge.is_magic(grid) is True
    assert all(total == MAGIC_CONSTANT for total in col_sums)
