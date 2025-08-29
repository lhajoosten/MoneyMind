"""Unit tests for User domain entity."""

import pytest
from app.domain.entities.user import User
from app.domain.value_objects.user_id import UserId


class TestUser:
    """Test cases for User entity."""

    def test_user_creation_success(self):
        """Test successful user creation."""
        user_id = UserId.new()
        email = "test@example.com"

        user = User(
            id=user_id,
            email=email,
            first_name="Test",
            last_name="User",
            hashed_password="hashed_password",
            is_active=True,
        )

        assert user.id == user_id
        assert user.email == email
        assert user.first_name == "Test"
        assert user.last_name == "User"
        assert user.hashed_password == "hashed_password"
        assert user.is_active is True
        assert user.full_name == "Test User"

    def test_user_creation_with_minimal_data(self):
        """Test user creation with minimal required data."""
        user_id = UserId.new()
        email = "minimal@example.com"

        user = User(
            id=user_id,
            email=email,
            first_name="Min",
            last_name="User",
            is_active=True,
            hashed_password="hash",
        )

        assert user.is_active is True  # Should default to True
        assert user.full_name == "Min User"

    def test_user_full_name_property(self):
        """Test the full_name property."""
        user_id = UserId.new()
        email = "fullname@example.com"

        user = User(
            id=user_id,
            email=email,
            first_name="John",
            last_name="Doe",
            is_active=True,
            hashed_password="hash",
        )

        assert user.full_name == "John Doe"

    def test_user_equality(self):
        """Test user equality based on ID."""
        user_id1 = UserId.new()
        user_id2 = UserId.new()
        email = "test@example.com"

        user1 = User(
            id=user_id1,
            email=email,
            first_name="Test",
            last_name="User",
            hashed_password="hash",
            is_active=True,
        )

        user2 = User(
            id=user_id1,  # Same ID
            email=email,
            first_name="Test",
            last_name="User",
            hashed_password="hash",
            is_active=True,
        )

        user3 = User(
            id=user_id2,  # Different ID
            email=email,
            first_name="Test",
            last_name="User",
            hashed_password="hash",
            is_active=True,
        )

        assert user1 == user2
        assert user1 != user3

    def test_user_hash(self):
        """Test user hash based on ID."""
        user_id1 = UserId.new()
        user_id2 = UserId.new()
        email = "test@example.com"

        user1 = User(
            id=user_id1,
            email=email,
            first_name="Test",
            last_name="User",
            hashed_password="hash",
            is_active=True,
        )

        user2 = User(
            id=user_id1,  # Same ID
            email=email,
            first_name="Test",
            last_name="User",
            hashed_password="hash",
            is_active=True,
        )

        user3 = User(
            id=user_id2,  # Different ID
            email=email,
            first_name="Test",
            last_name="User",
            hashed_password="hash",
            is_active=True,
        )

        assert hash(user1) == hash(user2)
        assert hash(user1) != hash(user3)

    def test_user_repr(self):
        """Test user string representation."""
        user_id = UserId.new()
        email = "repr@example.com"

        user = User(
            id=user_id,
            email=email,
            first_name="Repr",
            last_name="Test",
            hashed_password="hash",
            is_active=True,
        )

        repr_str = repr(user)
        assert "User" in repr_str
        assert "repr@example.com" in repr_str
        assert str(user_id) in repr_str

    def test_user_validation_empty_email(self):
        """Test user validation with empty email."""
        user_id = UserId.new()

        with pytest.raises(ValueError, match="User email cannot be empty"):
            User(
                id=user_id,
                email="",
                first_name="Test",
                last_name="User",
                hashed_password="hash",
                is_active=True,
            )

    def test_user_validation_empty_first_name(self):
        """Test user validation with empty first name."""
        user_id = UserId.new()

        with pytest.raises(ValueError, match="User first name cannot be empty"):
            User(
                id=user_id,
                email="test@example.com",
                first_name="",
                last_name="User",
                hashed_password="hash",
                is_active=True,
            )

    def test_user_validation_empty_last_name(self):
        """Test user validation with empty last name."""
        user_id = UserId.new()

        with pytest.raises(ValueError, match="User last name cannot be empty"):
            User(
                id=user_id,
                email="test@example.com",
                first_name="Test",
                last_name="",
                hashed_password="hash",
                is_active=True,
            )

    def test_set_password_success(self):
        """Test successful password setting."""
        user_id = UserId.new()
        user = User(
            id=user_id,
            email="test@example.com",
            first_name="Test",
            last_name="User",
            hashed_password=None,
            is_active=True,
        )

        user.set_password("ValidPassword123!")

        assert user.hashed_password is not None
        assert user.hashed_password != "ValidPassword123!"  # Should be hashed

    def test_set_password_too_short(self):
        """Test password setting with too short password."""
        user_id = UserId.new()
        user = User(
            id=user_id,
            email="test@example.com",
            first_name="Test",
            last_name="User",
            hashed_password=None,
            is_active=True,
        )

        with pytest.raises(
            ValueError, match="Password must be at least 8 characters long"
        ):
            user.set_password("short")

    def test_verify_password_success(self):
        """Test successful password verification."""
        user_id = UserId.new()
        user = User(
            id=user_id,
            email="test@example.com",
            first_name="Test",
            last_name="User",
            hashed_password=None,
            is_active=True,
        )

        password = "ValidPassword123!"
        user.set_password(password)

        assert user.verify_password(password) is True

    def test_verify_password_wrong(self):
        """Test password verification with wrong password."""
        user_id = UserId.new()
        user = User(
            id=user_id,
            email="test@example.com",
            first_name="Test",
            last_name="User",
            hashed_password=None,
            is_active=True,
        )

        user.set_password("ValidPassword123!")

        assert user.verify_password("WrongPassword") is False

    def test_verify_password_no_hash(self):
        """Test password verification when no hash is set."""
        user_id = UserId.new()
        user = User(
            id=user_id,
            email="test@example.com",
            first_name="Test",
            last_name="User",
            hashed_password=None,
            is_active=True,
        )

        assert user.verify_password("AnyPassword") is False
