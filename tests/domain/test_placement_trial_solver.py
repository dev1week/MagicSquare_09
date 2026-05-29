"""PlacementTrialSolver RED tests ??DT-04, DM-E03, US-05."""

import pytest

from src.domain.exceptions import UnsolvableGrid
from src.domain.placement_trial_solver import PlacementTrialSolver
from tests.fixtures.grids import VALID_GRID_TWO_BLANKS


@pytest.fixture
def solver() -> PlacementTrialSolver:
    """PlacementTrialSolver SUT."""
    return PlacementTrialSolver()


@pytest.mark.domain
@pytest.mark.p1
def test_small_to_first_blank_large_to_second_succeeds_on_first_trial(
    solver: PlacementTrialSolver,
) -> None:
    """DT-04 ??first trial places small on first blank, large on second."""
    # AC-US-05-02
    # Given
    grid = VALID_GRID_TWO_BLANKS
    first_blank = (1, 2)
    second_blank = (3, 3)
    n_small = 7
    n_large = 16

    # When
    solution = solver.solve(grid, first_blank, second_blank, n_small, n_large)

    # Then
    assert solution.numbers == (n_small, n_large)


@pytest.mark.domain
@pytest.mark.p1
def test_reversed_assignment_succeeds_when_first_trial_fails(
    solver: PlacementTrialSolver,
) -> None:
    """DT-04 ??second trial swaps small and large when first fails."""
    # AC-US-05-04
    # Given
    grid = [
        [1, 2, 3, 4],
        [5, 6, 0, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 0],
    ]
    first_blank = (1, 2)
    second_blank = (3, 3)
    n_small = 16
    n_large = 7

    # When
    solution = solver.solve(grid, first_blank, second_blank, n_small, n_large)

    # Then
    assert solution.numbers == (n_large, n_small)


@pytest.mark.domain
@pytest.mark.p1
def test_both_trials_fail_raises_unsolvable_grid(
    solver: PlacementTrialSolver,
) -> None:
    """DM-E03 ??both placement orders failing raises UnsolvableGrid."""
    # AC-US-05-10
    # Given
    grid = [
        [1, 2, 3, 4],
        [5, 6, 0, 8],
        [9, 10, 11, 12],
        [13, 14, 0, 16],
    ]
    first_blank = (1, 2)
    second_blank = (3, 3)
    n_small = 7
    n_large = 15

    # When / Then
    with pytest.raises(UnsolvableGrid):
        solver.solve(grid, first_blank, second_blank, n_small, n_large)


@pytest.mark.domain
@pytest.mark.p1
def test_first_trial_success_invokes_validator_once(
    mocker,
) -> None:
    """SV-01 ??first successful trial calls MagicSquareValidator once."""
    # AC-US-05-03
    # Given
    from src.domain.magic_square_judge import MagicSquareJudge
    from src.domain.placement_trial_solver import PlacementTrialSolver

    judge = MagicSquareJudge()
    spy = mocker.spy(judge, "is_magic")
    solver = PlacementTrialSolver(judge=judge)
    grid = VALID_GRID_TWO_BLANKS
    first_blank = (1, 2)
    second_blank = (3, 3)
    n_small = 7
    n_large = 16

    # When
    solver.solve(grid, first_blank, second_blank, n_small, n_large)

    # Then
    assert spy.call_count == 1


@pytest.mark.domain
@pytest.mark.p1
def test_second_trial_success_invokes_validator_twice(
    mocker,
) -> None:
    """SV-02 ??second trial success calls validator exactly twice."""
    # AC-US-05-05
    # Given
    from src.domain.magic_square_judge import MagicSquareJudge
    from src.domain.placement_trial_solver import PlacementTrialSolver
    from tests.fixtures.grids import GRID_PUZZLE_SECOND_TRIAL

    judge = MagicSquareJudge()
    spy = mocker.spy(judge, "is_magic")
    solver = PlacementTrialSolver(judge=judge)
    grid = GRID_PUZZLE_SECOND_TRIAL
    first_blank = (1, 2)
    second_blank = (3, 3)
    n_small = 7
    n_large = 16

    # When
    solver.solve(grid, first_blank, second_blank, n_small, n_large)

    # Then
    assert spy.call_count == 2
