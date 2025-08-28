"""Account database model."""

from typing import List

from sqlalchemy import Boolean, Column, Float, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, relationship

from .base import BaseModel


class AccountModel(BaseModel):
    """Database model for Account."""
    __tablename__ = "accounts"

    user_id = Column(UUID(as_uuid=True), nullable=False)
    name = Column(String(100), nullable=False)
    account_type = Column(String(20), nullable=False)
    balance = Column(Float, nullable=False)
    currency = Column(String(3), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationships
    transactions: Mapped[List["TransactionModel"]] = relationship("TransactionModel", back_populates="account")
