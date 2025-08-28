"""Account type enum."""

from enum import Enum


class AccountType(Enum):
    """Types of bank accounts."""
    CHECKING = "checking"
    SAVINGS = "savings"
    CREDIT_CARD = "credit_card"
    INVESTMENT = "investment"
    LOAN = "loan"
    MORTGAGE = "mortgage"
