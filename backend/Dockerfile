FROM python:3.11-slim AS base

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml ./

# Install project (editable) and build-time dependencies
# Use pip directly; pyproject.toml is supported by pip via PEP 517
RUN pip install --no-cache-dir -e .

# Development stage
FROM base AS development
RUN pip install --no-cache-dir -e .[dev]

# Copy source code
COPY . .

# Run development server
CMD ["uvicorn", "app.presentation.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Production stage
FROM base AS production
COPY . .
CMD ["uvicorn", "app.presentation.main:app", "--host", "0.0.0.0", "--port", "8000"]