"""Account repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional, Protocol

from app.domain.entities.account import Account
from app.domain.value_objects.account_id import AccountId
from app.domain.value_objects.user_id import UserId


class IAccountRepository(Protocol):
    """Repository interface for Account entities."""

    @abstractmethod
    async def get_by_id(self, account_id: AccountId) -> Optional[Account]:
        """Get account by ID."""
        ...

    @abstractmethod
    async def get_by_user(self, user_id: UserId) -> List[Account]:
        """Get all accounts for a user."""
        ...

    @abstractmethod
    async def save(self, account: Account) -> None:
        """Save an account."""
        ...

    @abstractmethod
    async def delete(self, account_id: AccountId) -> None:
        """Delete an account."""
        ...
