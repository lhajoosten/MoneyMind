"""Unit tests for transaction handlers."""

import pytest
from datetime import datetime
from decimal import Decimal
from unittest.mock import AsyncMock

from app.application.handlers.create_transaction_handler import CreateTransactionHandler
from app.application.handlers.update_transaction_handler import UpdateTransactionHandler
from app.application.handlers.delete_transaction_handler import DeleteTransactionHandler
from app.application.handlers.categorize_transaction_handler import CategorizeTransactionHandler
from app.application.commands.create_transaction import CreateTransactionCommand
from app.application.commands.update_transaction import UpdateTransactionCommand
from app.application.commands.delete_transaction import DeleteTransactionCommand
from app.application.commands.categorize_transaction import CategorizeTransactionCommand
from app.domain.entities.transaction import Transaction
from app.domain.repositories.transaction_repository import ITransactionRepository
from app.domain.repositories.category_repository import ICategoryRepository
from app.domain.value_objects.account_id import AccountId
from app.domain.value_objects.category_id import CategoryId
from app.domain.value_objects.transaction_id import TransactionId
from app.domain.value_objects.money import Money, Currency


class TestCreateTransactionHandler:
    """Test cases for CreateTransactionHandler."""

    @pytest.fixture
    def mock_transaction_repo(self):
        """Mock transaction repository."""
        return AsyncMock(spec=ITransactionRepository)

    @pytest.fixture
    def mock_category_repo(self):
        """Mock category repository."""
        return AsyncMock(spec=ICategoryRepository)

    @pytest.fixture
    def handler(self, mock_transaction_repo, mock_category_repo):
        """Create handler with mocked dependencies."""
        return CreateTransactionHandler(mock_transaction_repo, mock_category_repo)

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
    async def test_handle_create_transaction_success(self, handler, mock_transaction_repo, mock_category_repo):
        """Test successful transaction creation."""
        # Arrange
        account_id = AccountId.new()
        category_id = CategoryId.new()
        command = CreateTransactionCommand(
            account_id=account_id,
            date=datetime.now(),
            amount=Money(Decimal("50.00"), Currency.USD),
            description="New transaction",
            merchant="Test Merchant",
            category_id=category_id,
            tags=["test"],
        )

        # Mock category lookup
        mock_category = AsyncMock()
        mock_category_repo.get_by_id.return_value = mock_category

        # Mock the repository save to return a transaction
        created_transaction = Transaction(
            id=TransactionId.new(),
            account_id=account_id,
            date=command.date,
            amount=command.amount,
            description=command.description,
            merchant=command.merchant,
            category=mock_category,
            tags=command.tags,
            created_at=datetime.now(),
        )
        mock_transaction_repo.save.return_value = created_transaction

        # Act
        result = await handler.handle(command)

        # Assert
        assert result is not None
        assert result.account_id == account_id
        assert result.amount == command.amount
        assert result.description == command.description
        assert result.merchant == command.merchant
        assert result.category == mock_category
        assert result.tags == command.tags
        mock_transaction_repo.save.assert_called_once()
        mock_category_repo.get_by_id.assert_called_once_with(category_id)

    @pytest.mark.asyncio
    async def test_handle_create_transaction_minimal_data(self, handler, mock_transaction_repo, mock_category_repo):
        """Test transaction creation with minimal required data."""
        # Arrange
        account_id = AccountId.new()
        command = CreateTransactionCommand(
            account_id=account_id,
            date=datetime.now(),
            amount=Money(Decimal("25.00"), Currency.USD),
            description="Minimal transaction",
        )

        # Mock the repository save to return a transaction
        created_transaction = Transaction(
            id=TransactionId.new(),
            account_id=account_id,
            date=command.date,
            amount=command.amount,
            description=command.description,
            merchant=None,
            category=None,
            tags=[],
            created_at=datetime.now(),
        )
        mock_transaction_repo.save.return_value = created_transaction

        # Act
        result = await handler.handle(command)

        # Assert
        assert result is not None
        assert result.account_id == account_id
        assert result.amount == command.amount
        assert result.description == command.description
        assert result.merchant is None
        assert result.category is None
        assert result.tags == []
        mock_transaction_repo.save.assert_called_once()
        mock_category_repo.get_by_id.assert_not_called()  # No category_id provided


