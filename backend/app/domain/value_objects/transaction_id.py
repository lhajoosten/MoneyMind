"""Transaction ID value object."""

from dataclasses import dataclass
from typing import Union
from uuid import UUID, uuid4


@dataclass(frozen=True)
class TransactionId:
    """Value object for transaction identifiers."""
    value: UUID

    @staticmethod
    def new() -> 'TransactionId':
        """Create a new TransactionId with a random UUID."""
        return TransactionId(uuid4())

    @staticmethod
    def from_string(value: str) -> 'TransactionId':
        """Create TransactionId from string representation."""
        return TransactionId(UUID(value))

    def __str__(self) -> str:
        """String representation."""
        return str(self.value)
