"""Insight DTOs."""

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class InsightDto:
    """Data transfer object for Insight."""
    title: str
    description: str
    type: str  # 'pattern', 'anomaly', 'suggestion', 'warning'
    severity: str  # 'low', 'medium', 'high'
    data: Dict[str, Any]

    @staticmethod
    def from_entity(insight: 'Insight') -> 'InsightDto':
        """Create DTO from domain entity."""
        return InsightDto(
            title=insight.title,
            description=insight.description,
            type=insight.type,
            severity=insight.severity,
            data=insight.data,
        )


@dataclass
class MonthlySummaryDto:
    """DTO for monthly financial summary."""
    month: int
    year: int
    total_income: float
    total_expenses: float
    net_income: float
    currency: str
    top_categories: List[Dict[str, Any]]
    transaction_count: int
    budget_performance: Dict[str, Any]


@dataclass
class CategorySpendingDto:
    """DTO for category spending data."""
    category_id: str
    category_name: str
    amount: float
    percentage: float
    transaction_count: int
    color: str
