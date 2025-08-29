"""Create transaction command handler."""

from datetime import datetime
from typing import Optional, Protocol

from ..commands.create_transaction import CreateTransactionCommand
from ...domain.entities.transaction import Transaction
from ...domain.repositories.transaction_repository import ITransactionRepository
from ...domain.repositories.category_repository import ICategoryRepository
from ...domain.value_objects.transaction_id import TransactionId


class ICreateTransactionHandler(Protocol):
    """Handler interface for creating transactions."""

    async def handle(self, command: CreateTransactionCommand) -> Transaction:
        """Handle create transaction command."""
        ...


class CreateTransactionHandler:
    """Handler for creating transactions."""

    def __init__(
        self,
        transaction_repository: ITransactionRepository,
        category_repository: ICategoryRepository
    ):
        """Initialize handler with dependencies."""
        self._transaction_repository = transaction_repository
        self._category_repository = category_repository

    async def handle(self, command: CreateTransactionCommand) -> Transaction:
        """Handle create transaction command."""
        # Load category if category_id is provided
        category = None
        if command.category_id:
            category = await self._category_repository.get_by_id(command.category_id)

        # Create new transaction entity
        transaction = Transaction(
            id=TransactionId.new(),  # Generate new ID
            account_id=command.account_id,
            date=command.date,
            amount=command.amount,
            description=command.description,
            merchant=command.merchant,
            category=category,  # Pass category entity, not ID
            tags=command.tags or [],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        # Save to repository
        await self._transaction_repository.save(transaction)

        return transaction
