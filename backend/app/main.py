"""FastAPI application entry point."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.api.routes import api_router
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan events."""
    # Startup
    logger.info("Starting BodyVision API...")
    logger.info(f"Environment: {settings.APP_ENV}")
    logger.info(f"Model: {settings.BODYVISION_MODEL}")

    yield

    # Shutdown
    logger.info("Shutting down BodyVision API...")


# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Sistema full-stack per la stima della composizione corporea",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api")


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "model": settings.BODYVISION_MODEL,
    }
