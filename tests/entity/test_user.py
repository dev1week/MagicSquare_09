"""Tests for the User entity."""

import pytest

from src.entity.user import User


def test_user_creation_with_valid_values() -> None:
    """Create a user with valid values."""
    # Arrange
    user_id = 1
    username = "alice"
    email = "alice@example.com"

    # Act
    user = User(user_id=user_id, username=username, email=email)

    # Assert
    assert user.user_id == 1
    assert user.username == "alice"
    assert user.email == "alice@example.com"
    assert user.is_active is True


def test_user_creation_fails_when_username_is_blank() -> None:
    """Reject a blank username."""
    # Arrange
    user_id = 1
    username = "   "
    email = "alice@example.com"

    # Act / Assert
    with pytest.raises(ValueError, match="username must not be blank"):
        User(user_id=user_id, username=username, email=email)


def test_user_creation_fails_when_email_is_invalid() -> None:
    """Reject an invalid email format."""
    # Arrange
    user_id = 1
    username = "alice"
    email = "invalid-email"

    # Act / Assert
    with pytest.raises(ValueError, match="email must be a valid email address"):
        User(user_id=user_id, username=username, email=email)


def test_user_can_be_deactivated() -> None:
    """Deactivate an active user."""
    # Arrange
    user = User(user_id=1, username="alice", email="alice@example.com")

    # Act
    user.deactivate()

    # Assert
    assert user.is_active is False
