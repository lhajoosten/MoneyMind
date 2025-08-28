"""Budget repository implementation."""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.budget import Budget
from app.domain.repositories.budget_repository import IBudgetRepository
from app.domain.value_objects.budget_id import BudgetId
from app.domain.value_objects.category_id import CategoryId
from app.domain.value_objects.currency import Currency
from app.domain.value_objects.money import Money
from app.domain.value_objects.user_id import UserId
from ..models.budget import BudgetModel


class SqlAlchemyBudgetRepository(IBudgetRepository):
    """SQLAlchemy implementation of BudgetRepository."""

    def __init__(self, session: AsyncSession):
        """Initialize repository with database session."""
        self._session = session

    async def get_by_id(self, budget_id: BudgetId) -> Optional[Budget]:
        """Get budget by ID."""
        stmt = select(BudgetModel).where(BudgetModel.id == budget_id.value)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return self._model_to_entity(model)

    async def get_by_user(self, user_id: UserId) -> List[Budget]:
        """Get all budgets for a user."""
        stmt = select(BudgetModel).where(BudgetModel.user_id == user_id.value)
        result = await self._session.execute(stmt)
        models = result.scalars().all()

        return [self._model_to_entity(model) for model in models]

    async def get_active_for_date(self, user_id: UserId, date: datetime) -> List[Budget]:
        """Get active budgets for a user on a specific date."""
        stmt = select(BudgetModel).where(
            and_(
                BudgetModel.user_id == user_id.value,
                BudgetModel.start_date <= date,
                BudgetModel.end_date >= date
            )
        )
        result = await self._session.execute(stmt)
        models = result.scalars().all()

        return [self._model_to_entity(model) for model in models]

    async def save(self, budget: Budget) -> None:
        """Save a budget."""
        model = self._entity_to_model(budget)
        self._session.add(model)
        await self._session.flush()

        # Update entity ID if it was generated
        if budget.id.value != model.id:
            budget.id = BudgetId(model.id)

    async def delete(self, budget_id: BudgetId) -> None:
        """Delete a budget."""
        stmt = select(BudgetModel).where(BudgetModel.id == budget_id.value)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()

        if model:
            await self._session.delete(model)

    def _model_to_entity(self, model: BudgetModel) -> Budget:
        """Convert database model to domain entity."""
        return Budget(
            id=BudgetId(model.id),
            user_id=UserId(model.user_id),
            category_id=CategoryId(model.category_id),
            limit_amount=Money(model.limit_amount, Currency(model.currency)),
            period=model.period,
            start_date=model.start_date,
            end_date=model.end_date,
        )

    def _entity_to_model(self, entity: Budget) -> BudgetModel:
        """Convert domain entity to database model."""
        return BudgetModel(
            id=entity.id.value if hasattr(entity.id, 'value') else entity.id,
            user_id=entity.user_id.value,
            category_id=entity.category_id.value,
            limit_amount=entity.limit_amount.value,
            currency=entity.limit_amount.currency.value,
            period=entity.period,
            start_date=entity.start_date,
            end_date=entity.end_date,
        )
