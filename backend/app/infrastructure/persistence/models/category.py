"""Category database model."""

from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, Column, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, relationship

from .base import BaseModel

if TYPE_CHECKING:
    from app.domain.entities.category import Category
    from app.infrastructure.persistence.models.transaction import TransactionModel


class CategoryModel(BaseModel):
    """Database model for Category."""

    __tablename__ = "categories"

    name = Column(String(100), nullable=False)
    color = Column(String(7), nullable=False)  # Hex color code
    icon = Column(String(50), nullable=False)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"))
    is_active = Column(Boolean, default=True, nullable=False)
    budget_limit = Column(Float)
    budget_currency = Column(String(3))

    # Relationships
    parent: Mapped[Optional["CategoryModel"]] = relationship(
        "CategoryModel", remote_side="CategoryModel.id"
    )
    subcategories: Mapped[List["CategoryModel"]] = relationship("CategoryModel")
    transactions: Mapped[List["TransactionModel"]] = relationship(
        "TransactionModel", back_populates="category"
    )

    @classmethod
    def from_domain(cls, category: "Category") -> "CategoryModel":
        """Create CategoryModel from domain Category entity."""
        return cls(
            id=category.id.value,
            name=category.name,
            color=category.color,
            icon=category.icon,
            parent_id=category.parent_id.value if category.parent_id else None,
            is_active=category.is_active,
            budget_limit=float(category.budget_limit.value) if category.budget_limit else None,
            budget_currency=category.budget_limit.currency.value if category.budget_limit else None,
            # created_at and updated_at are handled by BaseModel/database
        )

    def to_domain(self) -> "Category":
        """Convert CategoryModel to domain Category entity."""
        from app.domain.entities.category import Category
        from app.domain.value_objects.category_id import CategoryId
        from app.domain.value_objects.money import Currency, Money
        from decimal import Decimal

        # Create budget limit if present
        budget_limit = None
        if self.budget_limit and self.budget_currency:  # type: ignore
            budget_limit = Money(Decimal(str(self.budget_limit)), Currency(self.budget_currency))  # type: ignore

        return Category(
            id=CategoryId(self.id),  # type: ignore
            name=self.name,  # type: ignore
            color=self.color,  # type: ignore
            icon=self.icon,  # type: ignore
            parent_id=CategoryId(self.parent_id) if self.parent_id else None,  # type: ignore
            is_active=self.is_active,  # type: ignore
            budget_limit=budget_limit,
        )
