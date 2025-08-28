"""Categorize transaction command."""

from dataclasses import dataclass

from ...domain.value_objects.category_id import CategoryId
from ...domain.value_objects.transaction_id import TransactionId


@dataclass
class CategorizeTransactionCommand:
    """Command to categorize a transaction."""
    transaction_id: TransactionId
    category_id: CategoryId
