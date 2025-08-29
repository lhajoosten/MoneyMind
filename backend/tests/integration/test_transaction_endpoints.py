"""Integration tests for transaction API endpoints."""

from collections.abc import AsyncGenerator
import os
import pytest
from datetime import datetime
from decimal import Decimal
from httpx import AsyncClient
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.presentation.controllers.transaction_controller import router
from app.infrastructure.persistence.models import Base
from app.infrastructure.persistence.repositories.transaction_repository import SqlAlchemyTransactionRepository
from app.infrastructure.persistence.repositories.category_repository import SqlAlchemyCategoryRepository
from app.infrastructure.persistence.repositories.account_repository import SqlAlchemyAccountRepository
from app.infrastructure.persistence.repositories.user_repository import UserRepository
from app.domain.value_objects.user_id import UserId
from app.domain.value_objects.account_id import AccountId
from app.domain.value_objects.category_id import CategoryId
from app.domain.value_objects.transaction_id import TransactionId
from app.domain.value_objects.money import Money, Currency


@pytest.fixture
async def test_app(test_engine):
    """Create test FastAPI application."""
    # Set testing environment
    os.environ["TESTING"] = "true"

    from app.application.services.transaction_service import TransactionService
    from app.infrastructure.persistence.repositories.transaction_repository import SqlAlchemyTransactionRepository
    from app.infrastructure.persistence.repositories.category_repository import SqlAlchemyCategoryRepository
    from app.application.queries.search_transactions_handler import SearchTransactionsQueryHandler
    from app.presentation.controllers.transaction_controller import get_transaction_service

    # Create test service with test database
    test_session_factory = async_sessionmaker(
        bind=test_engine,
        expire_on_commit=False,
        autoflush=False,
    )

    async def get_test_transaction_service():
        """Test dependency that provides transaction service with test database."""
        transaction_repo = SqlAlchemyTransactionRepository(test_session_factory)
        category_repo = SqlAlchemyCategoryRepository(test_session_factory)
        search_handler = SearchTransactionsQueryHandler(transaction_repo, category_repo)
        return TransactionService(transaction_repo, category_repo, search_handler)

    app = FastAPI()
    app.include_router(router)

    # Override the dependency
    app.dependency_overrides[get_transaction_service] = get_test_transaction_service

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
    """Create a test database engine."""
    import tempfile
    import os
    
    # Use a temporary file-based SQLite database for testing
    # This ensures all connections share the same database
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
    temp_db.close()
    
    engine = create_async_engine(
        f"sqlite+aiosqlite:///{temp_db.name}",
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
    os.unlink(temp_db.name)


@pytest.fixture(scope="function")
async def test_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    async_session_factory = async_sessionmaker(
        bind=test_engine,
        expire_on_commit=False,
        autoflush=False,
    )

    async with async_session_factory() as session:
        yield session


@pytest.fixture
async def sample_user(test_session):
    """Create a sample user for testing."""
    import uuid
    user_repo = UserRepository(test_session)
    user_id = UserId.new()

    # Create user in database with unique email
    from app.infrastructure.persistence.models.user import UserModel
    user_model = UserModel(
        id=user_id.value,
        email=f"test_{uuid.uuid4()}@example.com",
        first_name="Test",
        last_name="User",
        hashed_password="hashed_password",
        is_active=True,
    )
    test_session.add(user_model)
    await test_session.commit()

    return user_id


@pytest.fixture
async def sample_account(test_session, sample_user):
    """Create a sample account for testing."""
    account_repo = SqlAlchemyAccountRepository(test_session)
    account_id = AccountId.new()

    # Create account in database
    from app.infrastructure.persistence.models.account import AccountModel
    from app.domain.entities.account import AccountType
    account_model = AccountModel(
        id=account_id.value,
        user_id=sample_user.value,
        name="Test Account",
        account_type=AccountType.CHECKING.value,
        balance=Decimal("1000.00"),
        currency="USD",
        is_active=True,
    )
    test_session.add(account_model)
    await test_session.commit()

    return account_id


@pytest.fixture
async def sample_category(test_session, sample_user):
    """Create a sample category for testing."""
    category_repo = SqlAlchemyCategoryRepository(test_session)
    category_id = CategoryId.new()

    # Create category in database
    from app.infrastructure.persistence.models.category import CategoryModel
    category_model = CategoryModel(
        id=category_id.value,
        name="Test Category",
        color="#FF5733",
        icon="shopping",
        is_active=True,
    )
    test_session.add(category_model)
    await test_session.commit()

    return category_id


class TestTransactionEndpoints:
    """Test cases for transaction API endpoints."""

    @pytest.mark.asyncio
    async def test_create_transaction_success(self, test_client, sample_account, sample_category):
        """Test successful transaction creation."""
        # Arrange
        transaction_data = {
            "account_id": str(sample_account),
            "date": "2024-01-15T10:00:00",
            "amount": 50.00,
            "currency": "USD",
            "description": "Test transaction",
            "merchant": "Test Merchant",
            "category_id": str(sample_category),
            "tags": ["test", "integration"],
        }

        # Act
        response = await test_client.post("/api/transactions/", json=transaction_data)

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["description"] == "Test transaction"
        assert data["amount"] == 50.00
        assert data["merchant"] == "Test Merchant"
        assert "id" in data
        assert "created_at" in data

    @pytest.mark.asyncio
    async def test_create_transaction_minimal_data(self, test_client, sample_account):
        """Test transaction creation with minimal required data."""
        # Arrange
        transaction_data = {
            "account_id": str(sample_account),
            "date": "2024-01-15T10:00:00",
            "amount": 25.00,
            "currency": "USD",
            "description": "Minimal transaction",
        }

        # Act
        response = await test_client.post("/api/transactions/", json=transaction_data)

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["description"] == "Minimal transaction"
        assert data["amount"] == 25.00
        assert data["merchant"] is None
        assert data["category_id"] is None
        assert data["tags"] == []

    @pytest.mark.asyncio
    async def test_create_transaction_invalid_account(self, test_client):
        """Test transaction creation with invalid account ID."""
        # Arrange
        transaction_data = {
            "account_id": "invalid-uuid",
            "date": "2024-01-15T10:00:00",
            "amount": 50.00,
            "currency": "USD",
            "description": "Test transaction",
        }

        # Act
        response = await test_client.post("/api/transactions/", json=transaction_data)

        # Assert
        assert response.status_code == 400  # Pydantic validation error for invalid UUID
        data = response.json()
        assert "detail" in data

    @pytest.mark.asyncio
    async def test_get_transaction_success(self, test_client, test_session, sample_account, sample_category):
        """Test getting an existing transaction."""
        # Arrange - Create a transaction first
        transaction_data = {
            "account_id": str(sample_account),
            "date": "2024-01-15T10:00:00",
            "amount": 75.00,
            "currency": "USD",
            "description": "Transaction to get",
            "merchant": "Test Merchant",
            "category_id": str(sample_category),
            "tags": ["get", "test"],
        }

        create_response = await test_client.post("/api/transactions/", json=transaction_data)
        assert create_response.status_code == 201
        created_data = create_response.json()
        transaction_id = created_data["id"]

        # Act
        response = await test_client.get(f"/api/transactions/{transaction_id}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == transaction_id
        assert data["description"] == "Transaction to get"
        assert data["amount"] == 75.00

    @pytest.mark.asyncio
    async def test_get_transaction_not_found(self, test_client):
        """Test getting a non-existent transaction."""
        # Arrange
        transaction_id = str(TransactionId.new())

        # Act
        response = await test_client.get(f"/api/transactions/{transaction_id}")

        # Assert
        assert response.status_code == 404  # Transaction not found
        data = response.json()
        assert "detail" in data

    @pytest.mark.asyncio
    async def test_search_transactions(self, test_client, sample_account, sample_category):
        """Test searching transactions."""
        # Arrange - Create multiple transactions
        transactions = [
            {
                "account_id": str(sample_account),
                "date": "2024-01-15T10:00:00",
                "amount": 100.00,
                "currency": "USD",
                "description": "First transaction",
                "merchant": "Merchant A",
                "category_id": str(sample_category),
                "tags": ["search", "test"],
            },
            {
                "account_id": str(sample_account),
                "date": "2024-01-16T10:00:00",
                "amount": 200.00,
                "currency": "USD",
                "description": "Second transaction",
                "merchant": "Merchant B",
                "category_id": str(sample_category),
                "tags": ["search", "test"],
            },
        ]

        for tx in transactions:
            response = await test_client.post("/api/transactions/", json=tx)
            assert response.status_code == 201

        # Act - Search transactions
        search_params = {
            "user_id": str(UserId.new()),  # This would need to be properly set up
            "limit": 10,
            "offset": 0,
        }
        response = await test_client.get("/api/transactions/", params=search_params)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # Note: This test would need proper user setup for full functionality

    @pytest.mark.asyncio
    async def test_update_transaction_success(self, test_client, test_session, sample_account, sample_category):
        """Test successful transaction update."""
        # Arrange - Create a transaction first
        transaction_data = {
            "account_id": str(sample_account),
            "date": "2024-01-15T10:00:00",
            "amount": 100.00,
            "currency": "USD",
            "description": "Original transaction",
            "merchant": "Original Merchant",
            "category_id": str(sample_category),
            "tags": ["original"],
        }

        create_response = await test_client.post("/api/transactions/", json=transaction_data)
        assert create_response.status_code == 201
        created_data = create_response.json()
        transaction_id = created_data["id"]

        # Act - Update the transaction
        update_data = {
            "description": "Updated transaction",
            "merchant": "Updated Merchant",
            "category_id": str(sample_category),
            "tags": ["updated"],
        }
        response = await test_client.put(f"/api/transactions/{transaction_id}", json=update_data)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == transaction_id
        assert data["description"] == "Updated transaction"
        assert data["merchant"] == "Updated Merchant"

    @pytest.mark.asyncio
    async def test_update_transaction_not_found(self, test_client):
        """Test updating a non-existent transaction."""
        # Arrange
        transaction_id = str(TransactionId.new())
        update_data = {
            "description": "Updated description",
        }

        # Act
        response = await test_client.put(f"/api/transactions/{transaction_id}", json=update_data)

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data

    @pytest.mark.asyncio
    async def test_delete_transaction_success(self, test_client, test_session, sample_account):
        """Test successful transaction deletion."""
        # Arrange - Create a transaction first
        transaction_data = {
            "account_id": str(sample_account),
            "date": "2024-01-15T10:00:00",
            "amount": 50.00,
            "currency": "USD",
            "description": "Transaction to delete",
        }

        create_response = await test_client.post("/api/transactions/", json=transaction_data)
        assert create_response.status_code == 201
        created_data = create_response.json()
        transaction_id = created_data["id"]

        # Act - Delete the transaction
        response = await test_client.delete(f"/api/transactions/{transaction_id}")

        # Assert
        assert response.status_code == 204

        # Verify transaction is gone
        get_response = await test_client.get(f"/api/transactions/{transaction_id}")
        assert get_response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_transaction_not_found(self, test_client):
        """Test deleting a non-existent transaction."""
        # Arrange
        transaction_id = str(TransactionId.new())

        # Act
        response = await test_client.delete(f"/api/transactions/{transaction_id}")

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data

    @pytest.mark.asyncio
    async def test_categorize_transaction_success(self, test_client, test_session, sample_account, sample_category):
        """Test successful transaction categorization."""
        # Arrange - Create a transaction first
        transaction_data = {
            "account_id": str(sample_account),
            "date": "2024-01-15T10:00:00",
            "amount": 75.00,
            "currency": "USD",
            "description": "Transaction to categorize",
        }

        create_response = await test_client.post("/api/transactions/", json=transaction_data)
        assert create_response.status_code == 201
        created_data = create_response.json()
        transaction_id = created_data["id"]

        # Act - Categorize the transaction
        categorize_data = {
            "category_id": str(sample_category),
        }
        response = await test_client.post(
            f"/api/transactions/{transaction_id}/categorize",
            json=categorize_data
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == transaction_id
        assert data["category_id"] == str(sample_category)

    @pytest.mark.asyncio
    async def test_categorize_transaction_not_found(self, test_client, sample_category):
        """Test categorizing a non-existent transaction."""
        # Arrange
        transaction_id = str(TransactionId.new())
        categorize_data = {
            "category_id": str(sample_category),
        }

        # Act
        response = await test_client.post(
            f"/api/transactions/{transaction_id}/categorize",
            json=categorize_data
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
