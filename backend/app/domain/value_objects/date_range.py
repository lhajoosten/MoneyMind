"""Date range value object."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class DateRange:
    """Value object representing a date range."""
    start_date: datetime
    end_date: datetime

    def __post_init__(self) -> None:
        """Validate the date range."""
        if self.start_date > self.end_date:
            raise ValueError("Start date must be before or equal to end date")

    def contains(self, date: datetime) -> bool:
        """Check if a date is within this range."""
        return self.start_date <= date <= self.end_date

    def duration_days(self) -> int:
        """Get the duration of the range in days."""
        return (self.end_date - self.start_date).days

    def overlaps(self, other: 'DateRange') -> bool:
        """Check if this range overlaps with another range."""
        return (
            self.start_date <= other.end_date and
            self.end_date >= other.start_date
        )

    @staticmethod
    def this_month() -> 'DateRange':
        """Create a DateRange for the current month."""
        now = datetime.now()
        start = datetime(now.year, now.month, 1)
        if now.month == 12:
            end = datetime(now.year + 1, 1, 1)
        else:
            end = datetime(now.year, now.month + 1, 1)
        return DateRange(start, end)

    @staticmethod
    def this_year() -> 'DateRange':
        """Create a DateRange for the current year."""
        now = datetime.now()
        start = datetime(now.year, 1, 1)
        end = datetime(now.year + 1, 1, 1)
        return DateRange(start, end)
