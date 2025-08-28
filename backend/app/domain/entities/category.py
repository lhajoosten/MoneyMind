"""Category domain entity."""

from dataclasses import dataclass
from typing import Optional

from .value_objects.category_id import CategoryId
from .value_objects.money import Money


@dataclass
class Category:
    """Domain entity representing a transaction category."""
    id: CategoryId
    name: str
    color: str
    icon: str
    parent_id: Optional[CategoryId]
    is_active: bool
    budget_limit: Optional[Money]

    def __post_init__(self) -> None:
        """Validate the category."""
        if not self.name or not self.name.strip():
            raise ValueError("Category name cannot be empty")
        if not self.color or not self.color.strip():
            raise ValueError("Category color cannot be empty")
        if not self.icon or not self.icon.strip():
            raise ValueError("Category icon cannot be empty")

    def is_subcategory(self) -> bool:
        """Check if this is a subcategory."""
        return self.parent_id is not None

    def has_budget_limit(self) -> bool:
        """Check if this category has a budget limit."""
        return self.budget_limit is not None

    def update_budget_limit(self, limit: Optional[Money]) -> None:
        """Update the budget limit."""
        self.budget_limit = limit

    def deactivate(self) -> None:
        """Deactivate the category."""
        self.is_active = False

    def activate(self) -> None:
        """Activate the category."""
        self.is_active = True
