"""Categorization domain service."""

from dataclasses import dataclass
from typing import List, Optional, Protocol

from ..entities.transaction import Transaction
from ..entities.category import Category
from ..value_objects.money import Money


class AIService(Protocol):
    """Protocol for AI categorization service."""

    async def categorize(self, description: str, merchant: Optional[str], amount: 'Money') -> Category:
        """Categorize a transaction using AI."""
        ...

    def suggest_categories(self, description: str) -> List['CategorySuggestion']:
        """Get category suggestions for a description."""
        ...


class RuleEngine(Protocol):
    """Protocol for rule-based categorization."""

    def categorize(self, transaction: Transaction) -> Optional['CategoryResult']:
        """Categorize using rules."""
        ...


@dataclass
class CategorySuggestion:
    """Category suggestion with confidence score."""
    category: Category
    confidence: float


@dataclass
class CategoryResult:
    """Categorization result."""
    category: Category
    confidence: float


class CategorizationService:
    """Domain service for transaction categorization."""

    def __init__(self, ai_service: AIService, rule_engine: RuleEngine):
        """Initialize the categorization service."""
        self._ai_service = ai_service
        self._rule_engine = rule_engine

    async def categorize_transaction(self, transaction: Transaction) -> Category:
        """Categorize a transaction using AI with rule-based fallback."""
        # Try rule-based first (faster, deterministic)
        rule_result = self._rule_engine.categorize(transaction)
        if rule_result and rule_result.confidence > 0.9:
            return rule_result.category

        # Use AI for complex cases
        ai_category = await self._ai_service.categorize(
            transaction.description,
            transaction.merchant,
            transaction.amount
        )

        return ai_category

    def suggest_categories(self, description: str) -> List[CategorySuggestion]:
        """Get category suggestions for user review."""
        return self._ai_service.suggest_categories(description)