class TestUpdateTransactionHandler:
    """Test cases for UpdateTransactionHandler."""

    @pytest.fixture
    def mock_transaction_repo(self):
        """Mock transaction repository."""
        return AsyncMock(spec=ITransactionRepository)

    @pytest.fixture
    def mock_category_repo(self):
        """Mock category repository."""
        return AsyncMock(spec=ICategoryRepository)

    @pytest.fixture
    def handler(self, mock_transaction_repo, mock_category_repo):
        """Create handler with mocked dependencies."""
        return UpdateTransactionHandler(mock_transaction_repo, mock_category_repo)

    @pytest.fixture
    def existing_transaction(self):
        """Create an existing transaction for testing."""
        return Transaction(
            id=TransactionId.new(),
            account_id=AccountId.new(),
            date=datetime.now(),
            amount=Money(Decimal("100.00"), Currency.USD),
            description="Original transaction",
            merchant="Original Merchant",
            category=None,
            tags=["original"],
            created_at=datetime.now(),
        )

    @pytest.mark.asyncio
    async def test_handle_update_transaction_success(self, handler, mock_transaction_repo, mock_category_repo, existing_transaction):
        """Test successful transaction update."""
        # Arrange
        transaction_id = existing_transaction.id
        command = UpdateTransactionCommand(
            transaction_id=transaction_id,
            description="Updated description",
            merchant="Updated Merchant",
            category_id=CategoryId.new(),
            tags=["updated"],
        )

        mock_transaction_repo.get_by_id.return_value = existing_transaction
        mock_transaction_repo.save.return_value = existing_transaction

        # Act
        result = await handler.handle(command)

        # Assert
        assert result == existing_transaction
        mock_transaction_repo.get_by_id.assert_called_once_with(transaction_id)
        mock_transaction_repo.save.assert_called_once()
        saved_transaction = mock_transaction_repo.save.call_args[0][0]
        assert saved_transaction.description == "Updated description"
        assert saved_transaction.merchant == "Updated Merchant"

    @pytest.mark.asyncio
    async def test_handle_update_transaction_not_found(self, handler, mock_transaction_repo):
        """Test updating a non-existent transaction."""
        # Arrange
        command = UpdateTransactionCommand(
            transaction_id=TransactionId.new(),
            description="Updated description",
        )

        mock_transaction_repo.get_by_id.return_value = None

        # Act
        result = await handler.handle(command)

        # Assert
        assert result is None
        mock_transaction_repo.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_handle_update_transaction_partial_update(self, handler, mock_transaction_repo, existing_transaction):
        """Test partial transaction update."""
        # Arrange
        transaction_id = existing_transaction.id
        command = UpdateTransactionCommand(
            transaction_id=transaction_id,
            description="Only description updated",
            # Other fields remain None
        )

        mock_transaction_repo.get_by_id.return_value = existing_transaction
        mock_transaction_repo.save.return_value = existing_transaction

        # Act
        result = await handler.handle(command)

        # Assert
        assert result == existing_transaction
        saved_transaction = mock_transaction_repo.save.call_args[0][0]
        assert saved_transaction.description == "Only description updated"
        assert saved_transaction.merchant == "Original Merchant"  # Unchanged
        assert saved_transaction.tags == ["original"]  # Unchanged


