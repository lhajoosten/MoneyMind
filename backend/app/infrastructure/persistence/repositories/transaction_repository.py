"""Transaction repository implementation."""

import json
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.transaction import Transaction
from app.domain.repositories.transaction_repository import ITransactionRepository
from app.domain.value_objects.account_id import AccountId
from app.domain.value_objects.transaction_id import TransactionId
from ..models.transaction import TransactionModel


class SqlAlchemyTransactionRepository(ITransactionRepository):
    """SQLAlchemy implementation of TransactionRepository."""

    def __init__(self, session: AsyncSession):
        """Initialize repository with database session."""
        self._session = session

    async def get_by_id(self, transaction_id: TransactionId) -> Optional[Transaction]:
        """Get transaction by ID."""
        stmt = select(TransactionModel).where(TransactionModel.id == transaction_id.value)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return self._model_to_entity(model)

    async def get_by_account(self, account_id: AccountId) -> List[Transaction]:
        """Get all transactions for an account."""
        stmt = select(TransactionModel).where(TransactionModel.account_id == account_id.value)
        result = await self._session.execute(stmt)
        models = result.scalars().all()

        return [self._model_to_entity(model) for model in models]

    async def save(self, transaction: Transaction) -> None:
        """Save a transaction."""
        model = self._entity_to_model(transaction)
        self._session.add(model)
        await self._session.flush()

        # Update entity ID if it was generated
        if transaction.id.value != model.id:
            transaction.id = TransactionId(model.id)

    async def delete(self, transaction_id: TransactionId) -> None:
        """Delete a transaction."""
        stmt = select(TransactionModel).where(TransactionModel.id == transaction_id.value)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()

        if model:
            await self._session.delete(model)

    def _model_to_entity(self, model: TransactionModel) -> Transaction:
        """Convert database model to domain entity."""
        from app.domain.entities.category import Category
        from app.domain.value_objects.category_id import CategoryId
        from app.domain.value_objects.currency import Currency
        from app.domain.value_objects.money import Money

        # Parse tags from JSON string
        tags = json.loads(model.tags) if model.tags else []

        # Create category if present
        category = None
        if model.category:
            category = Category(
                id=CategoryId(model.category.id),
                name=model.category.name,
                color=model.category.color,
                icon=model.category.icon,
                parent_id=CategoryId(model.category.parent_id) if model.category.parent_id else None,
                is_active=model.category.is_active,
                budget_limit=Money(model.category.budget_limit, Currency(model.category.budget_currency)) if model.category.budget_limit else None,
            )

        return Transaction(
            id=TransactionId(model.id),
            account_id=AccountId(model.account_id),
            date=model.date,
            amount=Money(model.amount, Currency(model.currency)),
            description=model.description,
            merchant=model.merchant,
            category=category,
            tags=tags,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _entity_to_model(self, entity: Transaction) -> TransactionModel:
        """Convert domain entity to database model."""
        return TransactionModel(
            id=entity.id.value if hasattr(entity.id, 'value') else entity.id,
            account_id=entity.account_id.value,
            date=entity.date,
            amount=entity.amount.value,
            currency=entity.amount.currency.value,
            description=entity.description,
            merchant=entity.merchant,
            category_id=entity.category.id.value if entity.category else None,
            tags=json.dumps(entity.tags) if entity.tags else None,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
