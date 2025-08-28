"""Create budget command."""

from dataclasses import dataclass
from datetime import datetime

from ...domain.value_objects.category_id import CategoryId
from ...domain.value_objects.money import Money
from ...domain.value_objects.user_id import UserId
from ...domain.value_objects.budget_period import BudgetPeriod


@dataclass
class CreateBudgetCommand:
    """Command to create a new budget."""
    user_id: UserId
    category_id: CategoryId
    amount: Money
    period: BudgetPeriod
    start_date: datetime