class TestDeleteTransactionHandler:
    """Test cases for DeleteTransactionHandler."""

    @pytest.fixture
    def mock_transaction_repo(self):
        """Mock transaction repository."""
        return AsyncMock(spec=ITransactionRepository)

    @pytest.fixture
    def handler(self, mock_transaction_repo):
        """Create handler with mocked dependencies."""
        return DeleteTransactionHandler(mock_transaction_repo)

    @pytest.mark.asyncio
    async def test_handle_delete_transaction_success(self, handler, mock_transaction_repo):
        """Test successful transaction deletion."""
        # Arrange
        transaction_id = TransactionId.new()
        command = DeleteTransactionCommand(transaction_id=transaction_id)

        mock_transaction_repo.delete.return_value = True

        # Act
        result = await handler.handle(command)

        # Assert
        assert result is True
        mock_transaction_repo.delete.assert_called_once_with(transaction_id)

    @pytest.mark.asyncio
    async def test_handle_delete_transaction_not_found(self, handler, mock_transaction_repo):
        """Test deleting a non-existent transaction."""
        # Arrange
        transaction_id = TransactionId.new()
        command = DeleteTransactionCommand(transaction_id=transaction_id)

        # Mock repository to indicate transaction doesn't exist
        mock_transaction_repo.get_by_id.return_value = None
        mock_transaction_repo.delete.return_value = False

        # Act
        result = await handler.handle(command)

        # Assert
        assert result is False
        mock_transaction_repo.get_by_id.assert_called_once_with(transaction_id)
        mock_transaction_repo.delete.assert_not_called()  # Should not attempt to delete if transaction doesn't exist


class TestCategorizeTransactionHandler:
    """Test cases for CategorizeTransactionHandler."""

    @pytest.fixture
    def mock_transaction_repo(self):
        """Mock transaction repository."""
        return AsyncMock(spec=ITransactionRepository)

    @pytest.fixture
    def mock_category_repo(self):
        """Mock category repository."""
        return AsyncMock(spec=ICategoryRepository)

    @pytest.fixture
    def handler(self, mock_transaction_repo, mock_category_repo):
        """Create handler with mocked dependencies."""
        return CategorizeTransactionHandler(mock_transaction_repo, mock_category_repo)

    @pytest.fixture
    def existing_transaction(self):
        """Create an existing transaction for testing."""
        return Transaction(
            id=TransactionId.new(),
            account_id=AccountId.new(),
            date=datetime.now(),
            amount=Money(Decimal("100.00"), Currency.USD),
            description="Test transaction",
            merchant="Test Merchant",
            category=None,
            tags=["test"],
            created_at=datetime.now(),
        )

    @pytest.fixture
    def mock_category(self):
        """Create a mock category."""
        category = AsyncMock()
        category.id = CategoryId.new()
        category.name = "Test Category"
        return category

    @pytest.mark.asyncio
    async def test_handle_categorize_transaction_success(self, handler, mock_transaction_repo, mock_category_repo, existing_transaction, mock_category):
        """Test successful transaction categorization."""
        # Arrange
        transaction_id = existing_transaction.id
        category_id = mock_category.id
        command = CategorizeTransactionCommand(
            transaction_id=transaction_id,
            category_id=category_id,
        )

        mock_transaction_repo.get_by_id.return_value = existing_transaction
        mock_category_repo.get_by_id.return_value = mock_category
        mock_transaction_repo.save.return_value = existing_transaction

        # Act
        result = await handler.handle(command)

        # Assert
        assert result == existing_transaction
        mock_transaction_repo.get_by_id.assert_called_once_with(transaction_id)
        mock_category_repo.get_by_id.assert_called_once_with(category_id)
        mock_transaction_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_handle_categorize_transaction_not_found(self, handler, mock_transaction_repo, mock_category_repo, mock_category):
        """Test categorizing a non-existent transaction."""
        # Arrange
        transaction_id = TransactionId.new()
        category_id = mock_category.id
        command = CategorizeTransactionCommand(
            transaction_id=transaction_id,
            category_id=category_id,
        )

        mock_transaction_repo.get_by_id.return_value = None
        mock_category_repo.get_by_id.return_value = mock_category

        # Act
        result = await handler.handle(command)

        # Assert
        assert result is None
        mock_transaction_repo.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_handle_categorize_category_not_found(self, handler, mock_transaction_repo, mock_category_repo, existing_transaction):
        """Test categorizing with a non-existent category."""
        # Arrange
        transaction_id = existing_transaction.id
        category_id = CategoryId.new()
        command = CategorizeTransactionCommand(
            transaction_id=transaction_id,
            category_id=category_id,
        )

        mock_transaction_repo.get_by_id.return_value = existing_transaction
        mock_category_repo.get_by_id.return_value = None

        # Act
        result = await handler.handle(command)

        # Assert
        assert result is None
        mock_transaction_repo.save.assert_not_called()
