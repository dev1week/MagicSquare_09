"""Domain-layer pytest fixtures."""

import pytest


@pytest.fixture
def magic_square_judge():
    """MagicSquareJudge SUT ??real instance (no Boundary mock)."""
    from src.domain.magic_square_judge import MagicSquareJudge

    return MagicSquareJudge()
