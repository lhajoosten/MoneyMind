"""Transaction repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional, Protocol

from app.domain.entities.transaction import Transaction
from app.domain.value_objects.account_id import AccountId
from app.domain.value_objects.transaction_id import TransactionId


class ITransactionRepository(Protocol):
    """Repository interface for Transaction entities."""

    @abstractmethod
    async def get_by_id(self, transaction_id: TransactionId) -> Optional[Transaction]:
        """Get transaction by ID."""
        ...

    @abstractmethod
    async def get_by_account(self, account_id: AccountId) -> List[Transaction]:
        """Get all transactions for an account."""
        ...

    @abstractmethod
    async def save(self, transaction: Transaction) -> None:
        """Save a transaction."""
        ...

    @abstractmethod
    async def delete(self, transaction_id: TransactionId) -> None:
        """Delete a transaction."""
        ...
