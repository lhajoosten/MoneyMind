"""User domain entity."""

from dataclasses import dataclass

from .entity import Entity
from ..value_objects.user_id import UserId


@dataclass
class User(Entity):
    """Domain entity representing a user."""
    id: UserId
    email: str
    first_name: str
    last_name: str
    is_active: bool

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

    def deactivate(self) -> None:
        """Deactivate the user."""
        self.is_active = False

    def activate(self) -> None:
        """Activate the user."""
        self.is_active = True
