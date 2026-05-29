"""Try placing missing numbers on blank cells in two trial orders."""

from copy import deepcopy
from dataclasses import dataclass

from src.domain.exceptions import UnsolvableGrid
from src.domain.magic_square_judge import MagicSquareJudge


@dataclass(frozen=True, slots=True)
class PlacementSolution:
    """Successful placement of the two missing numbers."""

    numbers: tuple[int, int]


class PlacementTrialSolver:
    """Place small/large on blanks; retry with reversed order on failure."""

    def __init__(self, judge: MagicSquareJudge | None = None) -> None:
        self._judge = judge if judge is not None else MagicSquareJudge()

    def solve(
        self,
        grid: list[list[int]],
        first_blank: tuple[int, int],
        second_blank: tuple[int, int],
        n_small: int,
        n_large: int,
    ) -> PlacementSolution:
        """Return the first successful (first-blank, second-blank) number pair."""
        first_trial = self._trial(
            grid,
            first_blank,
            second_blank,
            n_small,
            n_large,
        )
        if first_trial is not None:
            return PlacementSolution(numbers=(n_small, n_large))

        second_trial = self._trial(
            grid,
            first_blank,
            second_blank,
            n_large,
            n_small,
        )
        if second_trial is not None:
            return PlacementSolution(numbers=(n_large, n_small))

        raise UnsolvableGrid

    def _trial(
        self,
        grid: list[list[int]],
        first_blank: tuple[int, int],
        second_blank: tuple[int, int],
        first_value: int,
        second_value: int,
    ) -> list[list[int]] | None:
        candidate = deepcopy(grid)
        candidate[first_blank[0]][first_blank[1]] = first_value
        candidate[second_blank[0]][second_blank[1]] = second_value

        if self._judge.is_magic(candidate):
            return candidate

        return None
