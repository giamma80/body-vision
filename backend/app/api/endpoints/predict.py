"""Prediction endpoint for body composition analysis."""

import uuid
from typing import Literal

import dramatiq
from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger
from pydantic import BaseModel, Field, HttpUrl
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models import AnalysisSession, AnalysisStatus, Gender, Measurement, User

router = APIRouter()

# Define the task name for sending messages
# The actual task implementation is in inference/app/tasks/body_analysis.py
BODY_ANALYSIS_TASK = "process_body_analysis"


class UserMetadata(BaseModel):
    """User metadata for body composition analysis."""

    height_cm: float = Field(..., gt=50, lt=300, description="Height in centimeters")
    weight_kg: float = Field(..., gt=20, lt=500, description="Weight in kilograms")
    age: int = Field(..., gt=0, lt=150, description="Age in years")
    gender: Literal["male", "female", "other"] = Field(..., description="Gender")
    email: str = Field(..., description="User email for tracking")


class PredictionRequest(BaseModel):
    """Request model for body composition prediction."""

    front_image_url: HttpUrl = Field(..., description="URL to front view image")
    side_image_url: HttpUrl = Field(..., description="URL to side view image")
    back_image_url: HttpUrl = Field(..., description="URL to back view image")
    user_metadata: UserMetadata = Field(..., description="User metadata")


class PredictionResponse(BaseModel):
    """Response model for body composition prediction."""

    job_id: str = Field(..., description="Job ID for tracking processing status")
    session_id: int = Field(..., description="Database session ID")
    status: Literal["queued", "processing", "completed", "failed"] = "queued"
    message: str = "Job queued for processing"


class MeasurementData(BaseModel):
    """Body composition measurement data."""

    body_fat_percentage: float
    body_volume_liters: float
    body_density_kg_per_liter: float
    lean_mass_kg: float | None = None
    fat_mass_kg: float | None = None
    mesh_url: str | None = None
    confidence_score: float | None = None


class JobStatusResponse(BaseModel):
    """Response for job status query."""

    job_id: str
    session_id: int
    status: str
    created_at: str
    started_at: str | None = None
    completed_at: str | None = None
    processing_time_seconds: float | None = None
    model_used: str | None = None
    error_message: str | None = None
    measurements: MeasurementData | None = None


@router.post(
    "/",
    response_model=PredictionResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Start body composition analysis",
    description="Queue a new job for body composition analysis from three images",
)
async def create_prediction(
    request: PredictionRequest, db: AsyncSession = Depends(get_db)
) -> PredictionResponse:
    """
    Create a new prediction job.

    This endpoint:
    1. Creates or retrieves user by email
    2. Creates an analysis session in the database
    3. Queues a background job with Dramatiq
    4. Returns job_id for tracking

    Args:
        request: Prediction request with image URLs and user metadata
        db: Database session

    Returns:
        PredictionResponse with job_id and session_id for tracking

    Raises:
        HTTPException: If validation fails or queueing fails
    """
    try:
        # Get or create user
        result = await db.execute(select(User).where(User.email == request.user_metadata.email))
        user = result.scalar_one_or_none()

        if not user:
            logger.info(f"Creating new user: {request.user_metadata.email}")
            user = User(
                email=request.user_metadata.email,
                full_name=None,  # Can be added later
                is_active=True,
            )
            db.add(user)
            await db.flush()  # Get user.id before creating session

        # Generate unique job ID
        job_id = str(uuid.uuid4())

        # Create analysis session
        session = AnalysisSession(
            user_id=user.id,
            job_id=job_id,
            status=AnalysisStatus.QUEUED,
            front_image_url=str(request.front_image_url),
            side_image_url=str(request.side_image_url),
            back_image_url=str(request.back_image_url),
            height_cm=request.user_metadata.height_cm,
            weight_kg=request.user_metadata.weight_kg,
            age=request.user_metadata.age,
            gender=Gender(request.user_metadata.gender),
        )
        db.add(session)
        await db.commit()
        await db.refresh(session)

        logger.info(
            f"Created analysis session {session.id} for user {user.email} "
            f"with job_id {job_id}"
        )

        # Queue the Dramatiq task by sending a message to the broker
        logger.info(f"Queueing Dramatiq task for session {session.id}")
        broker = dramatiq.get_broker()
        message = dramatiq.Message(
            queue_name="default",
            actor_name=BODY_ANALYSIS_TASK,
            args=(session.id,),
            kwargs={},
            options={},
        )
        broker.enqueue(message)

        return PredictionResponse(
            job_id=job_id,
            session_id=session.id,
            status="queued",
            message="Job queued for processing",
        )

    except Exception as e:
        logger.error(f"Failed to create prediction job: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to queue prediction job: {str(e)}",
        ) from e


@router.get(
    "/{job_id}",
    response_model=JobStatusResponse,
    summary="Get prediction job status",
    description="Retrieve the status and results of a prediction job",
)
async def get_prediction_status(
    job_id: str, db: AsyncSession = Depends(get_db)
) -> JobStatusResponse:
    """
    Get the status of a prediction job.

    Args:
        job_id: The job ID returned from the POST request
        db: Database session

    Returns:
        Job status and results if available

    Raises:
        HTTPException: If job not found
    """
    try:
        # Fetch session by job_id
        result = await db.execute(
            select(AnalysisSession).where(AnalysisSession.job_id == job_id)
        )
        session = result.scalar_one_or_none()

        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Job {job_id} not found",
            )

        # Fetch measurement if exists
        measurement = None
        if session.status == AnalysisStatus.COMPLETED:
            result = await db.execute(
                select(Measurement).where(Measurement.session_id == session.id)
            )
            measurement_obj = result.scalar_one_or_none()

            if measurement_obj:
                measurement = MeasurementData(
                    body_fat_percentage=measurement_obj.body_fat_percentage,
                    body_volume_liters=measurement_obj.body_volume_liters,
                    body_density_kg_per_liter=measurement_obj.body_density_kg_per_liter,
                    lean_mass_kg=measurement_obj.lean_mass_kg,
                    fat_mass_kg=measurement_obj.fat_mass_kg,
                    mesh_url=measurement_obj.mesh_url,
                    confidence_score=measurement_obj.confidence_score,
                )

        return JobStatusResponse(
            job_id=session.job_id,
            session_id=session.id,
            status=session.status.value,
            created_at=session.created_at.isoformat(),
            started_at=session.started_at.isoformat() if session.started_at else None,
            completed_at=session.completed_at.isoformat() if session.completed_at else None,
            processing_time_seconds=session.processing_time_seconds,
            model_used=session.model_used,
            error_message=session.error_message,
            measurements=measurement,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get job status for {job_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve job status",
        ) from e
