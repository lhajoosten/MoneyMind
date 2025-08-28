"""Account ID value object."""

from dataclasses import dataclass
from typing import Union
from uuid import UUID, uuid4


@dataclass(frozen=True)
class AccountId:
    """Value object for account identifiers."""
    value: UUID

    @staticmethod
    def new() -> 'AccountId':
        """Create a new AccountId with a random UUID."""
        return AccountId(uuid4())

    @staticmethod
    def from_string(value: str) -> 'AccountId':
        """Create AccountId from string representation."""
        return AccountId(UUID(value))

    def __str__(self) -> str:
        """String representation."""
        return str(self.value)
