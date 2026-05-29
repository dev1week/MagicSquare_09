"""Try placing missing numbers on blank cells in two trial orders."""

from copy import deepcopy
from dataclasses import dataclass

from src.domain.exceptions import UnsolvableGrid
from src.domain.magic_square_judge import MagicSquareJudge


@dataclass(frozen=True, slots=True)
class PlacementContext:
    """Inputs for a two-blank placement attempt."""

    grid: list[list[int]]
    first_blank: tuple[int, int]
    second_blank: tuple[int, int]
    n_small: int
    n_large: int


@dataclass(frozen=True, slots=True)
class PlacementSolution:
    """Successful placement of the two missing numbers."""

    numbers: tuple[int, int]


class PlacementTrialSolver:
    """Place small/large on blanks; retry with reversed order on failure."""

    def __init__(self, judge: MagicSquareJudge | None = None) -> None:
        self._judge = judge if judge is not None else MagicSquareJudge()

    def solve(self, context: PlacementContext) -> PlacementSolution:
        """Return the first successful (first-blank, second-blank) number pair."""
        if self._trial(context, context.n_small, context.n_large):
            return PlacementSolution(numbers=(context.n_small, context.n_large))

        if self._trial(context, context.n_large, context.n_small):
            return PlacementSolution(numbers=(context.n_large, context.n_small))

        raise UnsolvableGrid

    def _trial(
        self,
        context: PlacementContext,
        first_value: int,
        second_value: int,
    ) -> bool:
        candidate = deepcopy(context.grid)
        candidate[context.first_blank[0]][context.first_blank[1]] = first_value
        candidate[context.second_blank[0]][context.second_blank[1]] = second_value
        return self._judge.is_magic(candidate)
