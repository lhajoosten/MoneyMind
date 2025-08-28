"""Transaction database model."""

from typing import List, Optional

from sqlalchemy import Column, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, relationship

from .base import BaseModel


class TransactionModel(BaseModel):
    """Database model for Transaction."""
    __tablename__ = "transactions"

    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), nullable=False)
    description = Column(Text, nullable=False)
    merchant = Column(String(255))
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"))
    tags = Column(String(1000))  # JSON string of tags

    # Relationships
    account: Mapped["AccountModel"] = relationship("AccountModel", back_populates="transactions")
    category: Mapped[Optional["CategoryModel"]] = relationship("CategoryModel", back_populates="transactions")
