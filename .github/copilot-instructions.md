# GitHub Copilot Instructions

## Developer Background & Expertise
I am transitioning from **fullstack .NET/Angular/SQL Server** development to **Python/React/PostgreSQL** with AI/LLM integration focus. My core strengths include:

### Established Expertise (.NET Ecosystem)
- **OOP Programming** with C# best practices
- **SOLID Principles** application in enterprise applications
- **Domain Driven Design (DDD)** - Entities, Value Objects, Aggregates, Domain Services
- **Event Driven Architecture** - Domain Events, Event Sourcing patterns
- **Clean Architecture** - Separation of concerns, dependency flow
- **Design Patterns** - Repository, Specification, Factory, Strategy, Observer
- **CQRS Pattern** - Command/Query separation with MediatR
- **Dependency Injection** - IoC containers, lifetime management
- **Identity Framework** - Authentication, Authorization, JWT implementation
- **Entity Framework** - Code First, migrations, complex queries
- **Automapping** - AutoMapper for object-to-object mapping
- **Mediator Pattern** - Request/response handling with MediatR

### Core Development Values
- **Modularity** - Clear separation of concerns and responsibilities
- **Readability** - Self-documenting code with meaningful names
- **Testability** - Unit/Integration tests, dependency inversion
- **Quality** - Code reviews, static analysis, consistent standards
- **Documentation** - Clear architectural decisions and API documentation
- **Decision Tracking** - Architectural Decision Records (ADRs)

---

## Target Technology Stack Translation

### Backend: Python FastAPI + SQLAlchemy
**When suggesting Python backend code:**

1. **Apply Clean Architecture principles:**
   ```python
   # Preferred structure
   /app
     /domain          # Domain models, interfaces (like Domain layer in .NET)
     /application     # Use cases, DTOs (like Application layer)
     /infrastructure  # Data access, external services
     /presentation    # FastAPI routes, controllers
   ```

2. **Use Dependency Injection patterns:**
   - Prefer `dependency-injector` library or FastAPI's dependency system
   - Implement interfaces/protocols for testability
   - Constructor injection over service locator

3. **Implement CQRS-like patterns:**
   - Separate command/query handlers
   - Use Pydantic for DTOs/requests/responses
   - Consider `mediator-py` library for MediatR-like behavior

4. **Domain-Driven Design translation:**
   - Domain entities with business logic
   - Value objects using `@dataclass` or Pydantic
   - Domain services for complex business operations
   - Repository pattern with SQLAlchemy

5. **Authentication/Authorization:**
   - JWT implementation with `python-jose`
   - Role-based authorization decorators
   - Identity management following .NET Identity patterns

### Frontend: React + TypeScript
**When suggesting React frontend code:**

1. **Maintain strong typing:**
   - Always use TypeScript
   - Define clear interfaces for all data structures
   - Use generic types where applicable

2. **Component architecture:**
   - Prefer composition over inheritance
   - Use custom hooks for business logic
   - Implement container/presenter pattern

3. **State management:**
   - Use Zustand or Redux Toolkit for complex state
   - React Query for server state management
   - Follow single responsibility for state slices

4. **Error handling and validation:**
   - Use react-hook-form with validation schemas
   - Implement global error boundaries
   - Clear error messaging patterns

### Database: PostgreSQL + SQLAlchemy
**When suggesting database code:**

1. **Entity Framework translation:**
   - Use SQLAlchemy ORM with declarative mapping
   - Implement repository pattern over direct ORM usage
   - Use Alembic for migrations (equivalent to EF migrations)

2. **Query patterns:**
   - Translate LINQ patterns to SQLAlchemy query syntax
   - Implement specification pattern for complex queries
   - Use relationship loading strategies (eager/lazy)

### AI/LLM Integration Patterns
**When suggesting AI integration:**

1. **LangChain patterns:**
   - Chain composition following SOLID principles
   - Agent architecture with clear responsibilities
   - Memory management and conversation handling

2. **RAG implementation:**
   - Vector store abstraction layers
   - Document processing pipelines
   - Retrieval strategy patterns

---

## Code Quality Standards

### Naming Conventions
- **Python**: Follow PEP 8 - snake_case for variables/functions, PascalCase for classes
- **React**: PascalCase for components, camelCase for functions/variables
- **Database**: snake_case for tables/columns

### Documentation Requirements
- **Docstrings**: Use Google-style docstrings for all public methods
- **Type hints**: Always include type annotations in Python
- **Comments**: Explain WHY, not WHAT - focus on business logic reasoning
- **README**: Include architecture overview and setup instructions

### Testing Patterns
- **Python**: Use pytest with fixtures, follow AAA pattern (Arrange, Act, Assert)
- **React**: Use Jest + React Testing Library, test behavior not implementation
- **Integration**: Test complete user workflows, not just units

### Error Handling
- **Python**: Use custom exceptions with clear hierarchy
- **React**: Implement error boundaries and graceful degradation
- **Logging**: Structured logging with correlation IDs

---

## Architectural Decision Guidelines

When suggesting architectural solutions, prioritize:

1. **Separation of Concerns** - Each module/class should have single responsibility
2. **Dependency Inversion** - Depend on abstractions, not concretions
3. **Testability** - Code should be easily unit testable
4. **Maintainability** - Prefer explicit over implicit, readable over clever
5. **Performance** - Consider async/await patterns, database query optimization
6. **Security** - Input validation, authorization checks, secure defaults

---

## Common Translation Patterns

| .NET Pattern | Python/React Equivalent |
|--------------|------------------------|
| `IRepository<T>` | Protocol-based repository with generics |
| `MediatR` | `mediator-py` or custom handler routing |
| `AutoMapper` | Pydantic model transformation |
| `FluentValidation` | Pydantic validators or `marshmallow` |
| `Entity Framework` | SQLAlchemy with repository pattern |
| `IOptions<T>` | Pydantic Settings management |
| `ILogger<T>` | Python `logging` with structured output |
| `BackgroundService` | Celery or async background tasks |

---

## AI Assistant Collaboration

When working with AI assistants:
1. **Always mention this background** when asking for architecture advice
2. **Request pattern translations** from .NET to Python/React equivalents  
3. **Ask for code reviews** against these established principles
4. **Seek clarification** on new patterns that don't align with clean architecture
5. **Request documentation** for architectural decisions made

---

## Project Structure Template

```
project-name/
├── backend/
│   ├── app/
│   │   ├── domain/          # Business entities, value objects
│   │   ├── application/     # Use cases, DTOs, interfaces
│   │   ├── infrastructure/  # Data access, external services
│   │   └── presentation/    # FastAPI routes, middleware
│   ├── tests/
│   ├── migrations/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/          # Route-based components
│   │   ├── hooks/          # Custom React hooks
│   │   ├── services/       # API clients, business logic
│   │   ├── types/          # TypeScript interfaces
│   │   └── utils/          # Helper functions
│   ├── tests/
│   └── package.json
├── docs/
│   ├── architecture/       # ADRs, system design
│   ├── api/               # API documentation
│   └── deployment/        # Infrastructure as code
└── README.md
```

Remember: **Quality over speed** - prioritize maintainable, testable code that follows established patterns over quick solutions.
