"""Authentication DTOs for API requests and responses."""

from pydantic import BaseModel, EmailStr, Field


class UserCreateRequest(BaseModel):
    """Request model for user registration."""
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)


class UserLoginRequest(BaseModel):
    """Request model for user login."""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Response model for authentication tokens."""
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """Response model for user information."""
    id: str
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool
    full_name: str

    @classmethod
    def from_user(cls, user: "User") -> "UserResponse":
        """Create a UserResponse from a User entity."""
        return cls(
            id=str(user.id),
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            full_name=user.full_name,
        )
