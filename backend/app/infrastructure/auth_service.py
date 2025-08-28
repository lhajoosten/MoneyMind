"""Authentication service for user management and JWT token handling."""

import uuid
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.domain.entities.user import User
from app.domain.repositories import IUserRepository
from app.domain.value_objects.user_id import UserId


class AuthService:
    """Service for handling user authentication and JWT tokens."""

    def __init__(
        self,
        user_repository: IUserRepository,
        secret_key: str,
        algorithm: str = "HS256",
        access_token_expire_minutes: int = 30,
    ):
        self.user_repository = user_repository
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate a user with email and password."""
        user = await self.user_repository.get_by_email(email)
        if not user:
            return None
        if not user.verify_password(password):
            return None
        return user

    async def create_user(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
    ) -> User:
        """Create a new user."""
        # Check if user already exists
        existing_user = await self.user_repository.get_by_email(email)
        if existing_user:
            raise ValueError("User with this email already exists")

        # Create new user
        user_id = UserId.new()
        user = User(
            id=user_id,
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_active=True,
        )
        user.set_password(password)

        await self.user_repository.save(user)
        return user

    def create_access_token(self, data: dict) -> str:
        """Create a JWT access token."""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(self, token: str) -> Optional[str]:
        """Verify and decode a JWT token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id: str = payload.get("sub")
            if user_id is None:
                return None
            return user_id
        except JWTError:
            return None

    async def get_current_user(self, token: str) -> Optional[User]:
        """Get the current user from a JWT token."""
        user_id = self.verify_token(token)
        if user_id is None:
            return None
        return await self.user_repository.get_by_id(UserId.from_string(user_id))
