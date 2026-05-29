"""Tests for complete-grid verification at Boundary."""

from unittest.mock import create_autospec

import pytest

from src.boundary.complete_grid_verifier import CompleteGridVerifier, VerifyError, VerifySuccess
from src.domain.exceptions import GridNotComplete, InvalidGridSize
from src.domain.magic_square_judge import MagicSquareJudge
from tests.fixtures.grids import GRID_3_BY_4, GRID_JAGGED, KNOWN_MAGIC_SQUARE


@pytest.fixture
def verifier() -> CompleteGridVerifier:
    return CompleteGridVerifier()


@pytest.mark.boundary
def test_known_magic_square_verifies_true(verifier: CompleteGridVerifier) -> None:
    result = verifier.verify(KNOWN_MAGIC_SQUARE)
    assert isinstance(result, VerifySuccess)
    assert result.is_magic is True
    assert result.magic_constant == 34


@pytest.mark.boundary
def test_incomplete_grid_returns_error(verifier: CompleteGridVerifier) -> None:
    grid = [row[:] for row in KNOWN_MAGIC_SQUARE]
    grid[0][0] = 0
    result = verifier.verify(grid)
    assert isinstance(result, VerifyError)
    assert result.code == "CELL_VALUE_OUT_OF_RANGE"


@pytest.mark.boundary
def test_duplicate_values_return_error(verifier: CompleteGridVerifier) -> None:
    grid = [row[:] for row in KNOWN_MAGIC_SQUARE]
    grid[0][0] = grid[0][1]
    result = verifier.verify(grid)
    assert isinstance(result, VerifyError)
    assert result.code == "DUPLICATE_NON_ZERO"


@pytest.mark.boundary
@pytest.mark.parametrize(
    "grid",
    [
        pytest.param(None, id="none"),
        pytest.param(GRID_3_BY_4, id="three_by_four"),
        pytest.param([], id="empty"),
    ],
)
def test_invalid_size_grid_returns_invalid_size(
    verifier: CompleteGridVerifier,
    grid: object,
) -> None:
    result = verifier.verify(grid)
    assert isinstance(result, VerifyError)
    assert result.code == "INVALID_SIZE"


@pytest.mark.boundary
def test_jagged_row_returns_invalid_size(verifier: CompleteGridVerifier) -> None:
    result = verifier.verify(GRID_JAGGED)
    assert isinstance(result, VerifyError)
    assert result.code == "INVALID_SIZE"


@pytest.mark.boundary
def test_non_int_cell_returns_cell_value_out_of_range(
    verifier: CompleteGridVerifier,
) -> None:
    grid = [row[:] for row in KNOWN_MAGIC_SQUARE]
    grid[0][0] = "7"  # type: ignore[assignment]
    result = verifier.verify(grid)
    assert isinstance(result, VerifyError)
    assert result.code == "CELL_VALUE_OUT_OF_RANGE"


@pytest.mark.boundary
def test_complete_non_magic_grid_returns_is_magic_false(
    verifier: CompleteGridVerifier,
) -> None:
    grid = [row[:] for row in KNOWN_MAGIC_SQUARE]
    grid[0][0], grid[0][2] = grid[0][2], grid[0][0]
    result = verifier.verify(grid)
    assert isinstance(result, VerifySuccess)
    assert result.is_magic is False


@pytest.mark.boundary
def test_judge_grid_not_complete_maps_to_invalid_size() -> None:
    judge = create_autospec(MagicSquareJudge, instance=True)
    judge.is_magic.side_effect = GridNotComplete()
    verifier = CompleteGridVerifier(judge=judge)

    result = verifier.verify(KNOWN_MAGIC_SQUARE)

    assert isinstance(result, VerifyError)
    assert result.code == "INVALID_SIZE"


@pytest.mark.boundary
def test_judge_invalid_grid_size_maps_to_invalid_size() -> None:
    judge = create_autospec(MagicSquareJudge, instance=True)
    judge.is_magic.side_effect = InvalidGridSize()
    verifier = CompleteGridVerifier(judge=judge)

    result = verifier.verify(KNOWN_MAGIC_SQUARE)

    assert isinstance(result, VerifyError)
    assert result.code == "INVALID_SIZE"
