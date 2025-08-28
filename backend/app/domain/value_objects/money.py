"""Value objects for the MoneyMind domain."""

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import Union


class Currency(Enum):
    """Supported currencies."""
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    CAD = "CAD"
    AUD = "AUD"


@dataclass(frozen=True)
class Money:
    """Value object representing monetary amounts with currency support."""
    value: Decimal
    currency: Currency = Currency.USD

    def __post_init__(self) -> None:
        """Validate the money value."""
        if self.value is None:
            raise ValueError("Money value cannot be None")
        if not isinstance(self.value, Decimal):
            raise ValueError("Money value must be a Decimal")

    def add(self, other: 'Money') -> 'Money':
        """Add two Money objects."""
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(self.value + other.value, self.currency)

    def subtract(self, other: 'Money') -> 'Money':
        """Subtract two Money objects."""
        if self.currency != other.currency:
            raise ValueError("Cannot subtract different currencies")
        return Money(self.value - other.value, self.currency)

    def multiply(self, factor: Union[int, float, Decimal]) -> 'Money':
        """Multiply Money by a factor."""
        return Money(self.value * Decimal(str(factor)), self.currency)

    def is_positive(self) -> bool:
        """Check if the amount is positive."""
        return self.value > 0

    def is_negative(self) -> bool:
        """Check if the amount is negative."""
        return self.value < 0

    def is_zero(self) -> bool:
        """Check if the amount is zero."""
        return self.value == 0

    def __str__(self) -> str:
        """String representation of Money."""
        return f"{self.currency.value} {self.value}"

    def __eq__(self, other: object) -> bool:
        """Equality comparison."""
        if not isinstance(other, Money):
            return NotImplemented
        return self.value == other.value and self.currency == other.currency

    def __lt__(self, other: 'Money') -> bool:
        """Less than comparison."""
        if self.currency != other.currency:
            raise ValueError("Cannot compare different currencies")
        return self.value < other.value

    def __le__(self, other: 'Money') -> bool:
        """Less than or equal comparison."""
        if self.currency != other.currency:
            raise ValueError("Cannot compare different currencies")
        return self.value <= other.value

    def __gt__(self, other: 'Money') -> bool:
        """Greater than comparison."""
        if self.currency != other.currency:
            raise ValueError("Cannot compare different currencies")
        return self.value > other.value

    def __ge__(self, other: 'Money') -> bool:
        """Greater than or equal comparison."""
        if self.currency != other.currency:
            raise ValueError("Cannot compare different currencies")
        return self.value >= other.value
