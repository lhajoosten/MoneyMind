"""Transaction repository implementation."""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import selectinload

from app.domain.entities.transaction import Transaction
from app.domain.repositories.transaction_repository import ITransactionRepository
from app.domain.value_objects.account_id import AccountId
from app.domain.value_objects.transaction_id import TransactionId
from ..models.transaction import TransactionModel


class SqlAlchemyTransactionRepository(ITransactionRepository):
    """SQLAlchemy implementation of TransactionRepository."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        """Initialize repository with session factory."""
        self.session_factory = session_factory

    async def get_by_id(self, transaction_id: TransactionId) -> Optional[Transaction]:
        """Get transaction by ID."""
        from sqlalchemy.orm import selectinload
        
        async with self.session_factory() as session:
            stmt = select(TransactionModel).where(TransactionModel.id == transaction_id.value).options(
                selectinload(TransactionModel.account),
                selectinload(TransactionModel.category)
            )
            result = await session.execute(stmt)
            model = result.scalar_one_or_none()

            if model is None:
                return None

            return model.to_domain()

    async def get_by_account(self, account_id: AccountId) -> List[Transaction]:
        """Get all transactions for an account."""
        async with self.session_factory() as session:
            stmt = select(TransactionModel).where(TransactionModel.account_id == account_id.value)
            result = await session.execute(stmt)
            models = result.scalars().all()

            return [model.to_domain() for model in models]

    async def get_all(self) -> List[Transaction]:
        """Get all transactions."""
        async with self.session_factory() as session:
            # Eager load category relationship to avoid lazy loading issues
            stmt = select(TransactionModel).options(
                selectinload(TransactionModel.category)
            )
            result = await session.execute(stmt)
            models = result.scalars().all()

            return [model.to_domain() for model in models]

    async def save(self, transaction: Transaction) -> None:
        """Save a transaction."""
        async with self.session_factory() as session:
            model = TransactionModel.from_domain(transaction)
            # Use merge to handle both INSERT and UPDATE cases
            merged_model = await session.merge(model)
            await session.commit()

            # Update entity ID if it was generated
            if transaction.id.value != merged_model.id:
                transaction.id = TransactionId(merged_model.id)  # type: ignore

    async def delete(self, transaction_id: TransactionId) -> None:
        """Delete a transaction."""
        async with self.session_factory() as session:
            stmt = select(TransactionModel).where(TransactionModel.id == transaction_id.value)
            result = await session.execute(stmt)
            model = result.scalar_one_or_none()

            if model:
                await session.delete(model)
                await session.commit()
