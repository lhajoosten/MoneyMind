"""Unit tests for TransactionService."""

import pytest
from datetime import datetime
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock
from typing import List, Optional

from app.application.services.transaction_service import TransactionService
from app.application.commands.create_transaction import CreateTransactionCommand
from app.application.commands.update_transaction import UpdateTransactionCommand
from app.application.commands.delete_transaction import DeleteTransactionCommand
from app.application.commands.categorize_transaction import CategorizeTransactionCommand
from app.application.queries.search_transactions import SearchTransactionsQuery
from app.application.dtos.transaction_dto import TransactionDto
from app.domain.entities.transaction import Transaction
from app.domain.repositories.transaction_repository import ITransactionRepository
from app.domain.repositories.category_repository import ICategoryRepository
from app.domain.value_objects.account_id import AccountId
from app.domain.value_objects.category_id import CategoryId
from app.domain.value_objects.transaction_id import TransactionId
from app.domain.value_objects.money import Money, Currency
from app.domain.value_objects.user_id import UserId


class TestTransactionService:
    """Test cases for TransactionService."""

    @pytest.fixture
    def mock_transaction_repo(self):
        """Mock transaction repository."""
        return AsyncMock(spec=ITransactionRepository)

    @pytest.fixture
    def mock_category_repo(self):
        """Mock category repository."""
        return AsyncMock(spec=ICategoryRepository)

    @pytest.fixture
    def mock_search_handler(self):
        """Mock search handler."""
        return AsyncMock()

    @pytest.fixture
    def transaction_service(self, mock_transaction_repo, mock_category_repo, mock_search_handler):
        """Create transaction service with mocked dependencies."""
        return TransactionService(
            transaction_repository=mock_transaction_repo,
            category_repository=mock_category_repo,
            search_handler=mock_search_handler,
        )

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
            category=None,  # Will be set by category relationship
            tags=["test", "sample"],
            created_at=datetime.now(),
        )

    @pytest.mark.asyncio
    async def test_create_transaction_success(self, transaction_service, mock_transaction_repo, mock_category_repo, sample_transaction):
        """Test successful transaction creation."""
        # Arrange
        account_id = AccountId.new()
        date = datetime.now()
        amount = Money(Decimal("50.00"), Currency.USD)
        description = "Test transaction"
        merchant = "Test Merchant"
        category_id = CategoryId.new()
        tags = ["test"]

        # Mock the handler's handle method
        transaction_service._create_handler.handle = AsyncMock(return_value=sample_transaction)

        # Act
        result = await transaction_service.create_transaction(
            account_id=account_id,
            date=date,
            amount=amount,
            description=description,
            merchant=merchant,
            category_id=category_id,
            tags=tags,
        )

        # Assert
        assert result == sample_transaction
        transaction_service._create_handler.handle.assert_called_once()
        call_args = transaction_service._create_handler.handle.call_args[0][0]
        assert isinstance(call_args, CreateTransactionCommand)
        assert call_args.account_id == account_id
        assert call_args.amount == amount
        assert call_args.description == description

    @pytest.mark.asyncio
    async def test_create_transaction_minimal_data(self, transaction_service, sample_transaction):
        """Test transaction creation with minimal required data."""
        # Arrange
        account_id = AccountId.new()
        date = datetime.now()
        amount = Money(Decimal("25.00"), Currency.USD)
        description = "Minimal transaction"

        transaction_service._create_handler.handle = AsyncMock(return_value=sample_transaction)

        # Act
        result = await transaction_service.create_transaction(
            account_id=account_id,
            date=date,
            amount=amount,
            description=description,
        )

        # Assert
        assert result == sample_transaction
        call_args = transaction_service._create_handler.handle.call_args[0][0]
        assert call_args.merchant is None
        assert call_args.category_id is None
        assert call_args.tags is None

    @pytest.mark.asyncio
    async def test_get_transaction_found(self, transaction_service, mock_transaction_repo, sample_transaction):
        """Test getting an existing transaction."""
        # Arrange
        transaction_id = sample_transaction.id
        mock_transaction_repo.get_by_id.return_value = sample_transaction

        # Act
        result = await transaction_service.get_transaction(transaction_id)

        # Assert
        assert result == sample_transaction
        mock_transaction_repo.get_by_id.assert_called_once_with(transaction_id)

    @pytest.mark.asyncio
    async def test_get_transaction_not_found(self, transaction_service, mock_transaction_repo):
        """Test getting a non-existent transaction."""
        # Arrange
        transaction_id = TransactionId.new()
        mock_transaction_repo.get_by_id.return_value = None

        # Act
        result = await transaction_service.get_transaction(transaction_id)

        # Assert
        assert result is None
        mock_transaction_repo.get_by_id.assert_called_once_with(transaction_id)

    @pytest.mark.asyncio
    async def test_get_transactions_by_account(self, transaction_service, mock_transaction_repo, sample_transaction):
        """Test getting all transactions for an account."""
        # Arrange
        account_id = sample_transaction.account_id
        transactions = [sample_transaction]
        mock_transaction_repo.get_by_account.return_value = transactions

        # Act
        result = await transaction_service.get_transactions_by_account(account_id)

        # Assert
        assert result == transactions
        mock_transaction_repo.get_by_account.assert_called_once_with(account_id)

    @pytest.mark.asyncio
    async def test_search_transactions(self, transaction_service, mock_search_handler, sample_transaction):
        """Test searching transactions with filters."""
        # Arrange
        query = SearchTransactionsQuery(
            user_id=UserId.new(),
            search_term="test",
            start_date=datetime.now(),
            end_date=datetime.now(),
        )
        expected_results = [TransactionDto.from_entity(sample_transaction)]
        mock_search_handler.handle.return_value = expected_results

        # Act
        result = await transaction_service.search_transactions(query)

        # Assert
        assert result == expected_results
        mock_search_handler.handle.assert_called_once_with(query)

    @pytest.mark.asyncio
    async def test_update_transaction_success(self, transaction_service, sample_transaction):
        """Test successful transaction update."""
        # Arrange
        transaction_id = sample_transaction.id
        new_description = "Updated description"
        new_merchant = "Updated Merchant"
        new_category_id = CategoryId.new()
        new_tags = ["updated"]

        updated_transaction = sample_transaction
        updated_transaction.description = new_description
        updated_transaction.merchant = new_merchant
        updated_transaction.tags = new_tags

        transaction_service._update_handler.handle = AsyncMock(return_value=updated_transaction)

        # Act
        result = await transaction_service.update_transaction(
            transaction_id=transaction_id,
            description=new_description,
            merchant=new_merchant,
            category_id=new_category_id,
            tags=new_tags,
        )

        # Assert
        assert result == updated_transaction
        call_args = transaction_service._update_handler.handle.call_args[0][0]
        assert isinstance(call_args, UpdateTransactionCommand)
        assert call_args.transaction_id == transaction_id
        assert call_args.description == new_description

    @pytest.mark.asyncio
    async def test_update_transaction_not_found(self, transaction_service):
        """Test updating a non-existent transaction."""
        # Arrange
        transaction_id = TransactionId.new()
        transaction_service._update_handler.handle = AsyncMock(return_value=None)

        # Act
        result = await transaction_service.update_transaction(
            transaction_id=transaction_id,
            description="New description",
        )

        # Assert
        assert result is None

    @pytest.mark.asyncio
    async def test_delete_transaction_success(self, transaction_service):
        """Test successful transaction deletion."""
        # Arrange
        transaction_id = TransactionId.new()
        transaction_service._delete_handler.handle = AsyncMock(return_value=True)

        # Act
        result = await transaction_service.delete_transaction(transaction_id)

        # Assert
        assert result is True
        call_args = transaction_service._delete_handler.handle.call_args[0][0]
        assert isinstance(call_args, DeleteTransactionCommand)
        assert call_args.transaction_id == transaction_id

    @pytest.mark.asyncio
    async def test_delete_transaction_not_found(self, transaction_service):
        """Test deleting a non-existent transaction."""
        # Arrange
        transaction_id = TransactionId.new()
        transaction_service._delete_handler.handle = AsyncMock(return_value=False)

        # Act
        result = await transaction_service.delete_transaction(transaction_id)

        # Assert
        assert result is False

    @pytest.mark.asyncio
    async def test_categorize_transaction_success(self, transaction_service, sample_transaction):
        """Test successful transaction categorization."""
        # Arrange
        transaction_id = sample_transaction.id
        category_id = CategoryId.new()

        categorized_transaction = sample_transaction

        transaction_service._categorize_handler.handle = AsyncMock(return_value=categorized_transaction)

        # Act
        result = await transaction_service.categorize_transaction(
            transaction_id=transaction_id,
            category_id=category_id,
        )

        # Assert
        assert result == categorized_transaction
        call_args = transaction_service._categorize_handler.handle.call_args[0][0]
        assert isinstance(call_args, CategorizeTransactionCommand)
        assert call_args.transaction_id == transaction_id
        assert call_args.category_id == category_id

    @pytest.mark.asyncio
    async def test_categorize_transaction_not_found(self, transaction_service):
        """Test categorizing a non-existent transaction."""
        # Arrange
        transaction_id = TransactionId.new()
        category_id = CategoryId.new()
        transaction_service._categorize_handler.handle = AsyncMock(return_value=None)

        # Act
        result = await transaction_service.categorize_transaction(
            transaction_id=transaction_id,
            category_id=category_id,
        )

        # Assert
        assert result is None
