"""Integration RED tests ??Track C (IT-01, IT-02, IT-04, IT-06)."""

from unittest.mock import create_autospec

import pytest

from src.domain.solve_partial_grid import SolvePartialGrid
from tests.fixtures.grids import (
    GRID_3_BY_4,
    GRID_PUZZLE_SECOND_TRIAL,
    GRID_UNSOLVABLE,
    VALID_GRID_TWO_BLANKS,
)


@pytest.mark.integration
@pytest.mark.p2
def test_valid_grid_returns_six_element_result_it01(
    boundary_resolver_integration,
) -> None:
    """IT-01 ??valid input flows Boundary ??Domain ??success int[6]."""
    # AC-US-01-05
    # Given
    grid = VALID_GRID_TWO_BLANKS

    # When
    result = boundary_resolver_integration.solve(grid)

    # Then
    assert hasattr(result, "result")
    assert len(result.result) == 6
    r1, c1, n1, r2, c2, n2 = result.result
    assert 1 <= r1 <= 4 and 1 <= c1 <= 4
    assert 1 <= r2 <= 4 and 1 <= c2 <= 4
    assert 1 <= n1 <= 16 and 1 <= n2 <= 16
    assert n1 != n2


@pytest.mark.integration
@pytest.mark.p2
def test_3_by_4_rejects_without_domain_call_it04(
    boundary_resolver_integration,
    mocker,
) -> None:
    """IT-04 ??3×4 input returns INVALID_SIZE; Domain execute not called."""
    # AC-US-01-01
    # Given
    grid = GRID_3_BY_4
    domain_spy = create_autospec(SolvePartialGrid, instance=True)
    mocker.patch(
        "src.boundary.resolver.SolvePartialGrid",
        return_value=domain_spy,
    )

    # When
    result = boundary_resolver_integration.solve(grid)

    # Then
    assert result.code == "INVALID_SIZE"
    domain_spy.execute.assert_not_called()


@pytest.mark.integration
@pytest.mark.p2
def test_unsolvable_grid_returns_domain_unsolvable_it06(
    boundary_resolver_integration,
) -> None:
    """IT-06 ??unsolvable fixture maps to DOMAIN_UNSOLVABLE / EC-5."""
    # AC-US-05-10
    # Given
    grid = GRID_UNSOLVABLE

    # When
    result = boundary_resolver_integration.solve(grid)

    # Then
    assert result.code == "DOMAIN_UNSOLVABLE"


@pytest.mark.integration
@pytest.mark.p2
def test_second_trial_puzzle_succeeds_it02(
    boundary_resolver_integration,
) -> None:
    """IT-02 ??puzzle requiring second placement trial returns valid int[6]."""
    # AC-US-05-04
    # Given
    grid = GRID_PUZZLE_SECOND_TRIAL

    # When
    result = boundary_resolver_integration.solve(grid)

    # Then
    assert hasattr(result, "result")
    assert len(result.result) == 6
