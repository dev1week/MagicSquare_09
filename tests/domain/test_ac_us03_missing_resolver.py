"""AC-US-03-03/05 — MissingNumberResolver contract RED tests."""

import pytest

from src.domain.missing_number_resolver import MissingNumberResolver
from tests.fixtures.grids import GRID_MISSING_15_16, VALID_GRID_TWO_BLANKS


@pytest.fixture
def resolver() -> MissingNumberResolver:
    """MissingNumberResolver SUT."""
    return MissingNumberResolver()


@pytest.mark.domain
@pytest.mark.p0
def test_resolve_returns_strictly_ascending_pair(
    resolver: MissingNumberResolver,
) -> None:
    """AC-US-03-03 — [small, large] with small < large always."""
    # AC-US-03-03
    # Given
    grids = [VALID_GRID_TWO_BLANKS, GRID_MISSING_15_16]

    # When / Then
    for grid in grids:
        small, large = resolver.resolve(grid)
        assert small < large


@pytest.mark.domain
@pytest.mark.p0
def test_resolver_has_no_input_validation_method(
    resolver: MissingNumberResolver,
) -> None:
    """AC-US-03-05 — MissingNumberResolver does not validate Boundary IC."""
    # AC-US-03-05
    # Given / Then
    assert hasattr(resolver, "resolve")
    assert not hasattr(resolver, "validate")


@pytest.mark.domain
@pytest.mark.p0
def test_out_of_range_present_values_still_return_two_missing(
    resolver: MissingNumberResolver,
) -> None:
    """AC-US-03-05 — invalid cell values do not trigger Boundary error codes."""
    # AC-US-03-05
    # Given
    grid = [
        [17, 2, 3, 4],
        [5, 6, 0, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 0],
    ]

    # When
    small, large = resolver.resolve(grid)

    # Then
    assert len((small, large)) == 2
    assert small < large
