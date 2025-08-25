# MoneyMind - Personal Finance Intelligence Platform

## 🎯 Project Overview
An intelligent personal finance application that analyzes your banking data, discovers patterns, and provides proactive advice through AI. Think "Mint meets ChatGPT" - but privacy-first and self-hosted.

**Why this project is perfect for learning:**
- **Real-world relevant**: You'll use it daily
- **Data-driven**: Perfect use case for LangChain/AI
- **Complex enough**: Requires clean architecture
- **Privacy-focused**: Self-hosted, no external services
- **Scalable**: Can grow from MVP to enterprise-level

---

## 🏗️ Architecture Overview

### Clean Architecture Layers (Translated to Python/React)

```
┌─────────────────────────────────────────────┐
│                UI Layer                     │
│  React Components + State Management        │
└─────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────┐
│              API Layer                      │
│     FastAPI Controllers + DTOs              │
└─────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────┐
│           Application Layer                 │
│    Use Cases + Command/Query Handlers       │
│         (CQRS Pattern)                      │
└─────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────┐
│            Domain Layer                     │
│   Entities + Domain Services + Specs        │
└─────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────┐
│          Infrastructure Layer               │
│  Repositories + External Services + AI      │
└─────────────────────────────────────────────┘
```

---

## 📋 Functional Requirements

### Phase 1: Foundation (Week 1-2)
1. **Transaction Management**
   - CSV/OFX import from bank exports
   - Automatic + manual categorization
   - Data validation and cleaning
   - Transaction CRUD operations

2. **Dashboard & Visualizations**
   - Monthly income/expense overview
   - Category breakdown charts
   - Spending trend analysis
   - Account balance tracking

3. **Basic AI Chat**
   - "How much did I spend on restaurants this month?"
   - "What's my average expense per category?"
   - Natural language queries over financial data

### Phase 2: Intelligence (Week 3-4)
4. **Smart Insights**
   - Pattern detection via LangChain
   - Anomaly detection (unexpected expenses)
   - Predictions based on historical data
   - Recurring transaction identification

5. **AI Financial Advisor**
   - Budget suggestions
   - Savings opportunities identification
   - Personal financial coaching
   - Expense optimization recommendations

6. **Goal Tracking**
   - Savings goals with progress tracking
   - Budget limits with notifications
   - Financial milestone celebrations

### Phase 3: Advanced Features (Week 5-6)
7. **Advanced Analytics**
   - Multi-account consolidation
   - Investment tracking (optional)
   - Tax preparation helpers
   - Cash flow forecasting

8. **MCP Integration**
   - External data sources (exchange rates, inflation data)
   - Calculation tools (loan payments, investment returns)
   - Report generation tools

---

## 🛠️ Technical Architecture

### Backend Structure (Python/FastAPI)
```
src/
├── domain/
│   ├── entities/
│   │   ├── __init__.py
│   │   ├── transaction.py
│   │   ├── category.py
│   │   ├── account.py
│   │   ├── budget.py
│   │   └── user.py
│   ├── value_objects/
│   │   ├── __init__.py
│   │   ├── money.py
│   │   ├── transaction_id.py
│   │   └── date_range.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── transaction_repository.py
│   │   ├── category_repository.py
│   │   └── user_repository.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── categorization_service.py
│   │   ├── insight_service.py
│   │   └── budget_service.py
│   ├── specifications/
│   │   ├── __init__.py
│   │   ├── transaction_specs.py
│   │   └── budget_specs.py
│   └── events/
│       ├── __init__.py
│       ├── transaction_events.py
│       └── budget_events.py
│
├── application/
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── import_transactions.py
│   │   ├── create_budget.py
│   │   └── categorize_transaction.py
│   ├── queries/
│   │   ├── __init__.py
│   │   ├── get_monthly_summary.py
│   │   ├── get_insights.py
│   │   └── search_transactions.py
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── command_handlers.py
│   │   └── query_handlers.py
│   ├── dtos/
│   │   ├── __init__.py
│   │   ├── transaction_dto.py
│   │   └── insight_dto.py
│   └── interfaces/
│       ├── __init__.py
│       └── repositories.py
│
├── infrastructure/
│   ├── persistence/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── models/
│   │   └── repositories/
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── langchain_service.py
│   │   ├── categorization_ai.py
│   │   └── insight_generator.py
│   ├── mcp/
│   │   ├── __init__.py
│   │   ├── mcp_client.py
│   │   └── financial_tools.py
│   └── external/
│       ├── __init__.py
│       ├── bank_import_service.py
│       └── currency_service.py
│
└── api/
    ├── __init__.py
    ├── main.py
    ├── dependencies.py
    ├── middleware/
    │   ├── __init__.py
    │   ├── cors.py
    │   └── error_handling.py
    └── controllers/
        ├── __init__.py
        ├── transaction_controller.py
        ├── budget_controller.py
        ├── insight_controller.py
        └── chat_controller.py
```

