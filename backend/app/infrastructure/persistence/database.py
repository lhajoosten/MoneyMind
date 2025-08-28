"""Database configuration and session management."""

from typing import AsyncGenerator
import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


# Database URL should be set via environment variable
DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql+asyncpg://user:password@localhost/moneymind"
)

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Set to False in production
    future=True,
    poolclass=StaticPool,
)

# Create async session factory
async_session_factory = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting database session."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def create_database() -> None:
    """Create database tables."""
    from .models import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_database() -> None:
    """Drop database tables."""
    from .models import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
