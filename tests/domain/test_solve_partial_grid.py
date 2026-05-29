"""SolvePartialGrid RED tests ??DT-05, US-05."""

import pytest

from src.domain.exceptions import UnsolvableGrid
from src.domain.solve_partial_grid import SolvePartialGrid
from tests.fixtures.grids import VALID_GRID_TWO_BLANKS


@pytest.fixture
def use_case() -> SolvePartialGrid:
    """SolvePartialGrid SUT."""
    return SolvePartialGrid()


@pytest.mark.domain
@pytest.mark.p1
def test_valid_grid_returns_six_element_one_index_vector(
    use_case: SolvePartialGrid,
) -> None:
    """DT-05 ??success returns int[6] in [r1,c1,n1,r2,c2,n2] 1-index form."""
    # AC-US-05-06
    # Given
    grid = VALID_GRID_TWO_BLANKS

    # When
    result = use_case.execute(grid)

    # Then
    assert len(result) == 6
    r1, c1, n1, r2, c2, n2 = result
    assert 1 <= r1 <= 4
    assert 1 <= c1 <= 4
    assert 1 <= r2 <= 4
    assert 1 <= c2 <= 4
    assert 1 <= n1 <= 16
    assert 1 <= n2 <= 16
    assert n1 != n2


@pytest.mark.domain
@pytest.mark.p1
def test_output_coordinates_match_original_blank_positions(
    use_case: SolvePartialGrid,
) -> None:
    """DT-05 ??1-index output coordinates align with input zero cells."""
    # AC-US-05-08
    # Given
    grid = VALID_GRID_TWO_BLANKS

    # When
    r1, c1, _, r2, c2, _ = use_case.execute(grid)

    # Then
    assert grid[r1 - 1][c1 - 1] == 0
    assert grid[r2 - 1][c2 - 1] == 0


@pytest.mark.domain
@pytest.mark.p1
def test_unsolvable_grid_raises_without_success_vector(
    use_case: SolvePartialGrid,
) -> None:
    """DT-05 ??both combinations failing raises UnsolvableGrid, no int[6]."""
    # AC-US-05-10
    # Given
    grid = [
        [1, 2, 3, 4],
        [5, 6, 0, 8],
        [9, 10, 11, 12],
        [13, 14, 0, 16],
    ]

    # When / Then
    with pytest.raises(UnsolvableGrid):
        use_case.execute(grid)


@pytest.mark.domain
@pytest.mark.p1
def test_corner_blank_0_0_outputs_one_index_coordinates(
    use_case: SolvePartialGrid,
) -> None:
    """SV-04 ??blank at (0,0) maps to output r=1, c=1."""
    # AC-US-05-08
    # Given
    from tests.fixtures.grids import GRID_CORNER_BLANK_0_0

    grid = GRID_CORNER_BLANK_0_0

    # When
    r1, c1, _, _, _, _ = use_case.execute(grid)

    # Then
    assert (r1, c1) == (1, 1)


@pytest.mark.domain
@pytest.mark.p1
def test_success_vector_follows_r1_c1_n1_r2_c2_n2_order(
    use_case: SolvePartialGrid,
) -> None:
    """OC-2 ??result array order is [r1, c1, n1, r2, c2, n2]."""
    # AC-US-05-06
    # Given
    grid = VALID_GRID_TWO_BLANKS

    # When
    result = use_case.execute(grid)

    # Then
    assert len(result) == 6
    r1, c1, n1, r2, c2, n2 = result
    assert all(isinstance(value, int) for value in (r1, c1, n1, r2, c2, n2))


@pytest.mark.domain
@pytest.mark.p1
def test_different_valid_grids_produce_different_missing_numbers(
    use_case: SolvePartialGrid,
) -> None:
    """AC-US-05-11 ??no single hardcoded answer; outputs vary by input."""
    # AC-US-05-11
    # Given
    from tests.fixtures.grids import GRID_MISSING_15_16

    grid_a = VALID_GRID_TWO_BLANKS
    grid_b = GRID_MISSING_15_16

    # When
    _, _, n1_a, _, _, n2_a = use_case.execute(grid_a)
    _, _, n1_b, _, _, n2_b = use_case.execute(grid_b)

    # Then
    assert (n1_a, n2_a) != (n1_b, n2_b)
