"""Boundary-layer pytest fixtures."""

from unittest.mock import create_autospec

import pytest


@pytest.fixture
def domain_spy(mocker):
    """Spy for Domain entry point ??call count and argument verification."""
    from src.domain.solve_partial_grid import SolvePartialGrid

    spy = create_autospec(SolvePartialGrid, instance=True)
    spy.execute.return_value = [2, 3, 5, 4, 1, 11]
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
