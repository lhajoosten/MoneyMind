"""Unit tests for AuthService."""

import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, timedelta

from app.infrastructure.auth_service import AuthService
from app.domain.entities.user import User
from app.domain.value_objects.user_id import UserId


class TestAuthService:
    """Test cases for AuthService."""

    @pytest.fixture
    def mock_user_repository(self):
        """Mock user repository."""
        return AsyncMock()

    @pytest.fixture
    def auth_service(self, mock_user_repository):
        """Create AuthService instance for testing."""
        return AuthService(
            user_repository=mock_user_repository,
            secret_key="test-secret-key",
            access_token_expire_minutes=30,
        )

    @pytest.fixture
    def sample_user(self):
        """Create a sample user for testing."""
        user_id = UserId.new()
        user = User(
            id=user_id,
            email="test@example.com",
            first_name="Test",
            last_name="User",
            hashed_password=None,
            is_active=True,
        )
        user.set_password("TestPassword123!")
        return user

    def test_init(self, mock_user_repository):
        """Test AuthService initialization."""
        service = AuthService(
            user_repository=mock_user_repository,
            secret_key="secret",
            algorithm="HS256",
            access_token_expire_minutes=60,
        )

        assert service.user_repository == mock_user_repository
        assert service.secret_key == "secret"
        assert service.algorithm == "HS256"
        assert service.access_token_expire_minutes == 60

    def test_init_defaults(self, mock_user_repository):
        """Test AuthService initialization with defaults."""
        service = AuthService(user_repository=mock_user_repository, secret_key="secret")

        assert service.algorithm == "HS256"
        assert service.access_token_expire_minutes == 30

    @pytest.mark.asyncio
    async def test_authenticate_user_success(
        self, auth_service, mock_user_repository, sample_user
    ):
        """Test successful user authentication."""
        # Setup
        mock_user_repository.get_by_email.return_value = sample_user

        # Execute
        result = await auth_service.authenticate_user(
            "test@example.com", "TestPassword123!"
        )

        # Assert
        assert result == sample_user
        mock_user_repository.get_by_email.assert_called_once_with("test@example.com")

    @pytest.mark.asyncio
    async def test_authenticate_user_user_not_found(
        self, auth_service, mock_user_repository
    ):
        """Test authentication when user is not found."""
        # Setup
        mock_user_repository.get_by_email.return_value = None

        # Execute
        result = await auth_service.authenticate_user(
            "nonexistent@example.com", "password"
        )

        # Assert
        assert result is None
        mock_user_repository.get_by_email.assert_called_once_with(
            "nonexistent@example.com"
        )

    @pytest.mark.asyncio
    async def test_authenticate_user_wrong_password(
        self, auth_service, mock_user_repository, sample_user
    ):
        """Test authentication with wrong password."""
        # Setup
        mock_user_repository.get_by_email.return_value = sample_user

        # Execute
        result = await auth_service.authenticate_user(
            "test@example.com", "WrongPassword"
        )

        # Assert
        assert result is None
        mock_user_repository.get_by_email.assert_called_once_with("test@example.com")

    @pytest.mark.asyncio
    async def test_create_user_success(self, auth_service, mock_user_repository):
        """Test successful user creation."""
        # Setup
        mock_user_repository.get_by_email.return_value = None
        mock_user_repository.save.return_value = None

        # Execute
        result = await auth_service.create_user(
            email="new@example.com",
            password="NewPassword123!",
            first_name="New",
            last_name="User",
        )

        # Assert
        assert result.email == "new@example.com"
        assert result.first_name == "New"
        assert result.last_name == "User"
        assert result.is_active is True
        assert result.hashed_password is not None
        assert result.verify_password("NewPassword123!") is True

        mock_user_repository.get_by_email.assert_called_once_with("new@example.com")
        mock_user_repository.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_user_already_exists(
        self, auth_service, mock_user_repository, sample_user
    ):
        """Test user creation when user already exists."""
        # Setup
        mock_user_repository.get_by_email.return_value = sample_user

        # Execute & Assert
        with pytest.raises(ValueError, match="User with this email already exists"):
            await auth_service.create_user(
                email="test@example.com",
                password="Password123!",
                first_name="Test",
                last_name="User",
            )

        mock_user_repository.get_by_email.assert_called_once_with("test@example.com")
        mock_user_repository.save.assert_not_called()

    def test_create_access_token(self, auth_service):
        """Test JWT access token creation."""
        # Setup
        data = {"sub": "user123", "custom": "data"}

        # Execute
        token = auth_service.create_access_token(data)

        # Assert
        assert isinstance(token, str)
        assert len(token) > 0

        # Verify token contains expected data
        decoded = auth_service.verify_token(token)
        assert decoded == "user123"

    def test_verify_token_valid(self, auth_service):
        """Test valid JWT token verification."""
        # Setup
        data = {"sub": "user123"}
        token = auth_service.create_access_token(data)

        # Execute
        result = auth_service.verify_token(token)

        # Assert
        assert result == "user123"

    def test_verify_token_invalid(self, auth_service):
        """Test invalid JWT token verification."""
        # Execute
        result = auth_service.verify_token("invalid.token.here")

        # Assert
        assert result is None

    def test_verify_token_no_sub(self, auth_service):
        """Test JWT token verification with no subject."""
        # Setup
        data = {"custom": "data"}  # No 'sub' field
        token = auth_service.create_access_token(data)

        # Execute
        result = auth_service.verify_token(token)

        # Assert
        assert result is None

    def test_verify_token_expired(self, auth_service):
        """Test expired JWT token verification."""
        # Setup - create token that expires immediately
        expired_service = AuthService(
            user_repository=AsyncMock(),
            secret_key="test-secret",
            access_token_expire_minutes=-1,  # Already expired
        )
        data = {"sub": "user123"}
        token = expired_service.create_access_token(data)

        # Execute
        result = auth_service.verify_token(token)

        # Assert
        assert result is None

    @pytest.mark.asyncio
    async def test_get_current_user_success(
        self, auth_service, mock_user_repository, sample_user
    ):
        """Test successful current user retrieval."""
        # Setup
        data = {"sub": str(sample_user.id)}
        token = auth_service.create_access_token(data)
        mock_user_repository.get_by_id.return_value = sample_user

        # Execute
        result = await auth_service.get_current_user(token)

        # Assert
        assert result == sample_user
        mock_user_repository.get_by_id.assert_called_once_with(sample_user.id)

    @pytest.mark.asyncio
    async def test_get_current_user_invalid_token(
        self, auth_service, mock_user_repository
    ):
        """Test current user retrieval with invalid token."""
        # Execute
        result = await auth_service.get_current_user("invalid.token")

        # Assert
        assert result is None
        mock_user_repository.get_by_id.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_current_user_user_not_found(
        self, auth_service, mock_user_repository, sample_user
    ):
        """Test current user retrieval when user is not found."""
        # Setup
        data = {"sub": str(sample_user.id)}
        token = auth_service.create_access_token(data)
        mock_user_repository.get_by_id.return_value = None

        # Execute
        result = await auth_service.get_current_user(token)

        # Assert
        assert result is None
        mock_user_repository.get_by_id.assert_called_once_with(sample_user.id)
