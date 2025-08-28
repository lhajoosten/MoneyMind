"""Budget period enum."""

from enum import Enum


class BudgetPeriod(Enum):
    """Budget period types."""
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"
