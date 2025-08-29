"""Unit tests for authentication controller."""

import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.presentation.controllers.auth_controller import router
from app.application.dtos.auth_dto import (
    UserCreateRequest,
    UserLoginRequest,
    UserResponse,
    TokenResponse,
)
from app.domain.entities.user import User
from app.domain.value_objects.user_id import UserId


@pytest.fixture
def test_app(mock_auth_service):
    """Create test FastAPI application."""
    from app.presentation.controllers.auth_controller import get_auth_service
    
    app = FastAPI()
    app.include_router(router)
    
    # Override the dependency
    app.dependency_overrides[get_auth_service] = lambda: mock_auth_service
    
    return app


@pytest.fixture
def test_client(test_app):
    """Create test client."""
    return TestClient(test_app)


@pytest.fixture
def mock_auth_service():
    """Create mock auth service."""
    service = AsyncMock()

    # Mock user creation
    mock_user = User(
        id=UserId.new(),
        email="test@example.com",
        first_name="Test",
        last_name="User",
        is_active=True,
    )
    service.create_user.return_value = mock_user
    service.authenticate_user.return_value = mock_user
    # create_access_token is a synchronous method, so use regular MagicMock
    service.create_access_token = MagicMock(return_value="mock.jwt.token")
    service.get_current_user.return_value = mock_user

    return service


@pytest.fixture
def mock_user_repository():
    """Create mock user repository."""
    repo = AsyncMock()
    return repo


class TestAuthController:
    """Unit tests for authentication controller."""

    def test_register_success(self, test_client, mock_auth_service):
        """Test successful user registration."""
        user_data = {
            "email": "test@example.com",
            "password": "TestPassword123!",
            "first_name": "Test",
            "last_name": "User",
        }

        response = test_client.post("/auth/register", json=user_data)

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["first_name"] == "Test"
        assert data["last_name"] == "User"
        assert data["is_active"] is True
        mock_auth_service.create_user.assert_called_once()

    def test_register_service_error(self, test_client, mock_auth_service):
        """Test registration with service error."""
        # Mock service to raise exception
        mock_auth_service.create_user.side_effect = ValueError("User already exists")

        user_data = {
            "email": "existing@example.com",
            "password": "TestPassword123!",
            "first_name": "Existing",
            "last_name": "User",
        }

        response = test_client.post("/auth/register", json=user_data)

        assert response.status_code == 400
        assert "User already exists" in response.json()["detail"]

    def test_login_success(self, test_client, mock_auth_service):
        """Test successful user login."""
        login_data = {"username": "test@example.com", "password": "TestPassword123!"}

        response = test_client.post("/auth/login", data=login_data)

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        mock_auth_service.authenticate_user.assert_called_once()
        mock_auth_service.create_access_token.assert_called_once()

    def test_login_invalid_credentials(self, test_client, mock_auth_service):
        """Test login with invalid credentials."""
        # Mock service to raise HTTPException
        mock_auth_service.authenticate_user.side_effect = HTTPException(
            status_code=401, detail="Incorrect email or password"
        )

        login_data = {"username": "test@example.com", "password": "WrongPassword123!"}

        response = test_client.post("/auth/login", data=login_data)

        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]

    def test_get_current_user_success(self, test_client, mock_auth_service):
        """Test getting current user with valid token."""
        headers = {"Authorization": "Bearer valid.jwt.token"}

        response = test_client.get("/auth/me", headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["first_name"] == "Test"
        assert data["last_name"] == "User"
        mock_auth_service.get_current_user.assert_called_once()

    def test_get_current_user_invalid_token(self, test_client, mock_auth_service):
        """Test getting current user with invalid token."""
        # Mock service to raise HTTPException
        mock_auth_service.get_current_user.side_effect = HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )

        headers = {"Authorization": "Bearer invalid.jwt.token"}

        response = test_client.get("/auth/me", headers=headers)

        assert response.status_code == 401
        assert "Invalid authentication credentials" in response.json()["detail"]

    def test_get_current_user_no_token(self, test_client, mock_auth_service):
        """Test getting current user without token."""
        response = test_client.get("/auth/me")

        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]

    def test_logout(self, test_client):
        """Test logout endpoint."""
        response = test_client.post("/auth/logout")

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Successfully logged out"

    def test_register_invalid_email(self, test_client, mock_auth_service):
        """Test registration with invalid email format."""
        user_data = {
            "email": "invalid-email",
            "password": "TestPassword123!",
            "first_name": "Test",
            "last_name": "User",
        }

        response = test_client.post("/auth/register", json=user_data)

        # Should fail validation before reaching service
        assert response.status_code == 422

    def test_register_weak_password(self, test_client, mock_auth_service):
        """Test registration with weak password."""
        user_data = {
            "email": "test@example.com",
            "password": "weak",
            "first_name": "Test",
            "last_name": "User",
        }

        response = test_client.post("/auth/register", json=user_data)

        # Should fail validation before reaching service
        assert response.status_code == 422

    def test_register_empty_names(self, test_client, mock_auth_service):
        """Test registration with empty names."""
        user_data = {
            "email": "test@example.com",
            "password": "TestPassword123!",
            "first_name": "",
            "last_name": "",
        }

        response = test_client.post("/auth/register", json=user_data)

        # Should fail validation before reaching service
        assert response.status_code == 422
