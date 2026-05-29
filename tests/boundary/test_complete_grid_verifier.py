"""Tests for complete-grid verification at Boundary."""

import pytest

from src.boundary.complete_grid_verifier import CompleteGridVerifier
from tests.fixtures.grids import KNOWN_MAGIC_SQUARE


@pytest.fixture
def verifier() -> CompleteGridVerifier:
    return CompleteGridVerifier()


@pytest.mark.boundary
def test_known_magic_square_verifies_true(verifier: CompleteGridVerifier) -> None:
    result = verifier.verify(KNOWN_MAGIC_SQUARE)
    assert result.is_magic is True
    assert result.magic_constant == 34


@pytest.mark.boundary
def test_incomplete_grid_returns_error(verifier: CompleteGridVerifier) -> None:
    grid = [row[:] for row in KNOWN_MAGIC_SQUARE]
    grid[0][0] = 0
    result = verifier.verify(grid)
    assert result.code == "CELL_VALUE_OUT_OF_RANGE"


@pytest.mark.boundary
def test_duplicate_values_return_error(verifier: CompleteGridVerifier) -> None:
    grid = [row[:] for row in KNOWN_MAGIC_SQUARE]
    grid[0][0] = grid[0][1]
    result = verifier.verify(grid)
    assert result.code == "DUPLICATE_NON_ZERO"
