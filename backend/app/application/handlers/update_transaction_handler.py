"""Update transaction command handler."""

from datetime import datetime
from typing import Optional, Protocol

from ..commands.update_transaction import UpdateTransactionCommand
from ...domain.entities.transaction import Transaction
from ...domain.repositories.transaction_repository import ITransactionRepository
from ...domain.repositories.category_repository import ICategoryRepository


class IUpdateTransactionHandler(Protocol):
    """Handler interface for updating transactions."""

    async def handle(self, command: UpdateTransactionCommand) -> Optional[Transaction]:
        """Handle update transaction command."""
        ...


class UpdateTransactionHandler:
    """Handler for updating transactions."""

    def __init__(
        self,
        transaction_repository: ITransactionRepository,
        category_repository: ICategoryRepository
    ):
        """Initialize handler with dependencies."""
        self._transaction_repository = transaction_repository
        self._category_repository = category_repository

    async def handle(self, command: UpdateTransactionCommand) -> Optional[Transaction]:
        """Handle update transaction command."""
        # Get existing transaction
        transaction = await self._transaction_repository.get_by_id(command.transaction_id)
        if not transaction:
            return None

        # Load new category if category_id is provided
        if command.category_id:
            category = await self._category_repository.get_by_id(command.category_id)
            if category:
                transaction.category = category

        # Update fields if provided
        if command.description is not None:
            transaction.description = command.description
        if command.merchant is not None:
            transaction.merchant = command.merchant
        if command.tags is not None:
            transaction.tags = command.tags

        # Update timestamp
        transaction.updated_at = datetime.utcnow()

        # Save updated transaction
        await self._transaction_repository.save(transaction)

        return transaction
