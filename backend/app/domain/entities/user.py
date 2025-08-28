"""User domain entity."""

from dataclasses import dataclass
from typing import Optional

from passlib.context import CryptContext

from .entity import Entity
from app.domain.value_objects.user_id import UserId

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass
class User(Entity):
    """Domain entity representing a user."""

    id: UserId
    email: str
    first_name: str
    last_name: str
    is_active: bool
    hashed_password: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate the user."""
        if not self.email or not self.email.strip():
            raise ValueError("User email cannot be empty")
        if not self.first_name or not self.first_name.strip():
            raise ValueError("User first name cannot be empty")
        if not self.last_name or not self.last_name.strip():
            raise ValueError("User last name cannot be empty")

    @property
    def full_name(self) -> str:
        """Get the user's full name."""
        return f"{self.first_name} {self.last_name}"

    def set_password(self, password: str) -> None:
        """Hash and set the user's password."""
        if not password or len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        self.hashed_password = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        """Verify a password against the stored hash."""
        if not self.hashed_password:
            return False
        return pwd_context.verify(password, self.hashed_password)

    def deactivate(self) -> None:
        """Deactivate the user."""
        self.is_active = False

    def activate(self) -> None:
        """Activate the user."""
        self.is_active = True
