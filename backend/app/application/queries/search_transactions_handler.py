"""Search transactions query handler."""

from typing import List

from ...domain.repositories import ITransactionRepository
from ...domain.repositories import ICategoryRepository
from ..dtos.transaction_dto import TransactionDto
from .search_transactions import SearchTransactionsQuery


class SearchTransactionsQueryHandler:
    """Handler for searching transactions."""

    def __init__(
        self,
        transaction_repository: ITransactionRepository,
        category_repository: ICategoryRepository,
    ):
        self._transaction_repository = transaction_repository
        self._category_repository = category_repository

    async def handle(self, query: SearchTransactionsQuery) -> List[TransactionDto]:
        """Handle the search transactions query."""
        # For now, get all transactions for the user's accounts
        # In a real implementation, you'd filter by user_id through account ownership
        # This is a simplified version - you'd need to implement account ownership

        # Get all transactions (simplified - should filter by user's accounts)
        transactions = await self._transaction_repository.get_all()

        # Apply filters
        filtered_transactions = []
        for transaction in transactions:
            if self._matches_filters(transaction, query):
                filtered_transactions.append(transaction)

        # Apply pagination
        start = query.offset
        end = start + query.limit
        paginated_transactions = filtered_transactions[start:end]

        # Convert to DTOs
        return [TransactionDto.from_entity(t) for t in paginated_transactions]

    def _matches_filters(self, transaction, query: SearchTransactionsQuery) -> bool:
        """Check if transaction matches the query filters."""
        # Search term filter
        if query.search_term:
            search_lower = query.search_term.lower()
            if not (
                search_lower in transaction.description.lower() or
                (transaction.merchant and search_lower in transaction.merchant.lower())
            ):
                return False

        # Category filter
        if query.category_id and transaction.category:
            if str(transaction.category.id) != query.category_id:
                return False

        # Date range filter
        if query.start_date and transaction.date < query.start_date:
            return False
        if query.end_date and transaction.date > query.end_date:
            return False

        # Amount range filter
        amount_value = transaction.amount.value
        if query.min_amount is not None and amount_value < query.min_amount:
            return False
        if query.max_amount is not None and amount_value > query.max_amount:
            return False

        return True
