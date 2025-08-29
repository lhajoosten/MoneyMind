"""Update transaction command."""

from dataclasses import dataclass
from typing import Optional

from ...domain.value_objects.category_id import CategoryId
from ...domain.value_objects.transaction_id import TransactionId


@dataclass
class UpdateTransactionCommand:
    """Command to update an existing transaction."""
    transaction_id: TransactionId
    description: Optional[str] = None
    merchant: Optional[str] = None
    category_id: Optional[CategoryId] = None
    tags: Optional[list[str]] = None
