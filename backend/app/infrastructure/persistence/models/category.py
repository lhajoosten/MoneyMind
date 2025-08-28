"""Category database model."""

from typing import List, Optional

from sqlalchemy import Boolean, Column, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, relationship

from .base import BaseModel


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
    parent: Mapped[Optional["CategoryModel"]] = relationship("CategoryModel", remote_side=[id])
    subcategories: Mapped[List["CategoryModel"]] = relationship("CategoryModel")
    transactions: Mapped[List["TransactionModel"]] = relationship("TransactionModel", back_populates="category")
