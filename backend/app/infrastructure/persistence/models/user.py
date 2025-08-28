"""User database model."""

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
