"""Prediction endpoint for body composition analysis."""

from typing import Literal

from fastapi import APIRouter, HTTPException, status
from loguru import logger
from pydantic import BaseModel, Field, HttpUrl

router = APIRouter()


class UserMetadata(BaseModel):
    """User metadata for body composition analysis."""

    height_cm: float = Field(..., gt=50, lt=300, description="Height in centimeters")
    weight_kg: float = Field(..., gt=20, lt=500, description="Weight in kilograms")
    age: int = Field(..., gt=0, lt=150, description="Age in years")
    gender: Literal["male", "female", "other"] = Field(..., description="Gender")


class PredictionRequest(BaseModel):
    """Request model for body composition prediction."""

    front_image_url: HttpUrl = Field(..., description="URL to front view image")
    side_image_url: HttpUrl = Field(..., description="URL to side view image")
    back_image_url: HttpUrl = Field(..., description="URL to back view image")
    user_metadata: UserMetadata = Field(..., description="User metadata")


class PredictionResponse(BaseModel):
    """Response model for body composition prediction."""

    job_id: str = Field(..., description="Job ID for tracking processing status")
    status: Literal["queued", "processing", "completed", "failed"] = "queued"
    message: str = "Job queued for processing"


@router.post(
    "/",
    response_model=PredictionResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Start body composition analysis",
    description="Queue a new job for body composition analysis from three images",
)
async def create_prediction(request: PredictionRequest) -> PredictionResponse:
    """
    Create a new prediction job.

    This endpoint queues a background job to process the uploaded images
    and calculate body composition metrics.

    Args:
        request: Prediction request with image URLs and user metadata

    Returns:
        PredictionResponse with job_id for tracking

    Raises:
        HTTPException: If validation fails or queueing fails
    """
    try:
        # TODO: Implement job queueing with Dramatiq
        # For now, return a placeholder response
        logger.info(f"Received prediction request for images: {request.front_image_url}")

        # Placeholder job_id (will be replaced with actual Dramatiq job ID)
        job_id = "placeholder-job-id"

        return PredictionResponse(
            job_id=job_id,
            status="queued",
            message="Job queued for processing",
        )

    except Exception as e:
        logger.error(f"Failed to create prediction job: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to queue prediction job",
        ) from e


@router.get(
    "/{job_id}",
    summary="Get prediction job status",
    description="Retrieve the status and results of a prediction job",
)
async def get_prediction_status(job_id: str) -> dict[str, str]:
    """
    Get the status of a prediction job.

    Args:
        job_id: The job ID returned from the POST request

    Returns:
        Job status and results if available

    Raises:
        HTTPException: If job not found
    """
    # TODO: Implement job status retrieval
    logger.info(f"Checking status for job: {job_id}")

    return {
        "job_id": job_id,
        "status": "queued",
        "message": "Status endpoint not yet implemented",
    }
