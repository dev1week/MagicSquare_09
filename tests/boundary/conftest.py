"""Boundary-layer pytest fixtures."""

from unittest.mock import create_autospec

import pytest


@pytest.fixture
def domain_spy(mocker):
    """Spy for Domain entry point — call count and argument verification.

    ``execute.return_value`` is a fixed mock vector (``VALID_GRID_SUCCESS_RESULT``),
    not the real solver output. Golden baseline: ``[2, 3, 7, 4, 4, 16]``.
    """
    from src.domain.solve_partial_grid import SolvePartialGrid
    from tests.fixtures.grids import VALID_GRID_SUCCESS_RESULT

    spy = create_autospec(SolvePartialGrid, instance=True)
    spy.execute.return_value = VALID_GRID_SUCCESS_RESULT
    mocker.patch(
        "src.boundary.resolver.SolvePartialGrid",
        return_value=spy,
    )
    return spy


@pytest.fixture
def boundary_resolver(domain_spy):
    """Boundary SUT with injected Domain spy."""
    from src.boundary.resolver import BoundaryResolver

    return BoundaryResolver()
