"""Transaction domain events."""

from dataclasses import dataclass
from datetime import datetime

from .domain_event import DomainEvent
from ..value_objects.category_id import CategoryId
from ..value_objects.transaction_id import TransactionId


@dataclass
class TransactionCategorizedEvent(DomainEvent):
    """Event raised when a transaction is categorized."""
    transaction_id: TransactionId
    category_id: CategoryId

    def __post_init__(self) -> None:
        """Initialize event data."""
        super().__post_init__()
        self.event_data = {
            "transaction_id": str(self.transaction_id),
            "category_id": str(self.category_id)
        }
