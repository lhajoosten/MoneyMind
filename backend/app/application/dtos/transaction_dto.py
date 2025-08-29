"""Transaction DTOs."""

from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Optional, List

from pydantic import BaseModel, Field
from ...domain.value_objects.money import Money

if TYPE_CHECKING:
    from ...domain.entities.transaction import Transaction


@dataclass
class TransactionDto:
    """Data transfer object for Transaction."""
    id: str
    account_id: str
    date: datetime
    amount: float
    currency: str
    description: str
    merchant: Optional[str]
    category_id: Optional[str]
    category_name: Optional[str]
    tags: list[str]
    created_at: datetime
    updated_at: Optional[datetime]

    @staticmethod
    def from_entity(transaction: 'Transaction') -> 'TransactionDto':
        """Create DTO from domain entity."""
        return TransactionDto(
            id=str(transaction.id),
            account_id=str(transaction.account_id),
            date=transaction.date,
            amount=float(transaction.amount.value),
            currency=transaction.amount.currency.value,
            description=transaction.description,
            merchant=transaction.merchant,
            category_id=str(transaction.category.id) if transaction.category else None,
            category_name=transaction.category.name if transaction.category else None,
            tags=transaction.tags,
            created_at=transaction.created_at,
            updated_at=transaction.updated_at,
        )


@dataclass
class CreateTransactionDto:
    """DTO for creating a new transaction."""
    account_id: str
    date: datetime
    amount: float
    currency: str
    description: str
    merchant: Optional[str] = None
    category_id: Optional[str] = None
    tags: Optional[list[str]] = None


@dataclass
class UpdateTransactionDto:
    """DTO for updating a transaction."""
    description: Optional[str] = None
    merchant: Optional[str] = None
    category_id: Optional[str] = None
    tags: Optional[list[str]] = None


# Pydantic models for API requests and responses
class CreateTransactionRequest(BaseModel):
    """Request model for creating a transaction."""
    account_id: str = Field(..., description="Account ID")
    date: datetime = Field(..., description="Transaction date")
    amount: float = Field(..., description="Transaction amount")
    currency: str = Field(..., description="Transaction currency")
    description: str = Field(..., description="Transaction description")
    merchant: Optional[str] = Field(None, description="Merchant name")
    category_id: Optional[str] = Field(None, description="Category ID")
    tags: Optional[List[str]] = Field(None, description="Transaction tags")


class UpdateTransactionRequest(BaseModel):
    """Request model for updating a transaction."""
    description: Optional[str] = Field(None, description="Transaction description")
    merchant: Optional[str] = Field(None, description="Merchant name")
    category_id: Optional[str] = Field(None, description="Category ID")
    tags: Optional[List[str]] = Field(None, description="Transaction tags")


class CategorizeTransactionRequest(BaseModel):
    """Request model for categorizing a transaction."""
    category_id: str = Field(..., description="Category ID")


class SearchTransactionsRequest(BaseModel):
    """Request model for searching transactions."""
    user_id: str = Field(..., description="User ID for filtering transactions")
    search_term: Optional[str] = Field(None, description="Search term for description or merchant")
    category_id: Optional[str] = Field(None, description="Filter by category ID")
    start_date: Optional[datetime] = Field(None, description="Start date filter")
    end_date: Optional[datetime] = Field(None, description="End date filter")
    min_amount: Optional[float] = Field(None, description="Minimum amount filter")
    max_amount: Optional[float] = Field(None, description="Maximum amount filter")
    limit: int = Field(50, description="Maximum number of results", ge=1, le=1000)
    offset: int = Field(0, description="Number of results to skip", ge=0)


class TransactionResponse(BaseModel):
    """Response model for transaction data."""
    id: str
    account_id: str
    date: datetime
    amount: float
    currency: str
    description: str
    merchant: Optional[str]
    category_id: Optional[str]
    category_name: Optional[str]
    tags: List[str]
    created_at: datetime
    updated_at: Optional[datetime]

    @classmethod
    def from_dto(cls, dto: TransactionDto) -> "TransactionResponse":
        """Create response from DTO."""
        return cls(
            id=dto.id,
            account_id=dto.account_id,
            date=dto.date,
            amount=dto.amount,
            currency=dto.currency,
            description=dto.description,
            merchant=dto.merchant,
            category_id=dto.category_id,
            category_name=dto.category_name,
            tags=dto.tags,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )
