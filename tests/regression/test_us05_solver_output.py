"""Regression RED suite ??RG-US-05 (US-05 EC-5, OC-1~OC-6)."""

import pytest

from src.domain.exceptions import UnsolvableGrid
from src.domain.solve_partial_grid import SolvePartialGrid
from tests.fixtures.grids import GRID_UNSOLVABLE, VALID_GRID_TWO_BLANKS


@pytest.fixture
def use_case() -> SolvePartialGrid:
    """SolvePartialGrid SUT."""
    return SolvePartialGrid()


@pytest.mark.regression
@pytest.mark.domain
def test_us05_success_output_matches_oc_format(use_case: SolvePartialGrid) -> None:
    """RG-US-05 ??success path satisfies OC-1~OC-6."""
    # AC-US-05-06
    # Given
    grid = VALID_GRID_TWO_BLANKS

    # When
    result = use_case.execute(grid)

    # Then ??OC-1 length 6
    assert len(result) == 6
    r1, c1, n1, r2, c2, n2 = result
    # OC-2 order [r1,c1,n1,r2,c2,n2]
    assert isinstance(r1, int)
    # OC-3 1-index coordinates
    assert 1 <= r1 <= 4 and 1 <= c1 <= 4
    assert 1 <= r2 <= 4 and 1 <= c2 <= 4
    # OC-4~5 numbers and blank alignment
    assert 1 <= n1 <= 16 and 1 <= n2 <= 16 and n1 != n2
    assert grid[r1 - 1][c1 - 1] == 0
    assert grid[r2 - 1][c2 - 1] == 0


@pytest.mark.regression
@pytest.mark.domain
def test_us05_unsolvable_raises_ec5_no_success_vector(
    use_case: SolvePartialGrid,
) -> None:
    """RG-US-05 ??EC-5: no int[6] on unsolvable grid."""
    # AC-US-05-10
    # Given
    grid = GRID_UNSOLVABLE

    # When / Then
    with pytest.raises(UnsolvableGrid):
        use_case.execute(grid)
