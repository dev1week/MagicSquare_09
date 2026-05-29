"""AC-US-04-04/05/08 — diagonal sums and no magic literal in source."""

from pathlib import Path

import pytest

from src.domain.constants import MAGIC_CONSTANT
from src.domain.magic_square_judge import MagicSquareJudge
from tests.fixtures.grids import KNOWN_MAGIC_SQUARE


@pytest.fixture
def judge() -> MagicSquareJudge:
    """MagicSquareJudge SUT."""
    return MagicSquareJudge()


@pytest.mark.domain
@pytest.mark.p0
def test_main_diagonal_sum_equals_magic_constant_when_true(
    judge: MagicSquareJudge,
) -> None:
    """AC-US-04-04 — main diagonal sum equals MAGIC_CONSTANT when magic."""
    # AC-US-04-04
    # Given
    grid = KNOWN_MAGIC_SQUARE
    main_diagonal_sum = sum(grid[index][index] for index in range(4))

    # When
    result = judge.is_magic(grid)

    # Then
    assert result is True
    assert main_diagonal_sum == MAGIC_CONSTANT


@pytest.mark.domain
@pytest.mark.p0
def test_anti_diagonal_sum_equals_magic_constant_when_true(
    judge: MagicSquareJudge,
) -> None:
    """AC-US-04-05 — anti diagonal sum equals MAGIC_CONSTANT when magic."""
    # AC-US-04-05
    # Given
    grid = KNOWN_MAGIC_SQUARE
    anti_diagonal_sum = sum(grid[row][3 - row] for row in range(4))

    # When
    result = judge.is_magic(grid)

    # Then
    assert result is True
    assert anti_diagonal_sum == MAGIC_CONSTANT


@pytest.mark.domain
@pytest.mark.p0
def test_judge_source_avoids_bare_literal_34() -> None:
    """AC-US-04-08 — judge module must not use bare literal 34."""
    # AC-US-04-08
    # Given
    judge_path = Path("src/domain/magic_square_judge.py")

    # When
    source = judge_path.read_text(encoding="utf-8")

    # Then
    assert "MAGIC_CONSTANT" in source
    assert "== 34" not in source
    assert "!= 34" not in source
