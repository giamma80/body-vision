"""Test GraphQL API."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.core.database import Base, get_db
from backend.app.main import app
from backend.app.models import AnalysisSession, AnalysisStatus, Gender, Measurement, User

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


@pytest.fixture
def sample_user():
    """Create a sample user in the database."""
    # Tables already created by autouse fixture
    db = TestingSessionLocal()
    try:
        user = User(
            email="test@example.com",
            full_name="Test User",
            is_active=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        # Return a dict with user data to avoid SQLAlchemy detached instance issues
        user_data = {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "is_active": user.is_active
        }
        return type('User', (), user_data)()  # Convert dict to object
    finally:
        db.close()


def test_graphql_endpoint_accessible(client: TestClient) -> None:
    """Test that GraphQL endpoint is accessible."""
    response = client.get("/graphql")
    assert response.status_code == 200
    # GraphiQL UI should be served
    assert b"GraphiQL" in response.content or b"graphql" in response.content


def test_user_query_not_found(client: TestClient) -> None:
    """Test user query when user doesn't exist."""
    query = """
    query GetUser($email: String!) {
      user(email: $email) {
        id
        email
      }
    }
    """

    response = client.post(
        "/graphql",
        json={"query": query, "variables": {"email": "nonexistent@example.com"}},
    )

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert data["data"]["user"] is None


def test_user_query_success(client: TestClient, sample_user) -> None:
    """Test successful user query."""
    query = """
    query GetUser($email: String!) {
      user(email: $email) {
        id
        email
        fullName
        isActive
      }
    }
    """

    response = client.post(
        "/graphql",
        json={"query": query, "variables": {"email": sample_user.email}},
    )

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert data["data"]["user"]["id"] == sample_user.id
    assert data["data"]["user"]["email"] == sample_user.email
    assert data["data"]["user"]["fullName"] == "Test User"
    assert data["data"]["user"]["isActive"] is True


def test_user_sessions_query_empty(client: TestClient, sample_user) -> None:
    """Test user sessions query with no sessions."""
    query = """
    query GetUserSessions($email: String!) {
      userSessions(email: $email, limit: 10) {
        id
        jobId
        status
      }
    }
    """

    response = client.post(
        "/graphql",
        json={"query": query, "variables": {"email": sample_user.email}},
    )

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert data["data"]["userSessions"] == []


def test_user_stats_query(client: TestClient, sample_user) -> None:
    """Test user stats query."""
    query = """
    query GetUserStats($email: String!) {
      userStats(email: $email) {
        totalAnalyses
        completedAnalyses
        failedAnalyses
      }
    }
    """

    response = client.post(
        "/graphql",
        json={"query": query, "variables": {"email": sample_user.email}},
    )

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    stats = data["data"]["userStats"]
    assert stats["totalAnalyses"] == 0
    assert stats["completedAnalyses"] == 0
    assert stats["failedAnalyses"] == 0


def test_introspection_query(client: TestClient) -> None:
    """Test GraphQL introspection."""
    query = """
    {
      __schema {
        types {
          name
        }
      }
    }
    """

    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "__schema" in data["data"]
    assert len(data["data"]["__schema"]["types"]) > 0
