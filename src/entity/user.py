"""User entity for core domain rules."""

from dataclasses import dataclass
import re


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass(slots=True)
class User:
    """Represent an application user entity.

    Args:
        user_id: Unique user identifier.
        username: Visible account name.
        email: User email address.
        is_active: Whether the account is active.
    """

    user_id: int
    username: str
    email: str
    is_active: bool = True

    def __post_init__(self) -> None:
        """Validate entity invariants after initialization."""
        if self.user_id <= 0:
            raise ValueError("user_id must be greater than zero")

        if not self.username.strip():
            raise ValueError("username must not be blank")

        if not EMAIL_PATTERN.match(self.email):
            raise ValueError("email must be a valid email address")

    def deactivate(self) -> None:
        """Deactivate the user account."""
        self.is_active = False
