"""
main.py — Entry Point for the SkillWallet GenAI FastAPI Application

Initializes the FastAPI app instance, registers routers,
and configures middleware.
"""

# ──────────────────────────────────────────────
# Imports
# ──────────────────────────────────────────────
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.routers.conversation import router as conversation_router
from config import get_settings


# ──────────────────────────────────────────────
# Application Factory
# ──────────────────────────────────────────────

def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    settings = get_settings()
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
    )

    # Configure CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register conversation router
    app.include_router(conversation_router)

    @app.get("/")
    async def root():
        """Health check endpoint."""
        return {
            "status": "online",
            "project": settings.PROJECT_NAME,
            "version": settings.VERSION
        }

    return app


# ──────────────────────────────────────────────
# App Instance
# ──────────────────────────────────────────────

app = create_app()


# ──────────────────────────────────────────────
# Entry Point
# ──────────────────────────────────────────────

def main():
    """Run the application using uvicorn."""
    settings = get_settings()
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)


if __name__ == "__main__":
    main()

