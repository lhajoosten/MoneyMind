"""Budget domain entity."""

from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

from .entity import Entity
from ..value_objects.budget_id import BudgetId
from ..value_objects.budget_period import BudgetPeriod
from ..value_objects.money import Money

if TYPE_CHECKING:
    from .category import Category


@dataclass
class Budget(Entity):
    """Domain entity representing a spending budget."""
    id: BudgetId
    category: 'Category'
    limit: Money
    period: BudgetPeriod
    start_date: datetime
    end_date: datetime

    def __post_init__(self) -> None:
        """Validate the budget."""
        if self.start_date >= self.end_date:
            raise ValueError("Start date must be before end date")
        if not self.limit.is_positive():
            raise ValueError("Budget limit must be positive")

    def remaining_amount(self, spent: Money) -> Money:
        """Calculate remaining budget amount."""
        return Money(self.limit.value - spent.value, self.limit.currency)

    def is_exceeded(self, spent: Money) -> bool:
        """Check if budget is exceeded."""
        return spent.value > self.limit.value

    def percentage_used(self, spent: Money) -> float:
        """Calculate percentage of budget used."""
        if self.limit.value == 0:
            return 100.0
        return min(spent.value / self.limit.value * 100, 100.0)

    def is_active_for_date(self, date: datetime) -> bool:
        """Check if budget is active for a given date."""
        return self.start_date <= date <= self.end_date

    def update_limit(self, limit: Money) -> None:
        """Update the budget limit."""
        if not limit.is_positive():
            raise ValueError("Budget limit must be positive")
        self.limit = limit
