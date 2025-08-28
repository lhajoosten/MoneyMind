"""Unit tests for UserRepository."""

import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.persistence.repositories.user_repository import UserRepository
from app.domain.entities.user import User
from app.domain.value_objects.user_id import UserId
from app.infrastructure.persistence.models.user import UserModel


class TestUserRepository:
    """Test cases for UserRepository."""

    @pytest.fixture
    def mock_session_factory(self):
        """Mock session factory."""
        from unittest.mock import AsyncMock, MagicMock

        # Create a mock that acts as an async context manager
        mock_factory = MagicMock()
        mock_session = AsyncMock(spec=AsyncSession)

        # Set up the async context manager behavior
        mock_context = MagicMock()
        mock_context.__aenter__ = AsyncMock(return_value=mock_session)
        mock_context.__aexit__ = AsyncMock(return_value=None)

        mock_factory.return_value = mock_context
        return mock_factory

    @pytest.fixture
    def mock_session(self, mock_session_factory):
        """Mock database session."""
        # Get the session from the factory's context manager
        return mock_session_factory.return_value.__aenter__.return_value

    @pytest.fixture
    def user_repository(self, mock_session_factory):
        """Create UserRepository instance for testing."""
        return UserRepository(mock_session_factory)

    @pytest.fixture
    def sample_user(self):
        """Create a sample user for testing."""
        user_id = UserId.new()
        user = User(
            id=user_id,
            email="test@example.com",
            first_name="Test",
            last_name="User",
            hashed_password="hashed_password",
            is_active=True,
        )
        return user

    @pytest.fixture
    def sample_user_model(self, sample_user):
        """Create a sample user model for testing."""
        return UserModel.from_domain(sample_user)

    def test_init(self, mock_session_factory):
        """Test UserRepository initialization."""
        repo = UserRepository(mock_session_factory)
        assert repo.session_factory == mock_session_factory

    @pytest.mark.asyncio
    async def test_get_by_id_success(
        self, user_repository, mock_session, sample_user_model
    ):
        """Test successful user retrieval by ID."""
        # Setup
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none = MagicMock(return_value=sample_user_model)
        mock_session.execute.return_value = mock_result

        # Execute
        user_id = UserId(sample_user_model.id)
        result = await user_repository.get_by_id(user_id)

        # Assert
        assert result is not None
        assert result.id.value == sample_user_model.id
        assert result.email == sample_user_model.email

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, user_repository, mock_session):
        """Test user retrieval by ID when user is not found."""
        # Setup
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none = MagicMock(return_value=None)
        mock_session.execute.return_value = mock_result

        # Execute
        user_id = UserId.new()
        result = await user_repository.get_by_id(user_id)

        # Assert
        assert result is None

    @pytest.mark.asyncio
    async def test_get_by_email_success(
        self, user_repository, mock_session, sample_user_model
    ):
        """Test successful user retrieval by email."""
        # Setup
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none = MagicMock(return_value=sample_user_model)
        mock_session.execute.return_value = mock_result

        # Execute
        result = await user_repository.get_by_email("test@example.com")

        # Assert
        assert result is not None
        assert result.email == "test@example.com"

    @pytest.mark.asyncio
    async def test_get_by_email_not_found(self, user_repository, mock_session):
        """Test user retrieval by email when user is not found."""
        # Setup
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        # Execute
        result = await user_repository.get_by_email("nonexistent@example.com")

        # Assert
        assert result is None

    @pytest.mark.asyncio
    async def test_save_new_user(self, user_repository, mock_session, sample_user):
        """Test saving a new user."""
        # Setup
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = None  # User doesn't exist
        mock_session.execute.return_value = mock_result

        # Execute
        await user_repository.save(sample_user)

        # Assert
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()

    @pytest.mark.asyncio
    async def test_save_existing_user(
        self,
        user_repository,
        mock_session,
        sample_user,
        sample_user_model,
    ):
        """Test saving an existing user (update)."""
        # Setup
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = sample_user_model  # User exists
        mock_session.execute.return_value = mock_result

        # Execute
        await user_repository.save(sample_user)

        # Assert
        mock_session.merge.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_not_called()  # No refresh for updates

    @pytest.mark.asyncio
    async def test_delete_existing_user(
        self, user_repository, mock_session, sample_user_model
    ):
        """Test deleting an existing user."""
        # Setup
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = sample_user_model
        mock_session.execute.return_value = mock_result

        # Execute
        user_id = UserId(sample_user_model.id)
        await user_repository.delete(user_id)

        # Assert
        mock_session.delete.assert_called_once_with(sample_user_model)
        mock_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_nonexistent_user(self, user_repository, mock_session):
        """Test deleting a nonexistent user."""
        # Setup
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        # Execute
        user_id = UserId.new()
        await user_repository.delete(user_id)

        # Assert
        mock_session.delete.assert_not_called()
        mock_session.commit.assert_not_called()

    @pytest.mark.asyncio
    async def test_session_context_manager(
        self, user_repository, mock_session_factory, mock_session
    ):
        """Test that session is properly used as context manager."""
        # Setup
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        # Execute
        await user_repository.get_by_email("test@example.com")

        # Assert
        mock_session_factory.assert_called_once()
        mock_session_factory.return_value.__aenter__.assert_called_once()
        mock_session_factory.return_value.__aexit__.assert_called_once()
