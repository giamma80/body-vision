"""API routes aggregator."""

from fastapi import APIRouter

from app.api.endpoints import predict

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(predict.router, prefix="/predict", tags=["predict"])
