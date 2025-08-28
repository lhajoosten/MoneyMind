"""Category ID value object."""

from dataclasses import dataclass
from typing import Union
from uuid import UUID, uuid4


@dataclass(frozen=True)
class CategoryId:
    """Value object for category identifiers."""
    value: UUID

    @staticmethod
    def new() -> 'CategoryId':
        """Create a new CategoryId with a random UUID."""
        return CategoryId(uuid4())

    @staticmethod
    def from_string(value: str) -> 'CategoryId':
        """Create CategoryId from string representation."""
        return CategoryId(UUID(value))

    def __str__(self) -> str:
        """String representation."""
        return str(self.value)
