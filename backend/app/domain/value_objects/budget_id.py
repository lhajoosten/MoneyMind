"""Budget ID value object."""

from dataclasses import dataclass
from typing import Union
from uuid import UUID, uuid4


@dataclass(frozen=True)
class BudgetId:
    """Value object for budget identifiers."""
    value: UUID

    @staticmethod
    def new() -> 'BudgetId':
        """Create a new BudgetId with a random UUID."""
        return BudgetId(uuid4())

    @staticmethod
    def from_string(value: str) -> 'BudgetId':
        """Create BudgetId from string representation."""
        return BudgetId(UUID(value))

    def __str__(self) -> str:
        """String representation."""
        return str(self.value)
