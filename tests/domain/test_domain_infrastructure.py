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
