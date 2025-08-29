"""Categorize transaction command handler."""

from datetime import datetime
from typing import Optional, Protocol

from ..commands.categorize_transaction import CategorizeTransactionCommand
from ...domain.entities.transaction import Transaction
from ...domain.repositories.transaction_repository import ITransactionRepository
from ...domain.repositories.category_repository import ICategoryRepository


class ICategorizeTransactionHandler(Protocol):
    """Handler interface for categorizing transactions."""

    async def handle(self, command: CategorizeTransactionCommand) -> Optional[Transaction]:
        """Handle categorize transaction command."""
        ...


class CategorizeTransactionHandler:
    """Handler for categorizing transactions."""

    def __init__(
        self,
        transaction_repository: ITransactionRepository,
        category_repository: ICategoryRepository
    ):
        """Initialize handler with dependencies."""
        self._transaction_repository = transaction_repository
        self._category_repository = category_repository

    async def handle(self, command: CategorizeTransactionCommand) -> Optional[Transaction]:
        """Handle categorize transaction command."""
        # Get existing transaction
        transaction = await self._transaction_repository.get_by_id(command.transaction_id)
        if not transaction:
            return None

        # Get the category
        category = await self._category_repository.get_by_id(command.category_id)
        if not category:
            return None

        # Update transaction category
        transaction.category = category
        transaction.updated_at = datetime.utcnow()

        # Save updated transaction
        await self._transaction_repository.save(transaction)

        return transaction
