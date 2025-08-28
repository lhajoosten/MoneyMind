"""Transaction DTOs."""

from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from ...domain.value_objects.money import Money

if TYPE_CHECKING:
    from ...domain.entities.transaction import Transaction


@dataclass
class TransactionDto:
    """Data transfer object for Transaction."""
    id: str
    account_id: str
    date: datetime
    amount: float
    currency: str
    description: str
    merchant: Optional[str]
    category_id: Optional[str]
    category_name: Optional[str]
    tags: list[str]
    created_at: datetime
    updated_at: Optional[datetime]

    @staticmethod
    def from_entity(transaction: 'Transaction') -> 'TransactionDto':
        """Create DTO from domain entity."""
        return TransactionDto(
            id=str(transaction.id),
            account_id=str(transaction.account_id),
            date=transaction.date,
            amount=transaction.amount.value,
            currency=transaction.amount.currency.value,
            description=transaction.description,
            merchant=transaction.merchant,
            category_id=str(transaction.category.id) if transaction.category else None,
            category_name=transaction.category.name if transaction.category else None,
            tags=transaction.tags,
            created_at=transaction.created_at,
            updated_at=transaction.updated_at,
        )


@dataclass
class CreateTransactionDto:
    """DTO for creating a new transaction."""
    account_id: str
    date: datetime
    amount: float
    currency: str
    description: str
    merchant: Optional[str] = None
    category_id: Optional[str] = None
    tags: Optional[list[str]] = None


@dataclass
class UpdateTransactionDto:
    """DTO for updating a transaction."""
    description: Optional[str] = None
    merchant: Optional[str] = None
    category_id: Optional[str] = None
    tags: Optional[list[str]] = None
