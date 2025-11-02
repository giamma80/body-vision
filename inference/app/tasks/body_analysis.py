"""Body analysis processing task with mock implementation."""

import asyncio
import random
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import dramatiq
from loguru import logger
from sqlalchemy import select

# Add backend to path for database access
backend_dir = Path(__file__).resolve().parent.parent.parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from app.core.database import AsyncSessionLocal
from app.models import AnalysisSession, AnalysisStatus, Measurement


def calculate_mock_body_composition(
    height_cm: float, weight_kg: float, age: int, gender: str
) -> dict[str, float]:
    """
    Calculate mock body composition metrics based on user data.

    This is a simplified simulation. In production, this would use
    actual ML models (SMPL-X, MediaPipe, etc.).

    Args:
        height_cm: Height in centimeters
        weight_kg: Weight in kilograms
        age: Age in years
        gender: Gender (male/female/other)

    Returns:
        Dictionary with body composition metrics
    """
    # Simple BMI calculation
    height_m = height_cm / 100
    bmi = weight_kg / (height_m**2)

    # Mock body fat % based on BMI with some randomization
    # These are rough estimates and not medically accurate
    if gender.lower() == "male":
        base_bf = (bmi - 10) * 1.2
    elif gender.lower() == "female":
        base_bf = (bmi - 10) * 1.5
    else:
        base_bf = (bmi - 10) * 1.35

    # Add age factor
    base_bf += (age - 30) * 0.1

    # Add some randomness to simulate measurement variation
    body_fat_percentage = max(5.0, min(50.0, base_bf + random.uniform(-2, 2)))

    # Calculate lean and fat mass
    fat_mass_kg = weight_kg * (body_fat_percentage / 100)
    lean_mass_kg = weight_kg - fat_mass_kg

    # Mock body volume (simplified calculation)
    # Assumes average body density around 1.05 kg/L
    body_density = 1.10 - (body_fat_percentage / 100) * 0.15  # Fat is less dense
    body_volume_liters = weight_kg / body_density

    return {
        "body_fat_percentage": round(body_fat_percentage, 2),
        "body_volume_liters": round(body_volume_liters, 2),
        "body_density_kg_per_liter": round(body_density, 3),
        "lean_mass_kg": round(lean_mass_kg, 2),
        "fat_mass_kg": round(fat_mass_kg, 2),
        "confidence_score": round(random.uniform(0.85, 0.98), 3),
    }


@dramatiq.actor(store_results=True, max_retries=3)
def process_body_analysis(session_id: int) -> dict[str, str]:
    """
    Process body composition analysis for a given session.

    This is a MOCK implementation that simulates ML processing.
    In production, this would:
    1. Download images from Supabase
    2. Run MediaPipe pose estimation
    3. Fit SMPL-X body model
    4. Calculate actual body metrics
    5. Generate 3D mesh

    Args:
        session_id: ID of the analysis session to process

    Returns:
        Dictionary with status and message
    """
    logger.info(f"Starting body analysis for session_id={session_id}")

    # Simulate processing time (in production this would be ML inference)
    processing_start = time.time()
    time.sleep(random.uniform(2, 5))  # Simulate 2-5 seconds of processing

    # Run async database operations in sync context
    result = asyncio.run(_process_analysis_async(session_id, processing_start))

    return result


async def _process_analysis_async(session_id: int, processing_start: float) -> dict[str, str]:
    """Async helper to process analysis and save to database."""
    async with AsyncSessionLocal() as db:
        try:
            # Fetch the analysis session
            result = await db.execute(
                select(AnalysisSession).where(AnalysisSession.id == session_id)
            )
            session = result.scalar_one_or_none()

            if not session:
                logger.error(f"Session {session_id} not found")
                return {"status": "error", "message": "Session not found"}

            # Update session status to processing
            session.status = AnalysisStatus.PROCESSING
            session.started_at = datetime.now(timezone.utc)
            await db.commit()

            logger.info(
                f"Processing session {session_id}: "
                f"height={session.height_cm}cm, weight={session.weight_kg}kg, "
                f"age={session.age}, gender={session.gender}"
            )

            # Calculate mock body composition
            metrics = calculate_mock_body_composition(
                height_cm=session.height_cm,
                weight_kg=session.weight_kg,
                age=session.age,
                gender=session.gender.value,
            )

            logger.info(f"Calculated metrics for session {session_id}: {metrics}")

            # Create measurement record
            measurement = Measurement(
                session_id=session_id,
                body_fat_percentage=metrics["body_fat_percentage"],
                body_volume_liters=metrics["body_volume_liters"],
                body_density_kg_per_liter=metrics["body_density_kg_per_liter"],
                lean_mass_kg=metrics["lean_mass_kg"],
                fat_mass_kg=metrics["fat_mass_kg"],
                confidence_score=metrics["confidence_score"],
                # In production, this would be the URL to the generated mesh file
                mesh_url=None,
                mesh_vertices_count=None,
                mesh_faces_count=None,
            )
            db.add(measurement)

            # Update session with completion info
            processing_time = time.time() - processing_start
            session.status = AnalysisStatus.COMPLETED
            session.completed_at = datetime.now(timezone.utc)
            session.processing_time_seconds = processing_time
            session.model_used = "mock_v1"  # In production: smplx, star, ghum

            await db.commit()

            logger.info(
                f"Successfully completed analysis for session {session_id} "
                f"in {processing_time:.2f}s"
            )

            return {
                "status": "success",
                "message": f"Analysis completed in {processing_time:.2f}s",
                "session_id": str(session_id),
            }

        except Exception as e:
            logger.error(f"Error processing session {session_id}: {e}")

            # Update session with error status
            if session:
                session.status = AnalysisStatus.FAILED
                session.error_message = str(e)
                session.completed_at = datetime.now(timezone.utc)
                await db.commit()

            return {"status": "error", "message": str(e)}
