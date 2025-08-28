"""Category repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional, Protocol

from app.domain.entities.category import Category
from app.domain.value_objects.category_id import CategoryId


class ICategoryRepository(Protocol):
    """Repository interface for Category entities."""

    @abstractmethod
    async def get_by_id(self, category_id: CategoryId) -> Optional[Category]:
        """Get category by ID."""
        ...

    @abstractmethod
    async def get_all_active(self) -> List[Category]:
        """Get all active categories."""
        ...

    @abstractmethod
    async def get_by_parent(self, parent_id: CategoryId) -> List[Category]:
        """Get subcategories for a parent category."""
        ...

    @abstractmethod
    async def save(self, category: Category) -> None:
        """Save a category."""
        ...

    @abstractmethod
    async def delete(self, category_id: CategoryId) -> None:
        """Delete a category."""
        ...
