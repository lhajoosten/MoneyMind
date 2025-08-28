"""User repository interface."""

from abc import ABC, abstractmethod
from typing import Optional, Protocol

from app.domain.entities.user import User
from app.domain.value_objects.user_id import UserId


class IUserRepository(Protocol):
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
