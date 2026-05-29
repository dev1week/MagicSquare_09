"""Pydantic schemas for Boundary error contracts."""

from typing import Any

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Standard error payload returned by Boundary validation."""

    code: str
    message: str
    details: dict[str, Any] | None = None