### Frontend Structure (React/TypeScript)
```
src/
├── components/
│   ├── common/
│   │   ├── Button.tsx
│   │   ├── LoadingSpinner.tsx
│   │   ├── ErrorBoundary.tsx
│   │   └── Modal.tsx
│   ├── layout/
│   │   ├── Header.tsx
│   │   ├── Sidebar.tsx
│   │   └── Layout.tsx
│   ├── dashboard/
│   │   ├── Dashboard.tsx
│   │   ├── MonthlyOverview.tsx
│   │   ├── CategoryChart.tsx
│   │   └── SpendingTrends.tsx
│   ├── transactions/
│   │   ├── TransactionList.tsx
│   │   ├── TransactionItem.tsx
│   │   ├── ImportWizard.tsx
│   │   └── TransactionFilters.tsx
│   ├── chat/
│   │   ├── ChatInterface.tsx
│   │   ├── MessageBubble.tsx
│   │   └── ChatInput.tsx
│   ├── budgets/
│   │   ├── BudgetOverview.tsx
│   │   ├── BudgetCard.tsx
│   │   └── CreateBudget.tsx
│   └── insights/
│       ├── InsightCard.tsx
│       ├── InsightList.tsx
│       └── InsightDetails.tsx
├── hooks/
│   ├── useTransactions.ts
│   ├── useBudgets.ts
│   ├── useInsights.ts
│   ├── useChat.ts
│   └── useApi.ts
├── services/
│   ├── api/
│   │   ├── ApiClient.ts
│   │   ├── TransactionService.ts
│   │   ├── BudgetService.ts
│   │   ├── InsightService.ts
│   │   └── ChatService.ts
│   ├── formatters/
│   │   ├── CurrencyFormatter.ts
│   │   ├── DateFormatter.ts
│   │   └── NumberFormatter.ts
│   └── validation/
│       ├── TransactionValidator.ts
│       └── BudgetValidator.ts
├── stores/
│   ├── useTransactionStore.ts
│   ├── useBudgetStore.ts
│   ├── useUserStore.ts
│   └── useChatStore.ts
├── types/
│   ├── Transaction.ts
│   ├── Category.ts
│   ├── Budget.ts
│   ├── Insight.ts
│   ├── User.ts
│   └── api.ts
├── utils/
│   ├── constants.ts
│   ├── helpers.ts
│   ├── dateUtils.ts
│   └── mathUtils.ts
├── styles/
│   ├── globals.css
│   ├── components/
│   └── themes/
└── pages/
    ├── Dashboard.tsx
    ├── Transactions.tsx
    ├── Budgets.tsx
    ├── Insights.tsx
    ├── Chat.tsx
    └── Settings.tsx
```

---

## 🎨 Domain Model

