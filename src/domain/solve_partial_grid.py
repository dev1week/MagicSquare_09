"""Orchestrate partial-grid solving across Domain components."""

from src.domain.empty_cell_locator import EmptyCellLocator
from src.domain.magic_square_judge import MagicSquareJudge
from src.domain.missing_number_resolver import MissingNumberResolver
from src.domain.placement_trial_solver import PlacementTrialSolver


class SolvePartialGrid:
    """Domain entry point: locate blanks, resolve missing values, and place them."""

    def __init__(self, judge: MagicSquareJudge | None = None) -> None:
        self._locator = EmptyCellLocator()
        self._resolver = MissingNumberResolver()
        self._judge = judge

    def execute(self, grid: list[list[int]]) -> list[int]:
        """Return ``[r1, c1, n1, r2, c2, n2]`` using 1-indexed coordinates."""
        judge = self._judge if self._judge is not None else MagicSquareJudge()
        placement_solver = PlacementTrialSolver(judge=judge)

        first_blank, second_blank = self._locator.locate(grid)
        n_small, n_large = self._resolver.resolve(grid)

        solution = placement_solver.solve(
            grid,
            first_blank,
            second_blank,
            n_small,
            n_large,
        )
        first_number, second_number = solution.numbers

        return [
            first_blank[0] + 1,
            first_blank[1] + 1,
            first_number,
            second_blank[0] + 1,
            second_blank[1] + 1,
            second_number,
        ]
