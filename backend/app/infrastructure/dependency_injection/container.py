"""Dependency injection container for the MoneyMind application."""

from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import async_sessionmaker

from ..persistence.database import get_session_factory
from ..persistence.repositories.user_repository import UserRepository
from ..persistence.repositories.transaction_repository import SqlAlchemyTransactionRepository
from ..persistence.repositories.category_repository import SqlAlchemyCategoryRepository
from ...application.services.transaction_service import TransactionService
from ...application.queries.search_transactions_handler import SearchTransactionsQueryHandler
from ...infrastructure.auth_service import AuthService


class Container(containers.DeclarativeContainer):
    """Application dependency injection container."""

    # Infrastructure layer - Database
    session_factory = providers.Singleton(get_session_factory)

    # Infrastructure layer - Repositories
    user_repository = providers.Factory(
        UserRepository,
        session_factory=session_factory,
    )

    transaction_repository = providers.Factory(
        SqlAlchemyTransactionRepository,
        session_factory=session_factory,
    )

    category_repository = providers.Factory(
        SqlAlchemyCategoryRepository,
        session_factory=session_factory,
    )

    # Application layer - Query Handlers
    search_transactions_handler = providers.Factory(
        SearchTransactionsQueryHandler,
        transaction_repository=transaction_repository,
        category_repository=category_repository,
    )

    # Application layer - Services
    auth_service = providers.Factory(
        AuthService,
        user_repository=user_repository,
    )

    transaction_service = providers.Factory(
        TransactionService,
        transaction_repository=transaction_repository,
        category_repository=category_repository,
        search_handler=search_transactions_handler,
    )


# Global container instance
container = Container()
