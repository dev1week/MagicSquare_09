"""Error Contract RED tests ??BT-08, pydantic schema lock."""

import pytest
from pydantic import ValidationError

from src.boundary.schemas import ErrorResponse


from tests.fixtures.error_catalog import ERROR_CATALOG


@pytest.mark.boundary
@pytest.mark.p2
@pytest.mark.parametrize(
    ("code", "message"),
    [(code, message) for code, message in ERROR_CATALOG.items()],
)
def test_error_response_accepts_catalog_entries(code: str, message: str) -> None:
    """BT-08 ??catalog code/message pairs satisfy ErrorResponse schema."""
    # AC-US-01-07
    # Given
    payload = {"code": code, "message": message}

    # When
    response = ErrorResponse.model_validate(payload)

    # Then
    assert response.code == code
    assert response.message == message


@pytest.mark.boundary
@pytest.mark.p2
def test_error_response_rejects_missing_code() -> None:
    """BT-08 ??schema rejects incomplete error payloads."""
    # AC-US-01-07
    # Given
    payload = {"message": "Grid must be 4x4."}

    # When / Then
    with pytest.raises(ValidationError):
        ErrorResponse.model_validate(payload)


@pytest.mark.boundary
@pytest.mark.p2
def test_error_response_optional_details() -> None:
    """BT-08 ??optional details field is supported."""
    # AC-US-01-07
    # Given
    payload = {
        "code": "INVALID_SIZE",
        "message": "Grid must be 4x4.",
        "details": {"rows": 3, "cols": 4},
    }

    # When
    response = ErrorResponse.model_validate(payload)

    # Then
    assert response.details == {"rows": 3, "cols": 4}
