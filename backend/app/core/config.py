"""Application configuration using Pydantic Settings."""

from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Application
    APP_NAME: str = "BodyVision"
    APP_ENV: Literal["development", "staging", "production"] = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4

    # Database
    DATABASE_URL: str = Field(
        default="postgresql://user:password@localhost:5432/bodyvision",
        description="PostgreSQL connection string",
    )
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    # Supabase
    SUPABASE_URL: str = Field(default="", description="Supabase project URL")
    SUPABASE_ANON_KEY: str = Field(default="", description="Supabase anon key")
    SUPABASE_SERVICE_ROLE_KEY: str = Field(default="", description="Supabase service role key")
    SUPABASE_STORAGE_BUCKET: str = "bodyvision-images"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Body Model
    BODYVISION_MODEL: Literal["smplx", "star", "ghum"] = Field(
        default="smplx",
        description="Body model to use for inference",
    )

    # Security
    SECRET_KEY: str = Field(
        default="your-secret-key-change-in-production",
        description="Secret key for JWT and encryption",
    )
    ALLOWED_ORIGINS: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        description="CORS allowed origins",
    )

    # ML / Inference
    MODEL_CACHE_DIR: str = "./models"
    ENABLE_GPU: bool = False
    TORCH_DEVICE: Literal["cpu", "cuda", "mps"] = "cpu"

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: str | list[str]) -> list[str]:
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v


# Global settings instance
settings = Settings()
