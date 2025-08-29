"""Transaction database model."""

from typing import TYPE_CHECKING, Optional

from sqlalchemy import Column, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, relationship

from app.infrastructure.persistence.models.account import AccountModel

from .base import BaseModel

if TYPE_CHECKING:
    from app.domain.entities.transaction import Transaction
    from app.infrastructure.persistence.models.category import CategoryModel


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
    account: Mapped["AccountModel"] = relationship(
        "AccountModel", back_populates="transactions"
    )
    category: Mapped[Optional["CategoryModel"]] = relationship(
        "CategoryModel", back_populates="transactions"
    )

    @classmethod
    def from_domain(cls, transaction: "Transaction") -> "TransactionModel":
        """Create TransactionModel from domain Transaction entity."""
        import json
        return cls(
            id=transaction.id.value,
            account_id=transaction.account_id.value,
            date=transaction.date,
            amount=float(transaction.amount.value),
            currency=transaction.amount.currency.value,
            description=transaction.description,
            merchant=transaction.merchant,
            category_id=transaction.category.id.value if transaction.category else None,
            tags=json.dumps(transaction.tags) if transaction.tags else None,
            # created_at and updated_at are handled by BaseModel/database
        )

    def to_domain(self) -> "Transaction":
        """Convert TransactionModel to domain Transaction entity."""
        import json
        from decimal import Decimal

        from app.domain.entities.transaction import Transaction
        from app.domain.value_objects.account_id import AccountId
        from app.domain.value_objects.transaction_id import TransactionId
        from app.domain.value_objects.money import Currency, Money

        # Parse tags from JSON string
        tags = json.loads(self.tags) if self.tags else []  # type: ignore

        # Create category if present
        category = None
        if self.category:
            from app.domain.entities.category import Category
            from app.domain.value_objects.category_id import CategoryId

            category = Category(
                id=CategoryId(self.category.id),  # type: ignore
                name=self.category.name,  # type: ignore
                color=self.category.color,  # type: ignore
                icon=self.category.icon,  # type: ignore
                parent_id=CategoryId(self.category.parent_id) if self.category.parent_id else None,  # type: ignore
                is_active=self.category.is_active,  # type: ignore
                budget_limit=Money(Decimal(str(self.category.budget_limit)), Currency(self.category.budget_currency)) if self.category.budget_limit else None,  # type: ignore
            )

        return Transaction(
            id=TransactionId(self.id),  # type: ignore
            account_id=AccountId(self.account_id),  # type: ignore
            date=self.date,  # type: ignore
            amount=Money(Decimal(str(self.amount)), Currency(self.currency)),  # type: ignore
            description=self.description,  # type: ignore
            merchant=self.merchant,  # type: ignore
            category=category,
            tags=tags,
            created_at=self.created_at,  # type: ignore
            updated_at=self.updated_at,  # type: ignore
        )
