"""Category repository implementation."""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.category import Category
from app.domain.repositories.category_repository import ICategoryRepository
from app.domain.value_objects.category_id import CategoryId
from app.domain.value_objects.currency import Currency
from app.domain.value_objects.money import Money
from ..models.category import CategoryModel


class SqlAlchemyCategoryRepository(ICategoryRepository):
    """SQLAlchemy implementation of CategoryRepository."""

    def __init__(self, session: AsyncSession):
        """Initialize repository with database session."""
        self._session = session

    async def get_by_id(self, category_id: CategoryId) -> Optional[Category]:
        """Get category by ID."""
        stmt = select(CategoryModel).where(CategoryModel.id == category_id.value)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return self._model_to_entity(model)

    async def get_all_active(self) -> List[Category]:
        """Get all active categories."""
        stmt = select(CategoryModel).where(CategoryModel.is_active == True)
        result = await self._session.execute(stmt)
        models = result.scalars().all()

        return [self._model_to_entity(model) for model in models]

    async def get_by_parent(self, parent_id: CategoryId) -> List[Category]:
        """Get subcategories for a parent category."""
        stmt = select(CategoryModel).where(CategoryModel.parent_id == parent_id.value)
        result = await self._session.execute(stmt)
        models = result.scalars().all()

        return [self._model_to_entity(model) for model in models]

    async def save(self, category: Category) -> None:
        """Save a category."""
        model = self._entity_to_model(category)
        self._session.add(model)
        await self._session.flush()

        # Update entity ID if it was generated
        if category.id.value != model.id:
            category.id = CategoryId(model.id)

    async def delete(self, category_id: CategoryId) -> None:
        """Delete a category."""
        stmt = select(CategoryModel).where(CategoryModel.id == category_id.value)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()

        if model:
            await self._session.delete(model)

    def _model_to_entity(self, model: CategoryModel) -> Category:
        """Convert database model to domain entity."""
        # Create budget limit if present
        budget_limit = None
        if model.budget_limit is not None and model.budget_currency:
            budget_limit = Money(model.budget_limit, Currency(model.budget_currency))

        return Category(
            id=CategoryId(model.id),
            name=model.name,
            color=model.color,
            icon=model.icon,
            parent_id=CategoryId(model.parent_id) if model.parent_id else None,
            is_active=model.is_active,
            budget_limit=budget_limit,
        )

    def _entity_to_model(self, entity: Category) -> CategoryModel:
        """Convert domain entity to database model."""
        return CategoryModel(
            id=entity.id.value if hasattr(entity.id, 'value') else entity.id,
            name=entity.name,
            color=entity.color,
            icon=entity.icon,
            parent_id=entity.parent_id.value if entity.parent_id else None,
            is_active=entity.is_active,
            budget_limit=entity.budget_limit.value if entity.budget_limit else None,
            budget_currency=entity.budget_limit.currency.value if entity.budget_limit else None,
        )
