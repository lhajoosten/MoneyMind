# GitHub Copilot Instructions - Personal Finance Insights

## 🎯 Project Context
You are helping build a **Personal Finance Insights** application using **Python/FastAPI + React/TypeScript**. The developer has extensive **.NET/Angular** experience and wants to apply **Clean Architecture**, **SOLID principles**, **DDD**, and **CQRS** patterns in this new tech stack.

## 📋 Architecture Guidelines

### Clean Architecture Structure
```
- **Domain Layer**: Entities, Value Objects, Domain Services, Specifications
- **Application Layer**: Use Cases, Commands/Queries (CQRS), DTOs, Handlers  
- **Infrastructure Layer**: Repositories, External Services, AI Services
- **API Layer**: Controllers, Middleware, Dependency Injection
- **UI Layer**: React Components, Custom Hooks, State Management
```

### Key Patterns to Follow
- **CQRS**: Separate Command and Query models/handlers
- **Repository Pattern**: Abstract data access behind interfaces
- **Specification Pattern**: Encapsulate business rules in reusable specifications
- **Domain Services**: Complex business logic that doesn't fit in entities
- **Factory Pattern**: Complex object creation logic

## 🐍 Python/FastAPI Guidelines

### Code Style & Quality
```python
# ✅ GOOD: Type hints everywhere
from typing import List, Optional, Protocol
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Transaction:
    id: TransactionId
    amount: Money
    date: datetime
    description: str

# ✅ GOOD: Use protocols for dependency injection
class TransactionRepository(Protocol):
    async def get_by_id(self, id: TransactionId) -> Optional[Transaction]:
        ...
    
    async def find_by_specification(self, spec: Specification[Transaction]) -> List[Transaction]:
        ...

# ✅ GOOD: Dependency injection in FastAPI
@router.post("/transactions/import")
async def import_transactions(
    command: ImportTransactionsCommand,
    handler: ImportTransactionsHandler = Depends(get_import_handler)
) -> ImportResult:
    return await handler.handle(command)
```

### Domain-Driven Design
```python
# ✅ GOOD: Rich domain entities
class Transaction:
    def __init__(self, id: TransactionId, amount: Money, date: datetime, description: str):
        self._id = id
        self._amount = amount
        self._date = date  
        self._description = description
        self._validate()
    
    def categorize(self, category: Category) -> None:
        """Business logic in the domain"""
        if not category.is_active:
            raise DomainException("Cannot assign inactive category")
        self._category = category
        self._add_domain_event(TransactionCategorizedEvent(self._id, category.id))
    
    def is_recurring_pattern(self, other_transactions: List['Transaction']) -> bool:
        """Domain logic for pattern detection"""
        return len([t for t in other_transactions 
                   if t.merchant_matches(self._description)]) >= 3

# ✅ GOOD: Specifications for reusable queries
class TransactionsByDateRangeSpec:
    def __init__(self, start_date: datetime, end_date: datetime):
        self.start_date = start_date
        self.end_date = end_date
    
    def is_satisfied_by(self, transaction: Transaction) -> bool:
        return self.start_date <= transaction.date <= self.end_date
```

### CQRS Implementation
```python
# ✅ GOOD: Separate Command and Query models
@dataclass
class ImportTransactionsCommand:
    file_data: bytes
    account_id: AccountId
    user_id: UserId

@dataclass  
class GetMonthlySpendingQuery:
    user_id: UserId
    month: int
    year: int
    category_filter: Optional[CategoryId] = None

# ✅ GOOD: Dedicated handlers
class ImportTransactionsHandler:
    def __init__(self, 
                 repository: TransactionRepository,
                 categorization_service: CategorizationService,
                 event_bus: EventBus):
        self._repository = repository
        self._categorization_service = categorization_service
        self._event_bus = event_bus
    
    async def handle(self, command: ImportTransactionsCommand) -> ImportResult:
        # Complex business workflow
        transactions = await self._parse_transactions(command.file_data)
        
        for transaction in transactions:
            category = await self._categorization_service.categorize(transaction)
            transaction.categorize(category)
            await self._repository.save(transaction)
        
        await self._event_bus.publish_all(get_domain_events())
        return ImportResult(imported_count=len(transactions))
```

### Error Handling & Validation
```python
# ✅ GOOD: Domain exceptions
class DomainException(Exception):
    pass

class TransactionNotFoundException(DomainException):
    def __init__(self, transaction_id: TransactionId):
        super().__init__(f"Transaction {transaction_id} not found")

# ✅ GOOD: Input validation with Pydantic
from pydantic import BaseModel, validator

class CreateBudgetRequest(BaseModel):
    category_id: str
    amount: Decimal
    period: str
    
    @validator('amount')
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Amount must be positive')
        return v
    
    @validator('period')
    def period_must_be_valid(cls, v):
        if v not in ['MONTHLY', 'YEARLY']:
            raise ValueError('Period must be MONTHLY or YEARLY')
        return v
```

