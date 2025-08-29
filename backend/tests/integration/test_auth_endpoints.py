"""Integration tests for authentication API endpoints."""

import os
import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.presentation.controllers.auth_controller import router, get_auth_service
from app.infrastructure.persistence.models import Base
from app.infrastructure.persistence.repositories.user_repository import UserRepository
from app.infrastructure.auth_service import AuthService


@pytest.fixture
async def test_app(test_engine):
    """Create test FastAPI application."""
    # Set testing environment
    os.environ["TESTING"] = "true"
    
    app = FastAPI()
    app.include_router(router)
    
    # Override the database engine for testing
    from app.infrastructure.persistence import database
    database.engine = test_engine
    database.async_session_factory = async_sessionmaker(
        bind=test_engine,
        expire_on_commit=False,
        autoflush=False,
    )
    
    return app


@pytest.fixture
async def test_client(test_app):
    """Create test HTTP client."""
    from httpx import ASGITransport

    async with AsyncClient(
        transport=ASGITransport(app=test_app), base_url="http://testserver"
    ) as client:
        yield client


@pytest.fixture(scope="session")
async def test_engine():
    """Create test database engine."""
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
    await engine.dispose()


@pytest.fixture(scope="function")
async def test_session(test_engine):
    """Create test database session."""
    async_session_factory = async_sessionmaker(test_engine, expire_on_commit=False)

    async with async_session_factory() as session:
        yield session
        await session.rollback()


@pytest.fixture
async def auth_service(test_session):
    """Create auth service for testing."""
    user_repository = UserRepository(test_session)
    return AuthService(user_repository=user_repository, secret_key="test-secret-key")


class TestAuthEndpoints:
    """Integration tests for authentication endpoints."""

    @pytest.mark.asyncio
    async def test_register_success(self, test_client):
        """Test successful user registration."""
        user_data = {
            "email": "test@example.com",
            "password": "TestPassword123!",
            "first_name": "Test",
            "last_name": "User",
        }

        response = await test_client.post("/auth/register", json=user_data)

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["first_name"] == "Test"
        assert data["last_name"] == "User"
        assert data["is_active"] is True
        assert "id" in data
        assert "full_name" in data

    @pytest.mark.asyncio
    async def test_register_duplicate_email(self, test_client):
        """Test registration with duplicate email."""
        user_data = {
            "email": "duplicate@example.com",
            "password": "TestPassword123!",
            "first_name": "Test",
            "last_name": "User",
        }

        # First registration should succeed
        response1 = await test_client.post("/auth/register", json=user_data)
        assert response1.status_code == 200

        # Second registration should fail
        response2 = await test_client.post("/auth/register", json=user_data)
        assert response2.status_code == 400
        assert "already exists" in response2.json()["detail"]

    @pytest.mark.asyncio
    async def test_register_invalid_data(self, test_client):
        """Test registration with invalid data."""
        invalid_data = {
            "email": "invalid-email",
            "password": "short",
            "first_name": "",
            "last_name": "",
        }

        response = await test_client.post("/auth/register", json=invalid_data)
        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_login_success(self, test_client):
        """Test successful user login."""
        # First register a user
        user_data = {
            "email": "login@example.com",
            "password": "LoginPassword123!",
            "first_name": "Login",
            "last_name": "Test",
        }
        await test_client.post("/auth/register", json=user_data)

        # Then login
        login_data = {"username": "login@example.com", "password": "LoginPassword123!"}

        response = await test_client.post("/auth/login", data=login_data)

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_login_wrong_password(self, test_client):
        """Test login with wrong password."""
        # First register a user
        user_data = {
            "email": "wrongpass@example.com",
            "password": "CorrectPassword123!",
            "first_name": "Wrong",
            "last_name": "Pass",
        }
        await test_client.post("/auth/register", json=user_data)

        # Try to login with wrong password
        login_data = {
            "username": "wrongpass@example.com",
            "password": "WrongPassword123!",
        }

        response = await test_client.post("/auth/login", data=login_data)

        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_login_nonexistent_user(self, test_client):
        """Test login with nonexistent user."""
        login_data = {
            "username": "nonexistent@example.com",
            "password": "SomePassword123!",
        }

        response = await test_client.post("/auth/login", data=login_data)

        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_get_current_user_success(self, test_client):
        """Test getting current user with valid token."""
        # Register and login to get token
        user_data = {
            "email": "current@example.com",
            "password": "CurrentPassword123!",
            "first_name": "Current",
            "last_name": "User",
        }
        await test_client.post("/auth/register", json=user_data)

        login_data = {
            "username": "current@example.com",
            "password": "CurrentPassword123!",
        }
        login_response = await test_client.post("/auth/login", data=login_data)
        token = login_response.json()["access_token"]

        # Get current user
        headers = {"Authorization": f"Bearer {token}"}
        response = await test_client.get("/auth/me", headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "current@example.com"
        assert data["first_name"] == "Current"
        assert data["last_name"] == "User"

    @pytest.mark.asyncio
    async def test_get_current_user_invalid_token(self, test_client):
        """Test getting current user with invalid token."""
        headers = {"Authorization": "Bearer invalid.token.here"}
        response = await test_client.get("/auth/me", headers=headers)

        assert response.status_code == 401
        assert "Invalid authentication credentials" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_get_current_user_no_token(self, test_client):
        """Test getting current user without token."""
        response = await test_client.get("/auth/me")

        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_logout(self, test_client):
        """Test logout endpoint."""
        response = await test_client.post("/auth/logout")

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Successfully logged out"
