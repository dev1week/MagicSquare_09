"""AC-US-05-01~11 — SolvePartialGrid orchestration and strategy RED tests."""

from pathlib import Path

import pytest

from src.domain.exceptions import UnsolvableGrid
from src.domain.solve_partial_grid import SolvePartialGrid
from tests.fixtures.grids import (
    GRID_PUZZLE_SECOND_TRIAL,
    GRID_UNSOLVABLE,
    VALID_GRID_TWO_BLANKS,
)


@pytest.fixture
def use_case() -> SolvePartialGrid:
    """SolvePartialGrid SUT."""
    return SolvePartialGrid()


@pytest.mark.domain
@pytest.mark.p1
def test_execute_invokes_blankfinder_and_missingfinder(
    use_case: SolvePartialGrid,
    mocker,
) -> None:
    """AC-US-05-01 — execute wires EmptyCellLocator and MissingNumberResolver."""
    # AC-US-05-01
    # Given
    from src.domain.empty_cell_locator import EmptyCellLocator
    from src.domain.missing_number_resolver import MissingNumberResolver

    locate_spy = mocker.spy(EmptyCellLocator, "locate")
    resolve_spy = mocker.spy(MissingNumberResolver, "resolve")
    grid = VALID_GRID_TWO_BLANKS

    # When
    use_case.execute(grid)

    # Then
    locate_spy.assert_called_once()
    resolve_spy.assert_called_once()


@pytest.mark.domain
@pytest.mark.p1
def test_success_numbers_are_from_missing_set(
    use_case: SolvePartialGrid,
) -> None:
    """AC-US-05-09 — n1 and n2 belong to the missing-number pair."""
    # AC-US-05-09
    # Given
    from src.domain.missing_number_resolver import MissingNumberResolver

    grid = VALID_GRID_TWO_BLANKS
    resolver = MissingNumberResolver()
    n_small, n_large = resolver.resolve(grid)

    # When
    _, _, n1, _, _, n2 = use_case.execute(grid)

    # Then
    assert {n1, n2} == {n_small, n_large}
    assert n1 != n2


@pytest.mark.domain
@pytest.mark.p1
def test_first_trial_success_calls_validator_once_via_execute(
    mocker,
) -> None:
    """SV-01 / AC-US-05-03 — execute stops after first successful validator call."""
    # AC-US-05-03
    # Given
    from src.domain.magic_square_judge import MagicSquareJudge
    from src.domain.solve_partial_grid import SolvePartialGrid

    judge = MagicSquareJudge()
    spy = mocker.spy(judge, "is_magic")
    mocker.patch(
        "src.domain.solve_partial_grid.MagicSquareJudge",
        return_value=judge,
    )
    use_case = SolvePartialGrid()
    grid = VALID_GRID_TWO_BLANKS

    # When
    use_case.execute(grid)

    # Then
    assert spy.call_count == 1


@pytest.mark.domain
@pytest.mark.p1
def test_second_trial_success_calls_validator_twice_via_execute(
    mocker,
) -> None:
    """SV-02 / AC-US-05-05 — second trial puzzle triggers two validator calls."""
    # AC-US-05-05
    # Given
    from src.domain.magic_square_judge import MagicSquareJudge

    judge = MagicSquareJudge()
    spy = mocker.spy(judge, "is_magic")
    use_case = SolvePartialGrid(judge=judge)
    grid = GRID_PUZZLE_SECOND_TRIAL

    # When
    use_case.execute(grid)

    # Then
    assert spy.call_count == 2


@pytest.mark.domain
@pytest.mark.p1
def test_both_trials_fail_raises_unsolvable_without_int6(
    use_case: SolvePartialGrid,
) -> None:
    """SV-03 / EC5-01 — unsolvable grid raises, no success vector returned."""
    # AC-US-05-10
    # Given
    grid = GRID_UNSOLVABLE

    # When / Then
    with pytest.raises(UnsolvableGrid):
        use_case.execute(grid)


@pytest.mark.domain
@pytest.mark.p1
def test_solver_modules_contain_no_hardcoded_solution_vector() -> None:
    """AC-US-05-11 / SV-05 — domain solver modules must not embed fixed answers."""
    # AC-US-05-11
    # Given
    domain_dir = Path("src/domain")
    hardcoded = "[2, 3, 5, 4, 1, 11]"

    # When / Then
    for source_path in domain_dir.glob("*.py"):
        source = source_path.read_text(encoding="utf-8")
        assert hardcoded not in source
