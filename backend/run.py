"""Application entry point."""

import uvicorn
from app.presentation.main import app


if __name__ == "__main__":
    uvicorn.run(
        "app.presentation.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
