"""Test configuration and shared fixtures."""

import asyncio
import pytest
import pytest_asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.infrastructure.persistence.models import Base
from app.infrastructure.persistence.repositories.user_repository import UserRepository
from app.infrastructure.auth_service import AuthService


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    """Create a test database engine."""
    # Use SQLite for testing (in-memory)
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Cleanup
    await engine.dispose()


@pytest.fixture(scope="function")
async def test_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    async_session = async_sessionmaker(test_engine, expire_on_commit=False)

    async with async_session.begin() as session:
        yield session
        await session.rollback()


@pytest.fixture(scope="function")
async def user_repository(test_engine) -> UserRepository:
    """Create a user repository instance for testing."""
    async_session = async_sessionmaker(test_engine, expire_on_commit=False)
    return UserRepository(async_session)


@pytest.fixture(scope="function")
async def auth_service(user_repository) -> AuthService:
    """Create an auth service instance for testing."""
    return AuthService(
        user_repository=user_repository, secret_key="test-secret-key-for-testing-only"
    )


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "password": "TestPassword123!",
        "first_name": "Test",
        "last_name": "User",
    }


@pytest.fixture
def sample_user_data_2():
    """Another sample user data for testing."""
    return {
        "email": "test2@example.com",
        "password": "AnotherPassword123!",
        "first_name": "Another",
        "last_name": "User",
    }
