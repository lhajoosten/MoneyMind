"""Account repository implementation."""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.account import Account
from app.domain.repositories.account_repository import IAccountRepository
from app.domain.value_objects.account_id import AccountId
from app.domain.value_objects.currency import Currency
from app.domain.value_objects.money import Money
from app.domain.value_objects.user_id import UserId
from ..models.account import AccountModel


class SqlAlchemyAccountRepository(IAccountRepository):
    """SQLAlchemy implementation of AccountRepository."""

    def __init__(self, session: AsyncSession):
        """Initialize repository with database session."""
        self._session = session

    async def get_by_id(self, account_id: AccountId) -> Optional[Account]:
        """Get account by ID."""
        stmt = select(AccountModel).where(AccountModel.id == account_id.value)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return self._model_to_entity(model)

    async def get_by_user(self, user_id: UserId) -> List[Account]:
        """Get all accounts for a user."""
        stmt = select(AccountModel).where(AccountModel.user_id == user_id.value)
        result = await self._session.execute(stmt)
        models = result.scalars().all()

        return [self._model_to_entity(model) for model in models]

    async def save(self, account: Account) -> None:
        """Save an account."""
        model = self._entity_to_model(account)
        self._session.add(model)
        await self._session.flush()

        # Update entity ID if it was generated
        if account.id.value != model.id:
            account.id = AccountId(model.id)

    async def delete(self, account_id: AccountId) -> None:
        """Delete an account."""
        stmt = select(AccountModel).where(AccountModel.id == account_id.value)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()

        if model:
            await self._session.delete(model)

    def _model_to_entity(self, model: AccountModel) -> Account:
        """Convert database model to domain entity."""
        return Account(
            id=AccountId(model.id),
            user_id=UserId(model.user_id),
            name=model.name,
            account_type=model.account_type,
            balance=Money(model.balance, Currency(model.currency)),
            is_active=model.is_active,
        )

    def _entity_to_model(self, entity: Account) -> AccountModel:
        """Convert domain entity to database model."""
        return AccountModel(
            id=entity.id.value if hasattr(entity.id, 'value') else entity.id,
            user_id=entity.user_id.value,
            name=entity.name,
            account_type=entity.account_type,
            balance=entity.balance.value,
            currency=entity.balance.currency.value,
            is_active=entity.is_active,
        )
