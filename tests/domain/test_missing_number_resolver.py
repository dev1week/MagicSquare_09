"""MissingNumberResolver RED tests ??DT-02, US-03."""

import pytest

from src.domain.missing_number_resolver import MissingNumberResolver
from tests.fixtures.grids import VALID_GRID_TWO_BLANKS


@pytest.fixture
def resolver() -> MissingNumberResolver:
    """MissingNumberResolver SUT."""
    return MissingNumberResolver()


@pytest.mark.domain
@pytest.mark.p0
def test_blanks_15_16_returns_fifteen_and_sixteen_ascending(
    resolver: MissingNumberResolver,
) -> None:
    """DT-02 ??missing 15 and 16 returned in ascending order."""
    # AC-US-03-02
    # Given
    grid = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 0, 0],
    ]

    # When
    small, large = resolver.resolve(grid)

    # Then
    assert small == 15
    assert large == 16
    assert small < large


@pytest.mark.domain
@pytest.mark.p0
def test_blanks_3_and_7_returns_three_and_seven_ascending(
    resolver: MissingNumberResolver,
) -> None:
    """DT-02 ??missing 3 and 7 returned in ascending order."""
    # AC-US-03-02
    # Given
    grid = [
        [0, 2, 4, 5],
        [6, 8, 9, 10],
        [11, 12, 13, 14],
        [15, 16, 0, 1],
    ]

    # When
    small, large = resolver.resolve(grid)

    # Then
    assert small == 3
    assert large == 7


@pytest.mark.domain
@pytest.mark.p0
def test_zero_is_excluded_from_missing_number_calculation(
    resolver: MissingNumberResolver,
) -> None:
    """DT-02 ??zero is never returned as a missing number."""
    # AC-US-03-01
    # Given
    grid = VALID_GRID_TWO_BLANKS

    # When
    small, large = resolver.resolve(grid)

    # Then
    assert small != 0
    assert large != 0


@pytest.mark.domain
@pytest.mark.p0
def test_resolve_returns_two_distinct_values_in_range_1_to_16(
    resolver: MissingNumberResolver,
) -> None:
    """DT-02 ??missing numbers are distinct and within 1..16."""
    # AC-US-03-04
    # Given
    grid = VALID_GRID_TWO_BLANKS

    # When
    small, large = resolver.resolve(grid)

    # Then
    assert 1 <= small <= 16
    assert 1 <= large <= 16
    assert small != large


@pytest.mark.domain
@pytest.mark.p0
def test_missing_15_16_from_partial_grid(
    resolver: MissingNumberResolver,
) -> None:
    """MN-01 ??blanks for 15 and 16 yield [15, 16]."""
    # AC-US-03-02
    # Given
    from tests.fixtures.grids import GRID_MISSING_15_16

    grid = GRID_MISSING_15_16

    # When
    small, large = resolver.resolve(grid)

    # Then
    assert (small, large) == (15, 16)


@pytest.mark.domain
@pytest.mark.p0
def test_missing_3_7_from_partial_grid(
    resolver: MissingNumberResolver,
) -> None:
    """MN-02 ??blanks for 3 and 7 yield [3, 7]."""
    # AC-US-03-02
    # Given
    from tests.fixtures.grids import GRID_MISSING_3_7

    grid = GRID_MISSING_3_7

    # When
    small, large = resolver.resolve(grid)

    # Then
    assert (small, large) == (3, 7)


@pytest.mark.domain
@pytest.mark.p0
def test_resolve_returns_exactly_two_missing_numbers(
    resolver: MissingNumberResolver,
) -> None:
    """AC-US-03-02 ??exactly two missing numbers are returned."""
    # AC-US-03-02
    # Given
    grid = VALID_GRID_TWO_BLANKS

    # When
    missing = resolver.resolve(grid)

    # Then
    assert len(missing) == 2


@pytest.mark.domain
@pytest.mark.p0
def test_wrong_missing_count_raises_grid_not_complete(
    resolver: MissingNumberResolver,
) -> None:
    """Domain guard — exactly two numbers must be missing."""
    from src.domain.exceptions import GridNotComplete
    from tests.fixtures.grids import GRID_BLANK_0

    with pytest.raises(GridNotComplete, match="Expected 2 missing numbers"):
        resolver.resolve(GRID_BLANK_0)
