"""Authentication API endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.application.dtos.auth_dto import (
    TokenResponse,
    UserCreateRequest,
    UserLoginRequest,
    UserResponse,
)
from app.domain.entities.user import User
from app.infrastructure.auth_service import AuthService
from app.infrastructure.persistence.repositories.user_repository import UserRepository

# Dependency injection setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter(prefix="/auth", tags=["authentication"])


async def get_auth_service() -> AuthService:
    """Dependency to get the auth service."""
    # In a real app, this would be injected via dependency injection container
    from app.infrastructure.persistence.database import get_session_factory
    from app.infrastructure.persistence.repositories.user_repository import UserRepository

    session_factory = get_session_factory()
    user_repository = UserRepository(session_factory)
    return AuthService(
        user_repository=user_repository,
        secret_key="your-secret-key-here",  # In production, use environment variable
    )


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> User:
    """Dependency to get the current authenticated user."""
    user = await auth_service.get_current_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    return user


@router.post("/register", response_model=UserResponse)
async def register_user(
    user_data: UserCreateRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> UserResponse:
    """Register a new user."""
    try:
        user = await auth_service.create_user(
            email=user_data.email,
            password=user_data.password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
        )
        return UserResponse.from_user(user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/login", response_model=TokenResponse)
async def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> TokenResponse:
    """Authenticate a user and return an access token."""
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )

    access_token = auth_service.create_access_token(data={"sub": str(user.id)})
    return TokenResponse(access_token=access_token)


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: Annotated[User, Depends(get_current_user)],
) -> UserResponse:
    """Get information about the current authenticated user."""
    return UserResponse.from_user(current_user)


@router.post("/logout")
async def logout_user() -> dict[str, str]:
    """Logout endpoint (client-side token removal)."""
    # In a stateless JWT system, logout is handled client-side
    # For server-side logout, you would implement token blacklisting
    return {"message": "Successfully logged out"}
