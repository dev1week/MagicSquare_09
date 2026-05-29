"""Integration-layer pytest fixtures."""

import pytest


@pytest.fixture
def boundary_resolver_integration():
    """Boundary resolver with real Domain (no Domain spy)."""
    from src.boundary.resolver import BoundaryResolver

    return BoundaryResolver()
