"""PlacementTrialSolver RED tests — DT-04, DM-E03, US-05."""

import pytest

from src.domain.exceptions import UnsolvableGrid
from src.domain.placement_trial_solver import PlacementContext, PlacementTrialSolver
from tests.fixtures.grids import GRID_PUZZLE_SECOND_TRIAL, GRID_UNSOLVABLE, VALID_GRID_TWO_BLANKS


def _context(
    grid: list[list[int]],
    first_blank: tuple[int, int],
    second_blank: tuple[int, int],
    n_small: int,
    n_large: int,
) -> PlacementContext:
    return PlacementContext(
        grid=grid,
        first_blank=first_blank,
        second_blank=second_blank,
        n_small=n_small,
        n_large=n_large,
    )


@pytest.fixture
def solver() -> PlacementTrialSolver:
    """PlacementTrialSolver SUT."""
    return PlacementTrialSolver()


@pytest.mark.domain
@pytest.mark.p1
def test_small_to_first_blank_large_to_second_succeeds_on_first_trial(
    solver: PlacementTrialSolver,
) -> None:
    """DT-04 — first trial places small on first blank, large on second."""
    context = _context(VALID_GRID_TWO_BLANKS, (1, 2), (3, 3), 7, 16)

    solution = solver.solve(context)

    assert solution.numbers == (7, 16)


@pytest.mark.domain
@pytest.mark.p1
def test_reversed_assignment_succeeds_when_first_trial_fails(
    solver: PlacementTrialSolver,
) -> None:
    """DT-04 — second trial swaps small and large when first fails."""
    context = _context(VALID_GRID_TWO_BLANKS, (1, 2), (3, 3), 16, 7)

    solution = solver.solve(context)

    assert solution.numbers == (7, 16)


@pytest.mark.domain
@pytest.mark.p1
def test_both_trials_fail_raises_unsolvable_grid(
    solver: PlacementTrialSolver,
) -> None:
    """DM-E03 — both placement orders failing raises UnsolvableGrid."""
    context = _context(GRID_UNSOLVABLE, (1, 2), (3, 3), 7, 15)

    with pytest.raises(UnsolvableGrid):
        solver.solve(context)


@pytest.mark.domain
@pytest.mark.p1
def test_first_trial_success_invokes_validator_once(
    mocker,
) -> None:
    """SV-01 — first successful trial calls MagicSquareValidator once."""
    from src.domain.magic_square_judge import MagicSquareJudge

    judge = MagicSquareJudge()
    spy = mocker.spy(judge, "is_magic")
    solver = PlacementTrialSolver(judge=judge)
    context = _context(VALID_GRID_TWO_BLANKS, (1, 2), (3, 3), 7, 16)

    solver.solve(context)

    assert spy.call_count == 1


@pytest.mark.domain
@pytest.mark.p1
def test_second_trial_success_invokes_validator_twice(
    mocker,
) -> None:
    """SV-02 — second trial success calls validator exactly twice."""
    from src.domain.magic_square_judge import MagicSquareJudge

    judge = MagicSquareJudge()
    spy = mocker.spy(judge, "is_magic")
    solver = PlacementTrialSolver(judge=judge)
    context = _context(GRID_PUZZLE_SECOND_TRIAL, (1, 2), (2, 0), 3, 7)

    solver.solve(context)

    assert spy.call_count == 2
