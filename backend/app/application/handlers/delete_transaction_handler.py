"""Delete transaction command handler."""

from typing import Protocol

from ..commands.delete_transaction import DeleteTransactionCommand
from ...domain.repositories.transaction_repository import ITransactionRepository


class IDeleteTransactionHandler(Protocol):
    """Handler interface for deleting transactions."""

    async def handle(self, command: DeleteTransactionCommand) -> bool:
        """Handle delete transaction command."""
        ...


class DeleteTransactionHandler:
    """Handler for deleting transactions."""

    def __init__(self, transaction_repository: ITransactionRepository):
        """Initialize handler with dependencies."""
        self._transaction_repository = transaction_repository

    async def handle(self, command: DeleteTransactionCommand) -> bool:
        """Handle delete transaction command."""
        # Check if transaction exists
        existing_transaction = await self._transaction_repository.get_by_id(command.transaction_id)
        if not existing_transaction:
            return False

        # Delete the transaction
        await self._transaction_repository.delete(command.transaction_id)
        return True
