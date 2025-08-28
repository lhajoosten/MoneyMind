# MoneyMind

An intelligent personal finance application that analyzes your banking data, discovers patterns, and provides proactive advice through AI

## 🏗️ Architecture

This application follows Clean Architecture principles with the following layers:

- **Domain**: Core business entities and rules
- **Application**: Use cases and CQRS commands/queries
- **Infrastructure**: Data access, external services, AI integration
- **Presentation**: FastAPI controllers and middleware

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Docker (optional)

### Backend Setup

1. **Create virtual environment:**

   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**

   ```bash
   pip install -e .
   ```

3. **Set up environment variables:**

   ```bash
   cp .env.example .env
   # Edit .env with your database URL and other settings
   ```

4. **Run database migrations:**

   ```bash
   python run.py  # This will create tables on startup
   ```

5. **Start the backend:**
   ```bash
   python run.py
   ```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Install dependencies:**

   ```bash
   cd frontend
   npm install
   ```

2. **Start development server:**
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:1412`

## 📊 Features

### Phase 1 (Current)

- ✅ Transaction Management (CRUD operations)
- ✅ Dashboard & Visualizations
- ✅ Basic AI Chat for financial queries
- ✅ Clean Architecture implementation
- ✅ PostgreSQL with SQLAlchemy ORM
- ✅ React frontend with TypeScript

### Phase 2 (Upcoming)

- 🔄 Smart Insights via LangChain
- 🔄 AI Financial Advisor
- 🔄 Goal Tracking

### Phase 3 (Future)

- 🔄 Advanced Analytics
- 🔄 MCP Integration
- 🔄 Investment Tracking

## 🛠️ Tech Stack

### Backend

- **FastAPI**: High-performance async web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **PostgreSQL**: Primary database
- **Pydantic**: Data validation
- **LangChain**: AI/LLM integration
- **Dependency Injector**: IoC container

### Frontend

- **React 18**: UI library
- **TypeScript**: Type-safe JavaScript
- **Vite**: Build tool and dev server
- **Zustand**: State management
- **React Query**: Server state management
- **Tailwind CSS**: Utility-first CSS framework
- **Recharts**: Chart library

## 📁 Project Structure

```
moneymind/
├── backend/
│   ├── app/
│   │   ├── domain/          # Business entities, value objects
│   │   ├── application/     # Use cases, DTOs, CQRS
│   │   ├── infrastructure/  # Data access, external services
│   │   └── presentation/    # FastAPI routes, middleware
│   ├── tests/
│   ├── pyproject.toml
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/          # Route-based components
│   │   ├── hooks/          # Custom React hooks
│   │   ├── services/       # API clients
│   │   ├── types/          # TypeScript interfaces
│   │   └── utils/          # Helper functions
│   ├── package.json
│   └── vite.config.ts
└── docs/
    ├── PROJECT_CASE.md     # Detailed project specification
    └── copilot-instructions.md  # AI assistant guidelines
```

## 🤝 Contributing

1. Follow the established patterns in `docs/copilot-instructions.md`
2. Maintain Clean Architecture principles
3. Write tests for new features
4. Use meaningful commit messages

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
