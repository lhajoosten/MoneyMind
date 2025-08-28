"""User database model."""

from app.domain.entities.user import User
from app.domain.value_objects.user_id import UserId
from sqlalchemy import Boolean, Column, String

from .base import BaseModel


class UserModel(BaseModel):
    """Database model for User."""

    __tablename__ = "users"

    email = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    @classmethod
    def from_domain(cls, user: "User") -> "UserModel":
        """Create UserModel from domain User entity."""
        return cls(
            id=user.id.value if hasattr(user.id, "value") else user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            hashed_password=user.hashed_password,
            # created_at and updated_at are handled by BaseModel/database
        )

    def to_domain(self) -> "User":
        """Convert UserModel to domain User entity."""
        from app.domain.entities.user import User

        return User(
            id=UserId(self.id),
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            hashed_password=self.hashed_password,
            is_active=self.is_active,
        )