### Core Entities
```python
@dataclass
class Transaction:
    id: TransactionId
    account_id: AccountId
    date: datetime
    amount: Money
    description: str
    merchant: Optional[str]
    category: Optional[Category]
    tags: List[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    def is_income(self) -> bool:
        return self.amount.value > 0
        
    def is_expense(self) -> bool:
        return self.amount.value < 0
        
    def is_recent(self, days: int = 30) -> bool:
        return (datetime.now() - self.date).days <= days
    
    def categorize(self, category: Category) -> None:
        if not category.is_active:
            raise DomainException("Cannot assign inactive category")
        self.category = category
        self._add_domain_event(TransactionCategorizedEvent(self.id, category.id))

@dataclass  
class Category:
    id: CategoryId
    name: str
    color: str
    icon: str
    parent_id: Optional[CategoryId]
    is_active: bool
    budget_limit: Optional[Money]
    
    def is_subcategory(self) -> bool:
        return self.parent_id is not None

@dataclass
class Budget:
    id: BudgetId
    category: Category
    limit: Money
    period: BudgetPeriod
    start_date: datetime
    end_date: datetime
    
    def remaining_amount(self, spent: Money) -> Money:
        return Money(self.limit.value - spent.value)
    
    def is_exceeded(self, spent: Money) -> bool:
        return spent.value > self.limit.value
    
    def percentage_used(self, spent: Money) -> float:
        return min(spent.value / self.limit.value * 100, 100)

@dataclass
class Account:
    id: AccountId
    user_id: UserId
    name: str
    account_type: AccountType
    balance: Money
    currency: Currency
    is_active: bool
    
    def can_withdraw(self, amount: Money) -> bool:
        return self.balance.value >= amount.value
```

### Value Objects
```python
@dataclass(frozen=True)
class Money:
    value: Decimal
    currency: Currency = Currency.USD
    
    def add(self, other: 'Money') -> 'Money':
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(self.value + other.value, self.currency)
    
    def is_positive(self) -> bool:
        return self.value > 0
    
    def is_negative(self) -> bool:
        return self.value < 0

@dataclass(frozen=True)
class DateRange:
    start_date: datetime
    end_date: datetime
    
    def contains(self, date: datetime) -> bool:
        return self.start_date <= date <= self.end_date
    
    def duration_days(self) -> int:
        return (self.end_date - self.start_date).days
```

### Domain Services
```python
class CategorizationService:
    def __init__(self, ai_service: AIService, rule_engine: RuleEngine):
        self._ai_service = ai_service
        self._rule_engine = rule_engine
    
    async def categorize_transaction(self, transaction: Transaction) -> Category:
        """AI-powered categorization with rule-based fallback"""
        
        # Try rule-based first (faster, deterministic)
        rule_category = self._rule_engine.categorize(transaction)
        if rule_category and rule_category.confidence > 0.9:
            return rule_category.category
        
        # Use AI for complex cases
        ai_category = await self._ai_service.categorize(
            transaction.description,
            transaction.merchant,
            transaction.amount
        )
        
        return ai_category
        
    def suggest_categories(self, description: str) -> List[CategorySuggestion]:
        """Get category suggestions for user review"""
        return self._ai_service.suggest_categories(description)

class InsightService:
    def __init__(self, ai_service: AIService):
        self._ai_service = ai_service
    
    async def generate_monthly_insights(self, 
                                       transactions: List[Transaction], 
                                       budgets: List[Budget]) -> List[Insight]:
        """Generate AI-powered financial insights"""
        
        spending_patterns = self._analyze_spending_patterns(transactions)
        budget_analysis = self._analyze_budget_performance(transactions, budgets)
        
        insights = await self._ai_service.generate_insights(
            spending_patterns,
            budget_analysis
        )
        
        return insights
    
    def detect_anomalies(self, transactions: List[Transaction]) -> List[Anomaly]:
        """Detect unusual spending patterns"""
        # Statistical analysis + AI for anomaly detection
        pass
```

---

## 📊 Use Cases (CQRS Implementation)

### Commands
```python
@dataclass
class ImportTransactionsCommand:
    file_data: bytes
    account_id: AccountId
    user_id: UserId
    file_format: FileFormat
    skip_duplicates: bool = True

@dataclass
class CreateBudgetCommand:
    user_id: UserId
    category_id: CategoryId
    amount: Money
    period: BudgetPeriod
    start_date: datetime

@dataclass
class CategorizeTransactionCommand:
    transaction_id: TransactionId
    cat
