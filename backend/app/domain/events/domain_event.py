"""Base domain event."""

from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class DomainEvent(ABC):
    """Base class for all domain events."""
    occurred_at: datetime
    event_data: dict[str, Any]

    def __post_init__(self) -> None:
        """Set the occurred_at timestamp if not provided."""
        if self.occurred_at is None:
            self.occurred_at = datetime.now()
