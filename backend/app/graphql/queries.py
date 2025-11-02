"""GraphQL queries for BodyVision."""

from datetime import datetime

import strawberry
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.types import Info

from app.core.database import AsyncSessionLocal
from app.graphql.types import (
    AnalysisSessionType,
    AnalysisStatsType,
    AnalysisStatusEnum,
    GenderEnum,
    MeasurementType,
    UserType,
    UserWithSessionsType,
)
from app.models import AnalysisSession, AnalysisStatus, Gender, Measurement, User


async def get_db_session(info: Info) -> AsyncSession:
    """Get database session from context."""
    return AsyncSessionLocal()


def map_user_to_type(user: User) -> UserType:
    """Map SQLAlchemy User model to GraphQL type."""
    return UserType(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


def map_measurement_to_type(measurement: Measurement) -> MeasurementType:
    """Map SQLAlchemy Measurement model to GraphQL type."""
    return MeasurementType(
        id=measurement.id,
        session_id=measurement.session_id,
        body_fat_percentage=measurement.body_fat_percentage,
        body_volume_liters=measurement.body_volume_liters,
        body_density_kg_per_liter=measurement.body_density_kg_per_liter,
        lean_mass_kg=measurement.lean_mass_kg,
        fat_mass_kg=measurement.fat_mass_kg,
        mesh_url=measurement.mesh_url,
        confidence_score=measurement.confidence_score,
        created_at=measurement.created_at,
        updated_at=measurement.updated_at,
    )


def map_session_to_type(
    session: AnalysisSession, measurement: Measurement | None = None
) -> AnalysisSessionType:
    """Map SQLAlchemy AnalysisSession model to GraphQL type."""
    return AnalysisSessionType(
        id=session.id,
        user_id=session.user_id,
        job_id=session.job_id,
        status=AnalysisStatusEnum(session.status.value),
        front_image_url=session.front_image_url,
        side_image_url=session.side_image_url,
        back_image_url=session.back_image_url,
        height_cm=session.height_cm,
        weight_kg=session.weight_kg,
        age=session.age,
        gender=GenderEnum(session.gender.value),
        model_used=session.model_used,
        processing_time_seconds=session.processing_time_seconds,
        error_message=session.error_message,
        started_at=session.started_at,
        completed_at=session.completed_at,
        created_at=session.created_at,
        updated_at=session.updated_at,
        measurements=map_measurement_to_type(measurement) if measurement else None,
    )


@strawberry.type
class Query:
    """Root GraphQL query."""

    @strawberry.field
    async def user(self, info: Info, email: str) -> UserType | None:
        """Get user by email."""
        async with AsyncSessionLocal() as db:
            result = await db.execute(select(User).where(User.email == email))
            user = result.scalar_one_or_none()
            return map_user_to_type(user) if user else None

    @strawberry.field
    async def user_by_id(self, info: Info, id: int) -> UserType | None:
        """Get user by ID."""
        async with AsyncSessionLocal() as db:
            result = await db.execute(select(User).where(User.id == id))
            user = result.scalar_one_or_none()
            return map_user_to_type(user) if user else None

    @strawberry.field
    async def analysis_session(
        self, info: Info, job_id: str
    ) -> AnalysisSessionType | None:
        """Get analysis session by job ID."""
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(AnalysisSession).where(AnalysisSession.job_id == job_id)
            )
            session = result.scalar_one_or_none()

            if not session:
                return None

            # Fetch measurement if session is completed
            measurement = None
            if session.status == AnalysisStatus.COMPLETED:
                result = await db.execute(
                    select(Measurement).where(Measurement.session_id == session.id)
                )
                measurement = result.scalar_one_or_none()

            return map_session_to_type(session, measurement)

    @strawberry.field
    async def user_sessions(
        self,
        info: Info,
        email: str,
        status: AnalysisStatusEnum | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> list[AnalysisSessionType]:
        """Get user's analysis sessions with optional status filter."""
        async with AsyncSessionLocal() as db:
            # Get user
            result = await db.execute(select(User).where(User.email == email))
            user = result.scalar_one_or_none()

            if not user:
                return []

            # Build query
            query = select(AnalysisSession).where(AnalysisSession.user_id == user.id)

            if status:
                query = query.where(AnalysisSession.status == AnalysisStatus(status.value))

            query = query.order_by(desc(AnalysisSession.created_at))
            query = query.limit(limit).offset(offset)

            # Execute query
            result = await db.execute(query)
            sessions = result.scalars().all()

            # Fetch measurements for completed sessions
            session_types = []
            for session in sessions:
                measurement = None
                if session.status == AnalysisStatus.COMPLETED:
                    result = await db.execute(
                        select(Measurement).where(Measurement.session_id == session.id)
                    )
                    measurement = result.scalar_one_or_none()

                session_types.append(map_session_to_type(session, measurement))

            return session_types

    @strawberry.field
    async def user_with_sessions(
        self, info: Info, email: str, limit: int = 10
    ) -> UserWithSessionsType | None:
        """Get user with their recent analysis sessions."""
        async with AsyncSessionLocal() as db:
            # Get user
            result = await db.execute(select(User).where(User.email == email))
            user = result.scalar_one_or_none()

            if not user:
                return None

            # Get sessions
            result = await db.execute(
                select(AnalysisSession)
                .where(AnalysisSession.user_id == user.id)
                .order_by(desc(AnalysisSession.created_at))
                .limit(limit)
            )
            sessions = result.scalars().all()

            # Map to types
            session_types = []
            for session in sessions:
                measurement = None
                if session.status == AnalysisStatus.COMPLETED:
                    result = await db.execute(
                        select(Measurement).where(Measurement.session_id == session.id)
                    )
                    measurement = result.scalar_one_or_none()

                session_types.append(map_session_to_type(session, measurement))

            return UserWithSessionsType(
                id=user.id,
                email=user.email,
                full_name=user.full_name,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at,
                sessions=session_types,
            )

    @strawberry.field
    async def user_stats(self, info: Info, email: str) -> AnalysisStatsType | None:
        """Get statistics for a user's body composition analyses."""
        async with AsyncSessionLocal() as db:
            # Get user
            result = await db.execute(select(User).where(User.email == email))
            user = result.scalar_one_or_none()

            if not user:
                return None

            # Total analyses
            result = await db.execute(
                select(func.count(AnalysisSession.id)).where(
                    AnalysisSession.user_id == user.id
                )
            )
            total_analyses = result.scalar_one()

            # Completed analyses
            result = await db.execute(
                select(func.count(AnalysisSession.id)).where(
                    AnalysisSession.user_id == user.id,
                    AnalysisSession.status == AnalysisStatus.COMPLETED,
                )
            )
            completed_analyses = result.scalar_one()

            # Failed analyses
            result = await db.execute(
                select(func.count(AnalysisSession.id)).where(
                    AnalysisSession.user_id == user.id,
                    AnalysisSession.status == AnalysisStatus.FAILED,
                )
            )
            failed_analyses = result.scalar_one()

            # Average body fat % (from measurements)
            result = await db.execute(
                select(func.avg(Measurement.body_fat_percentage))
                .join(AnalysisSession)
                .where(AnalysisSession.user_id == user.id)
            )
            average_body_fat = result.scalar_one()

            # Average processing time
            result = await db.execute(
                select(func.avg(AnalysisSession.processing_time_seconds)).where(
                    AnalysisSession.user_id == user.id,
                    AnalysisSession.status == AnalysisStatus.COMPLETED,
                )
            )
            average_processing_time = result.scalar_one()

            # First and last analysis dates
            result = await db.execute(
                select(
                    func.min(AnalysisSession.created_at),
                    func.max(AnalysisSession.created_at),
                ).where(AnalysisSession.user_id == user.id)
            )
            first_date, last_date = result.one()

            return AnalysisStatsType(
                total_analyses=total_analyses,
                completed_analyses=completed_analyses,
                failed_analyses=failed_analyses,
                average_body_fat=float(average_body_fat) if average_body_fat else None,
                average_processing_time=(
                    float(average_processing_time) if average_processing_time else None
                ),
                first_analysis_date=first_date,
                last_analysis_date=last_date,
            )

    @strawberry.field
    async def latest_measurements(
        self, info: Info, email: str, limit: int = 5
    ) -> list[MeasurementType]:
        """Get user's latest body composition measurements."""
        async with AsyncSessionLocal() as db:
            # Get user
            result = await db.execute(select(User).where(User.email == email))
            user = result.scalar_one_or_none()

            if not user:
                return []

            # Get latest measurements
            result = await db.execute(
                select(Measurement)
                .join(AnalysisSession)
                .where(AnalysisSession.user_id == user.id)
                .order_by(desc(Measurement.created_at))
                .limit(limit)
            )
            measurements = result.scalars().all()

            return [map_measurement_to_type(m) for m in measurements]
