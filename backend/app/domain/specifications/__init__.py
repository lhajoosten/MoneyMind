# Domain Specifications
from .transaction_specs import (
    TransactionSpecification,
    TransactionByCategory,
    TransactionByDateRange,
    TransactionByAmountRange,
    TransactionByMerchant,
    TransactionByDescription,
    AndSpecification,
    OrSpecification,
    NotSpecification,
)

__all__ = [
    "TransactionSpecification",
    "TransactionByCategory",
    "TransactionByDateRange",
    "TransactionByAmountRange",
    "TransactionByMerchant",
    "TransactionByDescription",
    "AndSpecification",
    "OrSpecification",
    "NotSpecification",
]
