#!/usr/bin/env python3
"""Test script for GraphQL API."""

import httpx

GRAPHQL_URL = "http://localhost:8000/graphql"


def execute_query(query: str, variables: dict | None = None) -> dict:
    """Execute a GraphQL query."""
    payload = {"query": query}
    if variables:
        payload["variables"] = variables

    response = httpx.post(GRAPHQL_URL, json=payload, timeout=10.0)
    response.raise_for_status()
    return response.json()


def test_user_query() -> None:
    """Test user query."""
    print("📊 Testing user query...")

    query = """
    query GetUser($email: String!) {
      user(email: $email) {
        id
        email
        fullName
        isActive
        createdAt
      }
    }
    """

    variables = {"email": "test@example.com"}

    try:
        result = execute_query(query, variables)

        if "errors" in result:
            print(f"❌ Query failed: {result['errors']}")
            return

        user = result.get("data", {}).get("user")
        if user:
            print("✅ User found:")
            print(f"   ID: {user['id']}")
            print(f"   Email: {user['email']}")
            print(f"   Active: {user['isActive']}")
            print()
        else:
            print("⚠️  User not found (expected if no data yet)")
            print()

    except Exception as e:
        print(f"❌ Error: {e}\n")


def test_user_sessions() -> None:
    """Test user sessions query."""
    print("📋 Testing user sessions query...")

    query = """
    query GetUserSessions($email: String!, $limit: Int!) {
      userSessions(email: $email, limit: $limit) {
        id
        jobId
        status
        heightCm
        weightKg
        age
        gender
        createdAt
        measurements {
          bodyFatPercentage
          bodyVolumeLiters
          leanMassKg
          fatMassKg
        }
      }
    }
    """

    variables = {"email": "test@example.com", "limit": 5}

    try:
        result = execute_query(query, variables)

        if "errors" in result:
            print(f"❌ Query failed: {result['errors']}")
            return

        sessions = result.get("data", {}).get("userSessions", [])
        print(f"✅ Found {len(sessions)} session(s)")

        for i, session in enumerate(sessions, 1):
            print(f"\n   Session {i}:")
            print(f"     Job ID: {session['jobId']}")
            print(f"     Status: {session['status']}")
            print(f"     Height: {session['heightCm']}cm, Weight: {session['weightKg']}kg")

            if session.get("measurements"):
                m = session["measurements"]
                print(f"     Body Fat: {m['bodyFatPercentage']:.1f}%")
                print(f"     Lean Mass: {m['leanMassKg']:.1f}kg")

        print()

    except Exception as e:
        print(f"❌ Error: {e}\n")


def test_user_stats() -> None:
    """Test user statistics query."""
    print("📈 Testing user statistics query...")

    query = """
    query GetUserStats($email: String!) {
      userStats(email: $email) {
        totalAnalyses
        completedAnalyses
        failedAnalyses
        averageBodyFat
        averageProcessingTime
        firstAnalysisDate
        lastAnalysisDate
      }
    }
    """

    variables = {"email": "test@example.com"}

    try:
        result = execute_query(query, variables)

        if "errors" in result:
            print(f"❌ Query failed: {result['errors']}")
            return

        stats = result.get("data", {}).get("userStats")
        if stats:
            print("✅ User statistics:")
            print(f"   Total Analyses: {stats['totalAnalyses']}")
            print(f"   Completed: {stats['completedAnalyses']}")
            print(f"   Failed: {stats['failedAnalyses']}")

            if stats.get("averageBodyFat"):
                print(f"   Avg Body Fat: {stats['averageBodyFat']:.1f}%")

            if stats.get("averageProcessingTime"):
                print(f"   Avg Processing Time: {stats['averageProcessingTime']:.2f}s")

            print()
        else:
            print("⚠️  No statistics available\n")

    except Exception as e:
        print(f"❌ Error: {e}\n")


def test_analysis_session() -> None:
    """Test analysis session query (if job_id provided)."""
    print("🔍 Testing analysis session query...")
    print("   (Skipped - requires existing job_id)")
    print("   To test: Update the query with a real job_id\n")


def test_combined_query() -> None:
    """Test combined query with multiple fields."""
    print("🔄 Testing combined query...")

    query = """
    query CombinedQuery($email: String!) {
      user(email: $email) {
        id
        email
        fullName
      }

      sessions: userSessions(email: $email, limit: 3) {
        jobId
        status
        createdAt
      }

      stats: userStats(email: $email) {
        totalAnalyses
        completedAnalyses
      }
    }
    """

    variables = {"email": "test@example.com"}

    try:
        result = execute_query(query, variables)

        if "errors" in result:
            print(f"❌ Query failed: {result['errors']}")
            return

        data = result.get("data", {})

        print("✅ Combined query successful:")

        if data.get("user"):
            print(f"   User: {data['user']['email']}")

        sessions = data.get("sessions", [])
        print(f"   Recent Sessions: {len(sessions)}")

        if data.get("stats"):
            stats = data["stats"]
            print(f"   Total Analyses: {stats['totalAnalyses']}")

        print()

    except Exception as e:
        print(f"❌ Error: {e}\n")


def main() -> None:
    """Run all GraphQL tests."""
    print("\n" + "=" * 60)
    print("BodyVision GraphQL API Tests")
    print("=" * 60 + "\n")

    try:
        # Test individual queries
        test_user_query()
        test_user_sessions()
        test_user_stats()
        test_analysis_session()
        test_combined_query()

        print("=" * 60)
        print("✅ GraphQL tests completed!")
        print("=" * 60)
        print("\n💡 Tip: Visit http://localhost:8000/graphql for GraphiQL UI\n")

    except httpx.ConnectError:
        print("\n❌ Could not connect to API server.")
        print("   Make sure the server is running: make dev\n")
        exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}\n")
        exit(1)


if __name__ == "__main__":
    main()
