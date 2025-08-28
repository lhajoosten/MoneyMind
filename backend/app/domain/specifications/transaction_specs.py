"""Transaction specifications for querying."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from ..entities.transaction import Transaction
from ..value_objects.category_id import CategoryId
from ..value_objects.money import Money


class TransactionSpecification(ABC):
    """Base class for transaction specifications."""

    @abstractmethod
    def is_satisfied_by(self, transaction: Transaction) -> bool:
        """Check if transaction satisfies the specification."""
        ...


@dataclass
class TransactionByCategory(TransactionSpecification):
    """Specification for transactions by category."""
    category_id: CategoryId

    def is_satisfied_by(self, transaction: Transaction) -> bool:
        """Check if transaction belongs to the specified category."""
        return (
            transaction.category is not None and
            transaction.category.id == self.category_id
        )


@dataclass
class TransactionByDateRange(TransactionSpecification):
    """Specification for transactions within a date range."""
    start_date: datetime
    end_date: datetime

    def is_satisfied_by(self, transaction: Transaction) -> bool:
        """Check if transaction date is within the range."""
        return self.start_date <= transaction.date <= self.end_date


@dataclass
class TransactionByAmountRange(TransactionSpecification):
    """Specification for transactions within an amount range."""
    min_amount: Optional[Money] = None
    max_amount: Optional[Money] = None

    def is_satisfied_by(self, transaction: Transaction) -> bool:
        """Check if transaction amount is within the range."""
        if self.min_amount and transaction.amount.value < self.min_amount.value:
            return False
        if self.max_amount and transaction.amount.value > self.max_amount.value:
            return False
        return True


@dataclass
class TransactionByMerchant(TransactionSpecification):
    """Specification for transactions by merchant."""
    merchant: str

    def is_satisfied_by(self, transaction: Transaction) -> bool:
        """Check if transaction matches the merchant."""
        return (
            transaction.merchant is not None and
            self.merchant.lower() in transaction.merchant.lower()
        )


@dataclass
class TransactionByDescription(TransactionSpecification):
    """Specification for transactions by description."""
    description: str

    def is_satisfied_by(self, transaction: Transaction) -> bool:
        """Check if transaction description contains the search term."""
        return self.description.lower() in transaction.description.lower()


class AndSpecification(TransactionSpecification):
    """Composite specification using AND logic."""

    def __init__(self, *specifications: TransactionSpecification):
        """Initialize with multiple specifications."""
        self.specifications = specifications

    def is_satisfied_by(self, transaction: Transaction) -> bool:
        """Check if transaction satisfies all specifications."""
        return all(spec.is_satisfied_by(transaction) for spec in self.specifications)


class OrSpecification(TransactionSpecification):
    """Composite specification using OR logic."""

    def __init__(self, *specifications: TransactionSpecification):
        """Initialize with multiple specifications."""
        self.specifications = specifications

    def is_satisfied_by(self, transaction: Transaction) -> bool:
        """Check if transaction satisfies any specification."""
        return any(spec.is_satisfied_by(transaction) for spec in self.specifications)


class NotSpecification(TransactionSpecification):
    """Negation specification."""

    def __init__(self, specification: TransactionSpecification):
        """Initialize with a specification to negate."""
        self.specification = specification

    def is_satisfied_by(self, transaction: Transaction) -> bool:
        """Check if transaction does not satisfy the specification."""
        return not self.specification.is_satisfied_by(transaction)
