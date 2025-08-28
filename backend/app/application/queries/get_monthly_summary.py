"""Get monthly summary query."""

from dataclasses import dataclass
from datetime import datetime

from ...domain.value_objects.user_id import UserId


@dataclass
class GetMonthlySummaryQuery:
    """Query to get monthly financial summary."""
    user_id: UserId
    month: int
    year: int

    def __post_init__(self) -> None:
        """Validate the query."""
        if not 1 <= self.month <= 12:
            raise ValueError("Month must be between 1 and 12")
        if self.year < 2000:
            raise ValueError("Year must be 2000 or later")
