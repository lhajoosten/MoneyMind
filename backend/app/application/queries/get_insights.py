"""Get insights query."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from ...domain.value_objects.user_id import UserId


@dataclass
class GetInsightsQuery:
    """Query to get financial insights."""
    user_id: UserId
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    insight_types: Optional[list[str]] = None  # ['pattern', 'anomaly', 'suggestion']

    def __post_init__(self) -> None:
        """Validate the query."""
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValueError("Start date must be before or equal to end date")