### Testing Guidelines
```python
# ✅ GOOD: Unit tests for domain logic
import pytest
from unittest.mock import Mock

class TestTransaction:
    def test_categorize_with_inactive_category_should_raise_exception(self):
        # Arrange
        transaction = Transaction(TransactionId("123"), Money(100), datetime.now(), "Store")
        inactive_category = Category(CategoryId("cat1"), "Food", is_active=False)
        
        # Act & Assert  
        with pytest.raises(DomainException):
            transaction.categorize(inactive_category)
    
    def test_is_recurring_pattern_with_multiple_matches_should_return_true(self):
        # Arrange
        transaction = Transaction(TransactionId("1"), Money(50), datetime.now(), "Netflix")
        similar_transactions = [
            Transaction(TransactionId("2"), Money(50), datetime.now(), "Netflix"),
            Transaction(TransactionId("3"), Money(50), datetime.now(), "Netflix"),
            Transaction(TransactionId("4"), Money(50), datetime.now(), "Netflix")
        ]
        
        # Act
        result = transaction.is_recurring_pattern(similar_transactions)
        
        # Assert
        assert result is True

# ✅ GOOD: Integration tests for handlers
class TestImportTransactionsHandler:
    async def test_handle_should_save_transactions_and_publish_events(self):
        # Arrange
        mock_repo = Mock(spec=TransactionRepository)
        mock_categorization = Mock(spec=CategorizationService)
        mock_event_bus = Mock(spec=EventBus)
        
        handler = ImportTransactionsHandler(mock_repo, mock_categorization, mock_event_bus)
        command = ImportTransactionsCommand(b"csv_data", AccountId("acc1"), UserId("user1"))
        
        # Act
        result = await handler.handle(command)
        
        # Assert
        assert result.imported_count > 0
        mock_repo.save.assert_called()
        mock_event_bus.publish_all.assert_called()
```

## ⚛️ React/TypeScript Guidelines

### Component Architecture
```typescript
// ✅ GOOD: Typed props and clean separation
interface DashboardProps {
  userId: string;
  dateRange: DateRange;
}

interface DashboardState {
  transactions: Transaction[];
  insights: Insight[];
  loading: boolean;
  error: string | null;
}

// ✅ GOOD: Custom hooks for business logic
const useDashboardData = (userId: string, dateRange: DateRange): DashboardState => {
  const [state, setState] = useState<DashboardState>({
    transactions: [],
    insights: [],
    loading: true,
    error: null
  });

  useEffect(() => {
    const loadData = async () => {
      try {
        setState(prev => ({ ...prev, loading: true, error: null }));
        
        const [transactions, insights] = await Promise.all([
          transactionService.getByDateRange(userId, dateRange),
          insightService.getInsights(userId, dateRange)
        ]);
        
        setState({
          transactions,
          insights,
          loading: false,
          error: null
        });
      } catch (error) {
        setState(prev => ({
          ...prev,
          loading: false,
          error: error instanceof Error ? error.message : 'Unknown error'
        }));
      }
    };

    loadData();
  }, [userId, dateRange]);

  return state;
};

// ✅ GOOD: Clean component with separated concerns
const Dashboard: React.FC<DashboardProps> = ({ userId, dateRange }) => {
  const { transactions, insights, loading, error } = useDashboardData(userId, dateRange);
  
  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorDisplay message={error} />;
  
  return (
    <div className="dashboard">
      <MonthlyOverview transactions={transactions} />
      <CategoryBreakdown transactions={transactions} />
      <InsightCards insights={insights} />
    </div>
  );
};
```

### Service Layer (API Calls)
```typescript
// ✅ GOOD: Typed API client with error handling
class TransactionService {
  private readonly apiClient: ApiClient;
  
  constructor(apiClient: ApiClient) {
    this.apiClient = apiClient;
  }
  
  async importTransactions(file: File, accountId: string): Promise<ImportResult> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('account_id', accountId);
    
    try {
      const response = await this.apiClient.post<ImportResult>('/api/transactions/import', formData);
      return response.data;
    } catch (error) {
      if (error instanceof ApiError && error.status === 400) {
        throw new ValidationError('Invalid file format or data');
      }
      throw new ServiceError('Failed to import transactions');
    }
  }
  
  async getByDateRange(userId: string, dateRange: DateRange): Promise<Transaction[]> {
    const params = {
      user_id: userId,
      start_date: dateRange.startDate.toISOString(),
      end_date: dateRange.endDate.toISOString()
    };
    
    const response = await this.apiClient.get<Transaction[]>('/api/transactions', { params });
    return response.data.map(t => Transaction.fromApi(t));
  }
}

// ✅ GOOD: Domain models in TypeScript
class Transaction {
  constructor(
    public readonly id: string,
    public readonly amount: number,
    public readonly date: Date,
    public readonly description: string,
    public readonly category?: Category
  ) {}
  
  static fromApi(dto: TransactionDto): Transaction {
    return new Transaction(
      dto.id,
      dto.amount,
      new Date(dto.date),
      dto.description,
      dto.category ? Category.fromApi(dto.category) : undefined
    );
  }
  
  get isIncome(): boolean {
    return this.amount > 0;
  }
  
  get isExpense(): boolean {
    return this.amount < 0;
  }
  
  isInCategory(categoryId: string): boolean {
    return this.category?.id === categoryId;
  }
}
```

