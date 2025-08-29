"""Delete transaction command."""

from dataclasses import dataclass

from ...domain.value_objects.transaction_id import TransactionId


@dataclass
class DeleteTransactionCommand:
    """Command to delete a transaction."""
    transaction_id: TransactionId
