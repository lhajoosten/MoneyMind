"""Transaction application service."""

from datetime import datetime
from typing import List, Optional, Protocol

from ..commands.create_transaction import CreateTransactionCommand
from ..commands.update_transaction import UpdateTransactionCommand
from ..commands.delete_transaction import DeleteTransactionCommand
from ..commands.categorize_transaction import CategorizeTransactionCommand
from ..handlers.create_transaction_handler import CreateTransactionHandler
from ..handlers.update_transaction_handler import UpdateTransactionHandler
from ..handlers.delete_transaction_handler import DeleteTransactionHandler
from ..handlers.categorize_transaction_handler import CategorizeTransactionHandler
from ..queries.search_transactions import SearchTransactionsQuery
from ..queries.search_transactions_handler import SearchTransactionsQueryHandler
from ..dtos.transaction_dto import TransactionDto
from ...domain.entities.transaction import Transaction
from ...domain.repositories.transaction_repository import ITransactionRepository
from ...domain.repositories.category_repository import ICategoryRepository
from ...domain.value_objects.account_id import AccountId
from ...domain.value_objects.category_id import CategoryId
from ...domain.value_objects.transaction_id import TransactionId
from ...domain.value_objects.money import Money


class ITransactionService(Protocol):
    """Transaction service interface."""

    async def create_transaction(
        self,
        account_id: AccountId,
        date: datetime,
        amount: Money,
        description: str,
        merchant: Optional[str] = None,
        category_id: Optional[CategoryId] = None,
        tags: Optional[List[str]] = None,
    ) -> Transaction:
        """Create a new transaction."""
        ...

    async def get_transaction(self, transaction_id: TransactionId) -> Optional[Transaction]:
        """Get transaction by ID."""
        ...

    async def get_transactions_by_account(self, account_id: AccountId) -> List[Transaction]:
        """Get all transactions for an account."""
        ...

    async def search_transactions(self, query: SearchTransactionsQuery) -> List[TransactionDto]:
        """Search transactions with filters."""
        ...

    async def update_transaction(
        self,
        transaction_id: TransactionId,
        description: Optional[str] = None,
        merchant: Optional[str] = None,
        category_id: Optional[CategoryId] = None,
        tags: Optional[List[str]] = None,
    ) -> Optional[Transaction]:
        """Update an existing transaction."""
        ...

    async def delete_transaction(self, transaction_id: TransactionId) -> bool:
        """Delete a transaction."""
        ...

    async def categorize_transaction(
        self,
        transaction_id: TransactionId,
        category_id: CategoryId,
    ) -> Optional[Transaction]:
        """Categorize a transaction."""
        ...


class TransactionService:
    """Application service for transaction operations."""

    def __init__(
        self,
        transaction_repository: ITransactionRepository,
        category_repository: ICategoryRepository,
        search_handler: SearchTransactionsQueryHandler,
    ):
        """Initialize service with dependencies."""
        self._transaction_repository = transaction_repository
        self._category_repository = category_repository
        self._search_handler = search_handler

        # Initialize command handlers
        self._create_handler = CreateTransactionHandler(
            transaction_repository, category_repository
        )
        self._update_handler = UpdateTransactionHandler(
            transaction_repository, category_repository
        )
        self._delete_handler = DeleteTransactionHandler(transaction_repository)
        self._categorize_handler = CategorizeTransactionHandler(
            transaction_repository, category_repository
        )

    async def create_transaction(
        self,
        account_id: AccountId,
        date: datetime,
        amount: Money,
        description: str,
        merchant: Optional[str] = None,
        category_id: Optional[CategoryId] = None,
        tags: Optional[List[str]] = None,
    ) -> Transaction:
        """Create a new transaction."""
        command = CreateTransactionCommand(
            account_id=account_id,
            date=date,
            amount=amount,
            description=description,
            merchant=merchant,
            category_id=category_id,
            tags=tags,
        )
        return await self._create_handler.handle(command)

    async def get_transaction(self, transaction_id: TransactionId) -> Optional[Transaction]:
        """Get transaction by ID."""
        return await self._transaction_repository.get_by_id(transaction_id)

    async def get_transactions_by_account(self, account_id: AccountId) -> List[Transaction]:
        """Get all transactions for an account."""
        return await self._transaction_repository.get_by_account(account_id)

    async def search_transactions(self, query: SearchTransactionsQuery) -> List[TransactionDto]:
        """Search transactions with filters."""
        return await self._search_handler.handle(query)

    async def update_transaction(
        self,
        transaction_id: TransactionId,
        description: Optional[str] = None,
        merchant: Optional[str] = None,
        category_id: Optional[CategoryId] = None,
        tags: Optional[List[str]] = None,
    ) -> Optional[Transaction]:
        """Update an existing transaction."""
        command = UpdateTransactionCommand(
            transaction_id=transaction_id,
            description=description,
            merchant=merchant,
            category_id=category_id,
            tags=tags,
        )
        return await self._update_handler.handle(command)

    async def delete_transaction(self, transaction_id: TransactionId) -> bool:
        """Delete a transaction."""
        command = DeleteTransactionCommand(transaction_id=transaction_id)
        return await self._delete_handler.handle(command)

    async def categorize_transaction(
        self,
        transaction_id: TransactionId,
        category_id: CategoryId,
    ) -> Optional[Transaction]:
        """Categorize a transaction."""
        command = CategorizeTransactionCommand(
            transaction_id=transaction_id,
            category_id=category_id,
        )
        return await self._categorize_handler.handle(command)
