"""GraphQL types for BodyVision."""

from datetime import datetime
from enum import Enum

import strawberry


@strawberry.type
class UserType:
    """GraphQL type for User."""

    id: int
    email: str
    full_name: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime


@strawberry.type
class MeasurementType:
    """GraphQL type for body composition measurements."""

    id: int
    session_id: int
    body_fat_percentage: float
    body_volume_liters: float
    body_density_kg_per_liter: float
    lean_mass_kg: float | None
    fat_mass_kg: float | None
    mesh_url: str | None
    confidence_score: float | None
    created_at: datetime
    updated_at: datetime


@strawberry.enum
class AnalysisStatusEnum(str, Enum):
    """GraphQL enum for analysis status."""

    PENDING = "pending"
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@strawberry.enum
class GenderEnum(str, Enum):
    """GraphQL enum for gender."""

    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


@strawberry.type
class AnalysisSessionType:
    """GraphQL type for analysis session."""

    id: int
    user_id: int
    job_id: str
    status: AnalysisStatusEnum
    front_image_url: str
    side_image_url: str
    back_image_url: str
    height_cm: float
    weight_kg: float
    age: int
    gender: GenderEnum
    model_used: str | None
    processing_time_seconds: float | None
    error_message: str | None
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime

    # Relationships
    measurements: MeasurementType | None = None


@strawberry.type
class UserWithSessionsType:
    """GraphQL type for User with their analysis sessions."""

    id: int
    email: str
    full_name: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    sessions: list[AnalysisSessionType]


@strawberry.type
class AnalysisStatsType:
    """Statistics for a user's body composition over time."""

    total_analyses: int
    completed_analyses: int
    failed_analyses: int
    average_body_fat: float | None
    average_processing_time: float | None
    first_analysis_date: datetime | None
    last_analysis_date: datetime | None
