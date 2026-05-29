"""Golden Master regression — lock Green solver outputs (RG-REFACTOR / RG-US-05)."""

import pytest

from src.boundary.resolver import BoundaryError, BoundaryResolver, BoundarySuccess
from src.boundary.response_formatter import ResponseFormatter
from src.domain.exceptions import UnsolvableGrid
from src.domain.solve_partial_grid import SolvePartialGrid
from tests.fixtures.error_catalog import ERROR_CATALOG
from tests.fixtures.golden_master.solver_outputs import (
    GOLDEN_MASTER_GRIDS,
    GOLDEN_MASTER_SOLVER_OUTPUTS,
)


@pytest.fixture
def solver() -> SolvePartialGrid:
    """Domain solver SUT."""
    return SolvePartialGrid()


@pytest.fixture
def resolver() -> BoundaryResolver:
    """Boundary resolver SUT."""
    return BoundaryResolver()


def _assert_oc_contract(grid: list[list[int]], result: list[int]) -> None:
    """Verify OC-1~OC-6 structural contract on a success vector."""
    # OC-1 length 6
    assert len(result) == 6
    r1, c1, n1, r2, c2, n2 = result
    # OC-2 integer components
    assert all(isinstance(value, int) for value in result)
    # OC-3 1-index coordinates
    assert 1 <= r1 <= 4 and 1 <= c1 <= 4
    assert 1 <= r2 <= 4 and 1 <= c2 <= 4
    # OC-4~5 numbers and blank alignment
    assert 1 <= n1 <= 16 and 1 <= n2 <= 16 and n1 != n2
    assert grid[r1 - 1][c1 - 1] == 0
    assert grid[r2 - 1][c2 - 1] == 0


@pytest.mark.regression
def test_golden_master_grid_keys_match_outputs() -> None:
    """Golden Master — grid registry keys stay aligned with baseline records."""
    assert set(GOLDEN_MASTER_GRIDS) == set(GOLDEN_MASTER_SOLVER_OUTPUTS)


@pytest.mark.regression
@pytest.mark.parametrize("fixture_name", list(GOLDEN_MASTER_SOLVER_OUTPUTS))
def test_golden_master_domain_matches_runtime(
    solver: SolvePartialGrid,
    fixture_name: str,
) -> None:
    """Golden Master — Domain execute output matches captured baseline."""
    golden = GOLDEN_MASTER_SOLVER_OUTPUTS[fixture_name]
    grid = GOLDEN_MASTER_GRIDS[fixture_name]

    if "domain_result" in golden:
        result = solver.execute(grid)
        assert result == golden["domain_result"]
        _assert_oc_contract(grid, result)
        return

    with pytest.raises(UnsolvableGrid):
        solver.execute(grid)
    assert golden["domain_exception"] == "UnsolvableGrid"


@pytest.mark.regression
@pytest.mark.parametrize("fixture_name", list(GOLDEN_MASTER_SOLVER_OUTPUTS))
def test_golden_master_boundary_matches_runtime(
    resolver: BoundaryResolver,
    fixture_name: str,
) -> None:
    """Golden Master — Boundary resolve output matches captured baseline."""
    golden = GOLDEN_MASTER_SOLVER_OUTPUTS[fixture_name]
    grid = GOLDEN_MASTER_GRIDS[fixture_name]
    boundary_golden = golden["boundary"]

    result = resolver.solve(grid)

    if boundary_golden["kind"] == "success":
        assert isinstance(result, BoundarySuccess)
        assert result.result == boundary_golden["result"]
        return

    assert isinstance(result, BoundaryError)
    assert result.code == boundary_golden["code"]
    assert result.message == boundary_golden["message"]
    assert result.message == ERROR_CATALOG[boundary_golden["code"]]


@pytest.mark.regression
@pytest.mark.parametrize(
    "fixture_name",
    [
        name
        for name, record in GOLDEN_MASTER_SOLVER_OUTPUTS.items()
        if "formatted" in record
    ],
)
def test_golden_master_formatted_output_matches_runtime(
    solver: SolvePartialGrid,
    fixture_name: str,
) -> None:
    """Golden Master — ResponseFormatter text matches captured baseline."""
    golden = GOLDEN_MASTER_SOLVER_OUTPUTS[fixture_name]
    grid = GOLDEN_MASTER_GRIDS[fixture_name]

    domain_result = solver.execute(grid)
    formatted = ResponseFormatter.format_success(domain_result)

    assert formatted == golden["formatted"]
    assert formatted.startswith("OK [")
    assert formatted.endswith("]")
    assert " " not in formatted.removeprefix("OK ")
