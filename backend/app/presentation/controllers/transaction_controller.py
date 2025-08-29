"""Transaction REST API controller."""

from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from ...application.services.transaction_service import ITransactionService, TransactionService
from ...application.queries.search_transactions import SearchTransactionsQuery
from ...application.queries.search_transactions_handler import SearchTransactionsQueryHandler
from ...application.dtos.transaction_dto import (
    TransactionDto,
    CreateTransactionRequest,
    UpdateTransactionRequest,
    CategorizeTransactionRequest,
    SearchTransactionsRequest,
    TransactionResponse,
)
from ...infrastructure.persistence.repositories.transaction_repository import SqlAlchemyTransactionRepository
from ...infrastructure.persistence.repositories.category_repository import SqlAlchemyCategoryRepository
from ...infrastructure.persistence.database import get_session_factory
from ...infrastructure.dependency_injection import container
from ...domain.value_objects.user_id import UserId
from ...domain.value_objects.account_id import AccountId
from ...domain.value_objects.category_id import CategoryId
from ...domain.value_objects.transaction_id import TransactionId
from decimal import Decimal
from ...domain.value_objects.money import Money, Currency


# Create router
router = APIRouter(prefix="/api/transactions", tags=["transactions"])


async def get_transaction_service() -> ITransactionService:
    """Dependency to get the transaction service from DI container."""
    return container.transaction_service()


@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    request: CreateTransactionRequest,
    transaction_service: ITransactionService = Depends(get_transaction_service),
) -> TransactionResponse:
    """Create a new transaction."""
    try:
        # Convert request to domain objects
        account_id = AccountId.from_string(request.account_id)
        amount = Money(Decimal(str(request.amount)), Currency(request.currency))
        category_id = CategoryId.from_string(request.category_id) if request.category_id else None

        # Create transaction
        transaction = await transaction_service.create_transaction(
            account_id=account_id,
            date=request.date,
            amount=amount,
            description=request.description,
            merchant=request.merchant,
            category_id=category_id,
            tags=request.tags,
        )

        # Convert to DTO and then to response
        dto = TransactionDto.from_entity(transaction)
        return TransactionResponse.from_dto(dto)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create transaction"
        )


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: str,
    transaction_service: ITransactionService = Depends(get_transaction_service),
) -> TransactionResponse:
    """Get a transaction by ID."""
    try:
        # Convert to domain object
        tx_id = TransactionId.from_string(transaction_id)

        # Get transaction
        transaction = await transaction_service.get_transaction(tx_id)
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )

        # Convert to DTO and then to response
        dto = TransactionDto.from_entity(transaction)
        return TransactionResponse.from_dto(dto)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get transaction: {str(e)}"
        )


@router.get("/", response_model=List[TransactionResponse])
async def search_transactions(
    request: SearchTransactionsRequest = Depends(),
    transaction_service: ITransactionService = Depends(get_transaction_service),
) -> List[TransactionResponse]:
    """Search transactions with filters."""
    try:
        # Build search query
        query = SearchTransactionsQuery(
            user_id=UserId.from_string(request.user_id),
            search_term=None,  # For now, simplified search
            category_id=request.category_id,
            start_date=request.start_date,
            end_date=request.end_date,
            min_amount=request.min_amount,
            max_amount=request.max_amount,
            limit=request.limit,
            offset=request.offset,
        )

        # Search transactions
        results = await transaction_service.search_transactions(query)

        # Convert to responses
        return [TransactionResponse.from_dto(dto) for dto in results]

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search transactions: {str(e)}"
        )


@router.put("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: str,
    request: UpdateTransactionRequest,
    transaction_service: ITransactionService = Depends(get_transaction_service),
) -> TransactionResponse:
    """Update an existing transaction."""
    try:
        # Convert to domain objects
        tx_id = TransactionId.from_string(transaction_id)
        category_id = CategoryId.from_string(request.category_id) if request.category_id else None

        # Update transaction
        transaction = await transaction_service.update_transaction(
            transaction_id=tx_id,
            description=request.description,
            merchant=request.merchant,
            category_id=category_id,
            tags=request.tags,
        )

        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )

        # Convert to DTO and then to response
        dto = TransactionDto.from_entity(transaction)
        return TransactionResponse.from_dto(dto)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update transaction: {str(e)}"
        )


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: str,
    transaction_service: ITransactionService = Depends(get_transaction_service),
) -> None:
    """Delete a transaction."""
    try:
        # Convert to domain object
        tx_id = TransactionId.from_string(transaction_id)

        # Delete transaction
        success = await transaction_service.delete_transaction(tx_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete transaction: {str(e)}"
        )


@router.post("/{transaction_id}/categorize", response_model=TransactionResponse)
async def categorize_transaction(
    transaction_id: str,
    request: CategorizeTransactionRequest,
    transaction_service: ITransactionService = Depends(get_transaction_service),
) -> TransactionResponse:
    """Categorize a transaction."""
    try:
        # Convert to domain objects
        tx_id = TransactionId.from_string(transaction_id)
        category_id = CategoryId.from_string(request.category_id)

        # Categorize transaction
        transaction = await transaction_service.categorize_transaction(
            transaction_id=tx_id,
            category_id=category_id,
        )

        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction or category not found"
            )

        # Convert to DTO and then to response
        dto = TransactionDto.from_entity(transaction)
        return TransactionResponse.from_dto(dto)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to categorize transaction: {str(e)}"
        )
