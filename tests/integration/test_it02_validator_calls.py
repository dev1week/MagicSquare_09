"""IT-02 — second-trial puzzle invokes validator twice end-to-end."""

import pytest

from tests.fixtures.grids import GRID_PUZZLE_SECOND_TRIAL


@pytest.mark.integration
@pytest.mark.p2
def test_second_trial_puzzle_invokes_validator_twice_it02(
    boundary_resolver_integration,
    mocker,
) -> None:
    """IT-02 — 1st fail / 2nd success path calls MagicSquareJudge.is_magic twice."""
    # AC-US-05-05
    # Given
    from src.domain.magic_square_judge import MagicSquareJudge

    judge = MagicSquareJudge()
    spy = mocker.spy(judge, "is_magic")
    mocker.patch(
        "src.domain.solve_partial_grid.MagicSquareJudge",
        return_value=judge,
    )
    grid = GRID_PUZZLE_SECOND_TRIAL

    # When
    result = boundary_resolver_integration.solve(grid)

    # Then
    assert hasattr(result, "result")
    assert spy.call_count == 2
