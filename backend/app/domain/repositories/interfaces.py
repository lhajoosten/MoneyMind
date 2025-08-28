"""Repository interfaces for domain entities."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional, Protocol
from uuid import UUID

from ..entities.account import Account
from ..entities.budget import Budget
from ..entities.category import Category
from ..entities.transaction import Transaction
from ..entities.user import User
from ..value_objects.account_id import AccountId
from ..value_objects.budget_id import BudgetId
from ..value_objects.category_id import CategoryId
from ..value_objects.transaction_id import TransactionId
from ..value_objects.user_id import UserId


class TransactionRepository(Protocol):
    """Repository interface for Transaction entities."""

    @abstractmethod
    async def get_by_id(self, transaction_id: TransactionId) -> Optional[Transaction]:
        """Get transaction by ID."""
        ...

    @abstractmethod
    async def get_by_account(self, account_id: AccountId) -> List[Transaction]:
        """Get all transactions for an account."""
        ...

    @abstractmethod
    async def save(self, transaction: Transaction) -> None:
        """Save a transaction."""
        ...

    @abstractmethod
    async def delete(self, transaction_id: TransactionId) -> None:
        """Delete a transaction."""
        ...


class CategoryRepository(Protocol):
    """Repository interface for Category entities."""

    @abstractmethod
    async def get_by_id(self, category_id: CategoryId) -> Optional[Category]:
        """Get category by ID."""
        ...

    @abstractmethod
    async def get_all_active(self) -> List[Category]:
        """Get all active categories."""
        ...

    @abstractmethod
    async def get_by_parent(self, parent_id: CategoryId) -> List[Category]:
        """Get subcategories for a parent category."""
        ...

    @abstractmethod
    async def save(self, category: Category) -> None:
        """Save a category."""
        ...

    @abstractmethod
    async def delete(self, category_id: CategoryId) -> None:
        """Delete a category."""
        ...


class AccountRepository(Protocol):
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


class BudgetRepository(Protocol):
    """Repository interface for Budget entities."""

    @abstractmethod
    async def get_by_id(self, budget_id: BudgetId) -> Optional[Budget]:
        """Get budget by ID."""
        ...

    @abstractmethod
    async def get_by_user(self, user_id: UserId) -> List[Budget]:
        """Get all budgets for a user."""
        ...

    @abstractmethod
    async def get_active_for_date(self, user_id: UserId, date: datetime) -> List[Budget]:
        """Get active budgets for a user on a specific date."""
        ...

    @abstractmethod
    async def save(self, budget: Budget) -> None:
        """Save a budget."""
        ...

    @abstractmethod
    async def delete(self, budget_id: BudgetId) -> None:
        """Delete a budget."""
        ...


class UserRepository(Protocol):
    """Repository interface for User entities."""

    @abstractmethod
    async def get_by_id(self, user_id: UserId) -> Optional[User]:
        """Get user by ID."""
        ...

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        ...

    @abstractmethod
    async def save(self, user: User) -> None:
        """Save a user."""
        ...

    @abstractmethod
    async def delete(self, user_id: UserId) -> None:
        """Delete a user."""
        ...
