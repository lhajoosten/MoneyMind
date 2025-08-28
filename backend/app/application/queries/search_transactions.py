"""Search transactions query."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from ...domain.value_objects.user_id import UserId


@dataclass
class SearchTransactionsQuery:
    """Query to search transactions."""
    user_id: UserId
    search_term: Optional[str] = None
    category_id: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    limit: int = 50
    offset: int = 0

    def __post_init__(self) -> None:
        """Validate the query."""
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValueError("Start date must be before or equal to end date")
        if self.min_amount is not None and self.min_amount < 0:
            raise ValueError("Minimum amount cannot be negative")
        if self.max_amount is not None and self.max_amount < 0:
            raise ValueError("Maximum amount cannot be negative")
        if self.limit < 1 or self.limit > 100:
            raise ValueError("Limit must be between 1 and 100")
        if self.offset < 0:
            raise ValueError("Offset cannot be negative")
