"""Transaction domain entity."""

from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from .entity import Entity
from ..value_objects.account_id import AccountId
from ..value_objects.category_id import CategoryId
from ..value_objects.money import Money
from ..value_objects.transaction_id import TransactionId
from ..events.transaction_events import TransactionCategorizedEvent

if TYPE_CHECKING:
    from .category import Category


@dataclass
class Transaction(Entity):
    """Domain entity representing a financial transaction."""
    id: TransactionId
    account_id: AccountId
    date: datetime
    amount: Money
    description: str
    merchant: Optional[str]
    category: Optional['Category']  # Forward reference to avoid circular import
    tags: List[str]
    created_at: datetime
    updated_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        """Validate the transaction."""
        if not self.description or not self.description.strip():
            raise ValueError("Transaction description cannot be empty")
        if self.created_at is None:
            self.created_at = datetime.now()

    def is_income(self) -> bool:
        """Check if this is an income transaction."""
        return self.amount.is_positive()

    def is_expense(self) -> bool:
        """Check if this is an expense transaction."""
        return self.amount.is_negative()

    def is_recent(self, days: int = 30) -> bool:
        """Check if the transaction is recent."""
        return (datetime.now() - self.date).days <= days

    def categorize(self, category: 'Category') -> None:
        """Categorize the transaction."""
        if not category.is_active:
            raise ValueError("Cannot assign inactive category")
        self.category = category
        self.updated_at = datetime.now()
        self.add_domain_event(TransactionCategorizedEvent(
            transaction_id=self.id,
            category_id=category.id,
            occurred_at=datetime.now(),
            event_data={}
        ))

    def add_tag(self, tag: str) -> None:
        """Add a tag to the transaction."""
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.now()

    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the transaction."""
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.now()

    def update_description(self, description: str) -> None:
        """Update the transaction description."""
        if not description or not description.strip():
            raise ValueError("Transaction description cannot be empty")
        self.description = description
        self.updated_at = datetime.now()

    def update_merchant(self, merchant: Optional[str]) -> None:
        """Update the transaction merchant."""
        self.merchant = merchant
        self.updated_at = datetime.now()