## 🤖 AI Integration Guidelines

### LangChain Implementation
```python
# ✅ GOOD: Domain-specific AI services
class FinancialInsightService:
    def __init__(self, llm: BaseLLM, vector_store: VectorStore):
        self._llm = llm
        self._vector_store = vector_store
        
    async def generate_spending_insights(self, transactions: List[Transaction]) -> List[Insight]:
        """Generate AI insights from transaction patterns"""
        
        # Prepare context for AI
        spending_summary = self._create_spending_summary(transactions)
        
        prompt = PromptTemplate.from_template("""
        Based on the following spending data, provide 3-5 actionable financial insights:
        
        Spending Summary: {spending_summary}
        
        Focus on:
        - Spending patterns and trends
        - Potential savings opportunities  
        - Budget recommendations
        - Unusual spending behavior
        
        Format as JSON array of insights with 'category', 'message', and 'priority' fields.
        """)
        
        response = await self._llm.ainvoke(prompt.format(spending_summary=spending_summary))
        return self._parse_insights(response)

# ✅ GOOD: MCP tool integration
class FinancialCalculatorTool:
    name = "financial_calculator"
    description = "Perform financial calculations like loan payments, compound interest, etc."
    
    async def calculate_loan_payment(self, principal: float, rate: float, months: int) -> dict:
        """Calculate monthly loan payment"""
        monthly_rate = rate / 12 / 100
        payment = principal * (monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
        
        return {
            "monthly_payment": round(payment, 2),
            "total_paid": round(payment * months, 2),
            "total_interest": round(payment * months - principal, 2)
        }
```

## 🎨 Code Generation Preferences

### General Rules
- **Always** include comprehensive type hints in Python
- **Always** use dataclasses for DTOs and value objects
- **Always** implement proper error handling with custom exceptions
- **Always** write unit tests for business logic
- **Always** add docstrings for public methods and classes
- **Prefer** composition over inheritance
- **Prefer** immutable data structures where possible
- **Prefer** explicit dependencies over implicit ones

### File Structure Conventions
```
# Backend Python files should follow:
src/domain/entities/transaction.py
src/domain/services/categorization_service.py
src/application/commands/import_transactions.py
src/application/handlers/import_transactions_handler.py
src/infrastructure/repositories/sqlalchemy_transaction_repository.py
src/api/controllers/transaction_controller.py

# Frontend TypeScript files should follow:
src/components/transactions/TransactionList.tsx
src/services/api/TransactionService.ts
src/hooks/useTransactions.ts
src/types/Transaction.ts
src/utils/formatters.ts
```

### Testing Conventions
- Unit tests: `test_` prefix, focus on business logic
- Integration tests: `integration_test_` prefix, test workflows  
- Component tests: `Component.test.tsx`, test user interactions
- End-to-end tests: `e2e_test_` prefix, test complete user journeys

### Documentation Style
```python
def categorize_transactions(transactions: List[Transaction], ai_service: AIService) -> List[Transaction]:
    """
    Categorize a batch of transactions using AI-powered classification.
    
    This method applies machine learning to automatically assign categories to transactions
    based on description, amount patterns, and merchant information. Falls back to rule-based
    categorization if AI confidence is low.
    
    Args:
        transactions: List of uncategorized transactions to process
        ai_service: AI service for intelligent categorization
        
    Returns:
        List of transactions with assigned categories
        
    Raises:
        CategorizationServiceException: If AI service is unavailable
        ValidationException: If transactions contain invalid data
        
    Example:
        >>> transactions = [Transaction(...), Transaction(...)]
        >>> categorized = categorize_transactions(transactions, ai_service)
        >>> assert all(t.category is not None for t in categorized)
    """
```

## 🚫 What to Avoid
- **Don't** use `any` type in TypeScript - always be specific
- **Don't** put business logic in controllers/components  
- **Don't** use print() for logging - use proper logging
- **Don't** hardcode strings - use enums/constants
- **Don't** ignore error handling - always handle exceptions
- **Don't** write massive functions - keep them focused and small
- **Don't** skip tests for complex business logic
- **Don't** use global state when local state suffices

Remember: You're building enterprise-quality software that demonstrates clean architecture principles while learning new technologies. Every piece of code should be maintainable, testable, and follow SOLID principles!
