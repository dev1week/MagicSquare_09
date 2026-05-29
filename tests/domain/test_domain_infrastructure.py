"""Domain infrastructure RED tests — constants and exceptions."""

import pytest


@pytest.mark.domain
@pytest.mark.p0
def test_magic_constant_is_named_34() -> None:
    """AC-US-04-08 — MAGIC_CONSTANT module defines 34."""
    # AC-US-04-08
    # Given / When
    from src.domain.constants import MAGIC_CONSTANT

    # Then
    assert MAGIC_CONSTANT == 34


@pytest.mark.domain
@pytest.mark.p0
def test_grid_constants_are_centralized() -> None:
    """Phase 2 — grid invariants live in constants module (SSOT)."""
    from src.domain.constants import (
        BLANK_CELL,
        CELL_COUNT,
        GRID_SIZE,
        MAX_CELL_VALUE,
        MIN_FILLED_CELL_VALUE,
        MIN_PARTIAL_CELL_VALUE,
        REQUIRED_BLANK_COUNT,
        SOLUTION_VECTOR_LENGTH,
    )

    assert GRID_SIZE == 4
    assert CELL_COUNT == 16
    assert BLANK_CELL == 0
    assert MIN_PARTIAL_CELL_VALUE == 0
    assert MIN_FILLED_CELL_VALUE == 1
    assert MAX_CELL_VALUE == 16
    assert REQUIRED_BLANK_COUNT == 2
    assert SOLUTION_VECTOR_LENGTH == 6


@pytest.mark.domain
@pytest.mark.p0
def test_domain_exceptions_are_defined() -> None:
    """Domain failure types exist for DM-E01~03 and EC-5."""
    # AC-US-04-01
    # Given / When
    from src.domain.exceptions import (
        GridNotComplete,
        InvalidGridSize,
        UnsolvableGrid,
    )

    # Then
    assert issubclass(GridNotComplete, Exception)
    assert issubclass(InvalidGridSize, Exception)
    assert issubclass(UnsolvableGrid, Exception)
