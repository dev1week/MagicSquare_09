"""Tests for OC-1~6 solution vector assembly."""

import pytest

from src.domain.constants import SOLUTION_VECTOR_LENGTH
from src.domain.solution_vector import to_solution_vector


@pytest.mark.domain
def test_to_solution_vector_uses_one_indexed_coordinates() -> None:
    result = to_solution_vector((1, 2), (3, 0), 7, 16)

    assert result == [2, 3, 7, 4, 1, 16]
    assert len(result) == SOLUTION_VECTOR_LENGTH
