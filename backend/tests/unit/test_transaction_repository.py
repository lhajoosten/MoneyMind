"""Unit tests for TransactionRepository."""

import pytest
from datetime import datetime
from decimal import Decimal
from unittest.mock import AsyncMock

from app.infrastructure.persistence.repositories.transaction_repository import SqlAlchemyTransactionRepository
from app.domain.entities.transaction import Transaction
from app.domain.value_objects.account_id import AccountId
from app.domain.value_objects.category_id import CategoryId
from app.domain.value_objects.transaction_id import TransactionId
from app.domain.value_objects.money import Money, Currency


class TestSqlAlchemyTransactionRepository:
    """Test cases for SqlAlchemyTransactionRepository."""

    @pytest.fixture
    def mock_session(self):
        """Mock database session."""
        return AsyncMock()

    @pytest.fixture
    def repository(self, mock_session):
        """Create repository with mocked session."""
        return SqlAlchemyTransactionRepository(mock_session)

    @pytest.fixture
    def sample_transaction(self):
        """Create a sample transaction for testing."""
        return Transaction(
            id=TransactionId.new(),
            account_id=AccountId.new(),
            date=datetime.now(),
            amount=Money(Decimal("100.00"), Currency.USD),
            description="Test transaction",
            merchant="Test Merchant",
            category=None,
            tags=["test", "sample"],
            created_at=datetime.now(),
        )

    @pytest.mark.asyncio
    async def test_save_transaction(self, repository, mock_session, sample_transaction):
        """Test saving a transaction."""
        # Arrange
        mock_session.add.return_value = None
        mock_session.commit.return_value = None

        # Act
        result = await repository.save(sample_transaction)

        # Assert
        assert result == sample_transaction
        mock_session.add.assert_called_once_with(sample_transaction)
        mock_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_id_found(self, repository, mock_session, sample_transaction):
        """Test getting a transaction by ID when it exists."""
        # Arrange
        transaction_id = sample_transaction.id
        mock_session.get.return_value = sample_transaction

        # Act
        result = await repository.get_by_id(transaction_id)

        # Assert
        assert result == sample_transaction
        mock_session.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, repository, mock_session):
        """Test getting a transaction by ID when it doesn't exist."""
        # Arrange
        transaction_id = TransactionId.new()
        mock_session.get.return_value = None

        # Act
        result = await repository.get_by_id(transaction_id)

        # Assert
        assert result is None
        mock_session.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_account(self, repository, mock_session, sample_transaction):
        """Test getting transactions by account."""
        # Arrange
        account_id = sample_transaction.account_id
        transactions = [sample_transaction]

        # Mock the query execution
        mock_query = AsyncMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalars.return_value = transactions

        # Act
        result = await repository.get_by_account(account_id)

        # Assert
        assert result == transactions
        mock_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_account_empty(self, repository, mock_session):
        """Test getting transactions by account when none exist."""
        # Arrange
        account_id = AccountId.new()
        transactions = []

        # Mock the query execution
        mock_query = AsyncMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalars.return_value = transactions

        # Act
        result = await repository.get_by_account(account_id)

        # Assert
        assert result == []
        mock_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_transaction(self, repository, mock_session, sample_transaction):
        """Test updating a transaction."""
        # Arrange
        mock_session.merge.return_value = sample_transaction
        mock_session.commit.return_value = None

        # Act
        result = await repository.update(sample_transaction)

        # Assert
        assert result == sample_transaction
        mock_session.merge.assert_called_once_with(sample_transaction)
        mock_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_transaction_success(self, repository, mock_session, sample_transaction):
        """Test successful transaction deletion."""
        # Arrange
        transaction_id = sample_transaction.id
        mock_session.get.return_value = sample_transaction
        mock_session.delete.return_value = None
        mock_session.commit.return_value = None

        # Act
        result = await repository.delete(transaction_id)

        # Assert
        assert result is True
        mock_session.get.assert_called_once()
        mock_session.delete.assert_called_once_with(sample_transaction)
        mock_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_transaction_not_found(self, repository, mock_session):
        """Test deleting a non-existent transaction."""
        # Arrange
        transaction_id = TransactionId.new()
        mock_session.get.return_value = None

        # Act
        result = await repository.delete(transaction_id)

        # Assert
        assert result is False
        mock_session.get.assert_called_once()
        mock_session.delete.assert_not_called()
        mock_session.commit.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_all(self, repository, mock_session, sample_transaction):
        """Test getting all transactions."""
        # Arrange
        transactions = [sample_transaction]

        # Mock the query execution
        mock_query = AsyncMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalars.return_value = transactions

        # Act
        result = await repository.get_all()

        # Assert
        assert result == transactions
        mock_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_date_range(self, repository, mock_session, sample_transaction):
        """Test getting transactions by date range."""
        # Arrange
        start_date = datetime(2024, 1, 1)
        end_date = datetime(2024, 12, 31)
        transactions = [sample_transaction]

        # Mock the query execution
        mock_query = AsyncMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalars.return_value = transactions

        # Act
        result = await repository.get_by_date_range(start_date, end_date)

        # Assert
        assert result == transactions
        mock_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_category(self, repository, mock_session, sample_transaction):
        """Test getting transactions by category."""
        # Arrange
        category_id = CategoryId.new()
        transactions = [sample_transaction]

        # Mock the query execution
        mock_query = AsyncMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalars.return_value = transactions

        # Act
        result = await repository.get_by_category(category_id)

        # Assert
        assert result == transactions
        mock_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_amount_range(self, repository, mock_session, sample_transaction):
        """Test getting transactions by amount range."""
        # Arrange
        min_amount = Money(Decimal("50.00"), Currency.USD)
        max_amount = Money(Decimal("200.00"), Currency.USD)
        transactions = [sample_transaction]

        # Mock the query execution
        mock_query = AsyncMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalars.return_value = transactions

        # Act
        result = await repository.get_by_amount_range(min_amount, max_amount)

        # Assert
        assert result == transactions
        mock_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_search_by_description(self, repository, mock_session, sample_transaction):
        """Test searching transactions by description."""
        # Arrange
        search_term = "test"
        transactions = [sample_transaction]

        # Mock the query execution
        mock_query = AsyncMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalars.return_value = transactions

        # Act
        result = await repository.search_by_description(search_term)

        # Assert
        assert result == transactions
        mock_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_merchant(self, repository, mock_session, sample_transaction):
        """Test getting transactions by merchant."""
        # Arrange
        merchant = "Test Merchant"
        transactions = [sample_transaction]

        # Mock the query execution
        mock_query = AsyncMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalars.return_value = transactions

        # Act
        result = await repository.get_by_merchant(merchant)

        # Assert
        assert result == transactions
        mock_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_tags(self, repository, mock_session, sample_transaction):
        """Test getting transactions by tags."""
        # Arrange
        tags = ["test"]
        transactions = [sample_transaction]

        # Mock the query execution
        mock_query = AsyncMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalars.return_value = transactions

        # Act
        result = await repository.get_by_tags(tags)

        # Assert
        assert result == transactions
        mock_session.execute.assert_called_once()
