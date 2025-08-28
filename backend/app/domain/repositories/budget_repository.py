"""Budget repository interface."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional, Protocol

from app.domain.entities.budget import Budget
from app.domain.value_objects.budget_id import BudgetId
from app.domain.value_objects.user_id import UserId


class IBudgetRepository(Protocol):
    """Repository interface for Budget entities."""

    @abstractmethod
    async def get_by_id(self, budget_id: BudgetId) -> Optional[Budget]:
        """Get budget by ID."""
        ...

    @abstractmethod
    async def get_by_user(self, user_id: UserId) -> List[Budget]:
        """Get all budgets for a user."""
        ...

    @abstractmethod
    async def get_active_for_date(self, user_id: UserId, date: datetime) -> List[Budget]:
        """Get active budgets for a user on a specific date."""
        ...

    @abstractmethod
    async def save(self, budget: Budget) -> None:
        """Save a budget."""
        ...

    @abstractmethod
    async def delete(self, budget_id: BudgetId) -> None:
        """Delete a budget."""
        ...
