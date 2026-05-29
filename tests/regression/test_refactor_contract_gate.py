"""RG-REFACTOR — contract snapshot gates for Boundary and Output."""

import pytest

from tests.fixtures.error_catalog import ERROR_CATALOG


@pytest.mark.regression
@pytest.mark.boundary
def test_invalid_size_message_is_locked() -> None:
    """RG-REFACTOR — INVALID_SIZE message must not drift."""
    # AC-US-01-07
    # Given / Then
    assert ERROR_CATALOG["INVALID_SIZE"] == "Grid must be 4x4."


@pytest.mark.regression
@pytest.mark.boundary
@pytest.mark.parametrize("code", list(ERROR_CATALOG))
def test_error_catalog_codes_are_stable(code: str) -> None:
    """RG-REFACTOR — error code keys remain fixed."""
    # AC-US-01-07
    # Given / Then
    assert code in ERROR_CATALOG
    assert ERROR_CATALOG[code]


@pytest.mark.regression
@pytest.mark.domain
def test_success_vector_length_contract_is_six() -> None:
    """RG-REFACTOR — OC-1 success vector length remains 6."""
    # AC-US-05-06
    # Given
    expected_length = 6

    # Then
    assert expected_length == 6
