"""Create transaction command."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from ...domain.value_objects.account_id import AccountId
from ...domain.value_objects.category_id import CategoryId
from ...domain.value_objects.money import Money


@dataclass
class CreateTransactionCommand:
    """Command to create a new transaction."""
    account_id: AccountId
    date: datetime
    amount: Money
    description: str
    merchant: Optional[str] = None
    category_id: Optional[CategoryId] = None
    tags: Optional[list[str]] = None
