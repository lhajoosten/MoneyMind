"""Insight domain service."""

from dataclasses import dataclass
from typing import List, Protocol

from ..entities.transaction import Transaction
from ..entities.budget import Budget


class AIService(Protocol):
    """Protocol for AI insight generation."""

    async def generate_insights(self, spending_patterns: dict, budget_analysis: dict) -> List['Insight']:
        """Generate AI-powered financial insights."""
        ...


@dataclass
class Insight:
    """Financial insight."""
    title: str
    description: str
    type: str  # 'pattern', 'anomaly', 'suggestion', 'warning'
    severity: str  # 'low', 'medium', 'high'
    data: dict


@dataclass
class Anomaly:
    """Spending anomaly."""
    transaction: Transaction
    reason: str
    severity: str


class InsightService:
    """Domain service for generating financial insights."""

    def __init__(self, ai_service: AIService):
        """Initialize the insight service."""
        self._ai_service = ai_service

    async def generate_monthly_insights(self,
                                       transactions: List[Transaction],
                                       budgets: List[Budget]) -> List[Insight]:
        """Generate AI-powered financial insights."""
        spending_patterns = self._analyze_spending_patterns(transactions)
        budget_analysis = self._analyze_budget_performance(transactions, budgets)

        insights = await self._ai_service.generate_insights(
            spending_patterns,
            budget_analysis
        )

        return insights

    def detect_anomalies(self, transactions: List[Transaction]) -> List[Anomaly]:
        """Detect unusual spending patterns."""
        # Statistical analysis + AI for anomaly detection
        anomalies = []

        # Simple anomaly detection based on amount thresholds
        amounts = [t.amount.value for t in transactions if t.amount.is_negative()]
        if amounts:
            mean_amount = sum(amounts) / len(amounts)
            std_dev = (sum((x - mean_amount) ** 2 for x in amounts) / len(amounts)) ** 0.5

            for transaction in transactions:
                if transaction.amount.is_negative():
                    z_score = abs(transaction.amount.value - mean_amount) / std_dev if std_dev > 0 else 0
                    if z_score > 2.0:  # More than 2 standard deviations
                        anomalies.append(Anomaly(
                            transaction=transaction,
                            reason=f"Unusually high expense (z-score: {z_score:.2f})",
                            severity="high" if z_score > 3.0 else "medium"
                        ))

        return anomalies

    def _analyze_spending_patterns(self, transactions: List[Transaction]) -> dict:
        """Analyze spending patterns."""
        # Group by category, merchant, etc.
        patterns = {
            'total_spending': sum(t.amount.value for t in transactions if t.amount.is_negative()),
            'total_income': sum(t.amount.value for t in transactions if t.amount.is_positive()),
            'transaction_count': len(transactions),
            'categories': {},
            'merchants': {},
        }

        for transaction in transactions:
            if transaction.category:
                cat_name = transaction.category.name
                if cat_name not in patterns['categories']:
                    patterns['categories'][cat_name] = 0
                patterns['categories'][cat_name] += abs(transaction.amount.value)

            if transaction.merchant:
                if transaction.merchant not in patterns['merchants']:
                    patterns['merchants'][transaction.merchant] = 0
                patterns['merchants'][transaction.merchant] += abs(transaction.amount.value)

        return patterns

    def _analyze_budget_performance(self, transactions: List[Transaction], budgets: List[Budget]) -> dict:
        """Analyze budget performance."""
        analysis = {}

        for budget in budgets:
            category_spending = sum(
                abs(t.amount.value) for t in transactions
                if t.category and t.category.id == budget.category.id and t.amount.is_negative()
            )

            analysis[budget.category.name] = {
                'budget_limit': budget.limit.value,
                'actual_spending': category_spending,
                'remaining': budget.limit.value - category_spending,
                'percentage_used': (category_spending / budget.limit.value * 100) if budget.limit.value > 0 else 100,
                'is_exceeded': category_spending > budget.limit.value
            }

        return analysis
