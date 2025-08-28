"""Account domain entity."""

from dataclasses import dataclass

from .entity import Entity
from ..value_objects.account_id import AccountId
from ..value_objects.account_type import AccountType
from ..value_objects.currency import Currency
from ..value_objects.money import Money
from ..value_objects.user_id import UserId


@dataclass
class Account(Entity):
    """Domain entity representing a bank account."""
    id: AccountId
    user_id: UserId
    name: str
    account_type: AccountType
    balance: Money
    currency: Currency
    is_active: bool

    def __post_init__(self) -> None:
        """Validate the account."""
        if not self.name or not self.name.strip():
            raise ValueError("Account name cannot be empty")

    def can_withdraw(self, amount: Money) -> bool:
        """Check if withdrawal is possible."""
        return self.balance.value >= amount.value

    def deposit(self, amount: Money) -> None:
        """Deposit money into the account."""
        if not amount.is_positive():
            raise ValueError("Deposit amount must be positive")
        if self.currency != amount.currency:
            raise ValueError("Deposit currency must match account currency")
        self.balance = self.balance.add(amount)

    def withdraw(self, amount: Money) -> None:
        """Withdraw money from the account."""
        if not amount.is_positive():
            raise ValueError("Withdrawal amount must be positive")
        if self.currency != amount.currency:
            raise ValueError("Withdrawal currency must match account currency")
        if not self.can_withdraw(amount):
            raise ValueError("Insufficient funds")
        self.balance = self.balance.subtract(amount)

    def deactivate(self) -> None:
        """Deactivate the account."""
        self.is_active = False

    def activate(self) -> None:
        """Activate the account."""
        self.is_active = True
