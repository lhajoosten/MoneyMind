"""User repository for database operations."""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.domain.entities.user import User
from app.domain.repositories.user_repository import IUserRepository
from app.domain.value_objects.user_id import UserId
from app.infrastructure.persistence.models.user import UserModel


class UserRepository(IUserRepository):
    """Repository for User entity operations."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        """Initialize repository with session factory."""
        self.session_factory = session_factory

    async def get_by_id(self, user_id: UserId) -> Optional[User]:
        """Get user by ID."""
        async with self.session_factory() as session:
            result = await session.execute(
                select(UserModel).where(UserModel.id == user_id.value)
            )
            user_model = result.scalar_one_or_none()
            return user_model.to_domain() if user_model else None

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        async with self.session_factory() as session:
            result = await session.execute(
                select(UserModel).where(UserModel.email == email)
            )
            user_model = result.scalar_one_or_none()
            return user_model.to_domain() if user_model else None

    async def save(self, user: User) -> None:
        """Save a user."""
        user_model = UserModel.from_domain(user)
        async with self.session_factory() as session:
            # Check if user already exists
            existing = await session.execute(
                select(UserModel).where(UserModel.id == user.id.value)
            )
            existing_user = existing.scalar_one_or_none()
            
            if existing_user:
                # Update existing user
                await session.merge(user_model)
            else:
                # Create new user
                session.add(user_model)
            
            await session.commit()
            if not existing_user:
                await session.refresh(user_model)

    async def delete(self, user_id: UserId) -> None:
        """Delete a user by ID."""
        async with self.session_factory() as session:
            result = await session.execute(
                select(UserModel).where(UserModel.id == user_id.value)
            )
            user_model = result.scalar_one_or_none()
            if user_model:
                await session.delete(user_model)
                await session.commit()
