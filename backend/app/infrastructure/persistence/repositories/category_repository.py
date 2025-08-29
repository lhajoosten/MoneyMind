"""Category repository implementation."""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.domain.entities.category import Category
from app.domain.repositories.category_repository import ICategoryRepository
from app.domain.value_objects.category_id import CategoryId
from app.domain.value_objects.currency import Currency
from app.domain.value_objects.money import Money
from ..models.category import CategoryModel


class SqlAlchemyCategoryRepository(ICategoryRepository):
    """SQLAlchemy implementation of CategoryRepository."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        """Initialize repository with session factory."""
        self.session_factory = session_factory

    async def get_by_id(self, category_id: CategoryId) -> Optional[Category]:
        """Get category by ID."""
        from sqlalchemy.orm import selectinload
        
        async with self.session_factory() as session:
            stmt = select(CategoryModel).where(CategoryModel.id == category_id.value).options(
                selectinload(CategoryModel.parent),
                selectinload(CategoryModel.subcategories)
            )
            result = await session.execute(stmt)
            model = result.scalar_one_or_none()

            if model is None:
                return None

            return model.to_domain()

    async def get_all_active(self) -> List[Category]:
        """Get all active categories."""
        async with self.session_factory() as session:
            stmt = select(CategoryModel).where(CategoryModel.is_active == True)
            result = await session.execute(stmt)
            models = result.scalars().all()

            return [model.to_domain() for model in models]

    async def get_by_parent(self, parent_id: CategoryId) -> List[Category]:
        """Get subcategories for a parent category."""
        async with self.session_factory() as session:
            stmt = select(CategoryModel).where(CategoryModel.parent_id == parent_id.value)
            result = await session.execute(stmt)
            models = result.scalars().all()

            return [model.to_domain() for model in models]

    async def save(self, category: Category) -> None:
        """Save a category."""
        async with self.session_factory() as session:
            model = CategoryModel.from_domain(category)
            session.add(model)
            await session.flush()

            # Update entity ID if it was generated
            if category.id.value != model.id:
                category.id = CategoryId(model.id)  # type: ignore

    async def delete(self, category_id: CategoryId) -> None:
        """Delete a category."""
        async with self.session_factory() as session:
            stmt = select(CategoryModel).where(CategoryModel.id == category_id.value)
            result = await session.execute(stmt)
            model = result.scalar_one_or_none()

            if model:
                await session.delete(model)
