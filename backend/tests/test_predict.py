"""Test prediction endpoints."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.core.database import Base, get_db
from backend.app.main import app

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Override database dependency
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    """Create tables before each test and drop after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


def test_health_endpoint(client: TestClient) -> None:
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "model" in data


def test_create_prediction_validates_input(client: TestClient) -> None:
    """Test prediction creation validates input."""
    # Missing required fields
    response = client.post("/api/predict/", json={})
    assert response.status_code == 422  # Validation error

    # Invalid height
    response = client.post(
        "/api/predict/",
        json={
            "front_image_url": "https://example.com/front.jpg",
            "side_image_url": "https://example.com/side.jpg",
            "back_image_url": "https://example.com/back.jpg",
            "user_metadata": {
                "email": "test@example.com",
                "height_cm": 10,  # Too low
                "weight_kg": 75,
                "age": 30,
                "gender": "male",
            },
        },
    )
    assert response.status_code == 422


def test_get_nonexistent_job(client: TestClient) -> None:
    """Test getting status for non-existent job."""
    response = client.get("/api/predict/nonexistent-job-id")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
