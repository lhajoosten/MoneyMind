"""Budget database model."""

from sqlalchemy import Column, DateTime, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from .base import BaseModel


class BudgetModel(BaseModel):
    """Database model for Budget."""
    __tablename__ = "budgets"

    user_id = Column(UUID(as_uuid=True), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False)
    limit_amount = Column(Float, nullable=False)
    currency = Column(String(3), nullable=False)
    period = Column(String(20), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
