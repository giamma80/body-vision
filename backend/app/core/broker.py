"""Dramatiq broker configuration for background tasks."""

import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.results import Results
from dramatiq.results.backends import RedisBackend
from loguru import logger

from app.core.config import settings

# Initialize Redis broker
redis_broker = RedisBroker(url=settings.REDIS_URL)

# Enable results backend for tracking job status
result_backend = RedisBackend(url=settings.REDIS_URL)
redis_broker.add_middleware(Results(backend=result_backend))

# Set as default broker
dramatiq.set_broker(redis_broker)

logger.info(f"Dramatiq broker initialized with Redis at {settings.REDIS_URL}")
