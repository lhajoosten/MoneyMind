"""Application interfaces for dependency inversion."""

from abc import ABC, abstractmethod
from typing import List, Protocol

from ..commands.import_transactions import ImportTransactionsCommand
from ..commands.create_budget import CreateBudgetCommand
from ..commands.categorize_transaction import CategorizeTransactionCommand
from ..queries.get_monthly_summary import GetMonthlySummaryQuery
from ..queries.get_insights import GetInsightsQuery
from ..queries.search_transactions import SearchTransactionsQuery
from ..dtos.transaction_dto import TransactionDto
from ..dtos.insight_dto import InsightDto, MonthlySummaryDto


class TransactionServiceInterface(Protocol):
    """Interface for transaction application service."""

    async def import_transactions(self, command: ImportTransactionsCommand) -> List[TransactionDto]:
        """Import transactions from file."""
        ...

    async def categorize_transaction(self, command: CategorizeTransactionCommand) -> TransactionDto:
        """Categorize a transaction."""
        ...

    async def search_transactions(self, query: SearchTransactionsQuery) -> List[TransactionDto]:
        """Search transactions."""
        ...


class BudgetServiceInterface(Protocol):
    """Interface for budget application service."""

    async def create_budget(self, command: CreateBudgetCommand) -> str:
        """Create a new budget."""
        ...


class InsightServiceInterface(Protocol):
    """Interface for insight application service."""

    async def get_monthly_summary(self, query: GetMonthlySummaryQuery) -> MonthlySummaryDto:
        """Get monthly financial summary."""
        ...

    async def get_insights(self, query: GetInsightsQuery) -> List[InsightDto]:
        """Get financial insights."""
        ...
