"""Test main application endpoints."""

import pytest
from fastapi.testclient import TestClient

from backend.app.main import app


@pytest.fixture
def client() -> TestClient:
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


def test_docs_available_in_dev(client: TestClient) -> None:
    """Test that API docs are available in development."""
    response = client.get("/docs")
    assert response.status_code == 200
