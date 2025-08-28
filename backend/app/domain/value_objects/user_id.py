"""User ID value object."""

from dataclasses import dataclass
from typing import Union
from uuid import UUID, uuid4


@dataclass(frozen=True)
class UserId:
    """Value object for user identifiers."""
    value: UUID

    @staticmethod
    def new() -> 'UserId':
        """Create a new UserId with a random UUID."""
        return UserId(uuid4())

    @staticmethod
    def from_string(value: str) -> 'UserId':
        """Create UserId from string representation."""
        return UserId(UUID(value))

    def __str__(self) -> str:
        """String representation."""
        return str(self.value)
