"""Import transactions command."""

from dataclasses import dataclass
from enum import Enum

from ...domain.value_objects.account_id import AccountId
from ...domain.value_objects.user_id import UserId


class FileFormat(Enum):
    """Supported file formats for transaction import."""
    CSV = "csv"
    OFX = "ofx"
    QFX = "qfx"


@dataclass
class ImportTransactionsCommand:
    """Command to import transactions from a file."""
    file_data: bytes
    account_id: AccountId
    user_id: UserId
    file_format: FileFormat
    skip_duplicates: bool = True
