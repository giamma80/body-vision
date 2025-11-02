# GraphQL Query Examples

This document contains example GraphQL queries for the BodyVision API.

**GraphQL Endpoint:** http://localhost:8000/graphql

**GraphiQL UI:** http://localhost:8000/graphql (browser)

---

## Getting Started

### Access GraphiQL

1. Start the API server:
   ```bash
   make dev
   ```

2. Open browser to: http://localhost:8000/graphql

3. You'll see the GraphiQL interface with:
   - Query editor (left)
   - Results (middle)
   - Documentation explorer (right)

---

## Example Queries

### 1. Get User by Email

```graphql
query GetUser {
  user(email: "test@example.com") {
    id
    email
    fullName
    isActive
    createdAt
    updatedAt
  }
}
```

### 2. Get Analysis Session by Job ID

```graphql
query GetAnalysisSession {
  analysisSession(jobId: "your-job-id-here") {
    id
    jobId
    status
    frontImageUrl
    sideImageUrl
    backImageUrl
    heightCm
    weightKg
    age
    gender
    modelUsed
    processingTimeSeconds
    errorMessage
    startedAt
    completedAt
    createdAt
    measurements {
      id
      bodyFatPercentage
      bodyVolumeLiters
      bodyDensityKgPerLiter
      leanMassKg
      fatMassKg
      confidenceScore
      meshUrl
    }
  }
}
```

### 3. Get User's Recent Sessions

```graphql
query GetUserSessions {
  userSessions(
    email: "test@example.com"
    limit: 10
    offset: 0
  ) {
    id
    jobId
    status
    heightCm
    weightKg
    age
    gender
    processingTimeSeconds
    createdAt
    measurements {
      bodyFatPercentage
      bodyVolumeLiters
      leanMassKg
      fatMassKg
    }
  }
}
```

### 4. Get User Sessions Filtered by Status

```graphql
query GetCompletedSessions {
  userSessions(
    email: "test@example.com"
    status: COMPLETED
    limit: 5
  ) {
    id
    jobId
    status
    completedAt
    measurements {
      bodyFatPercentage
      bodyVolumeLiters
      bodyDensityKgPerLiter
    }
  }
}
```

**Available status values:**
- `PENDING`
- `QUEUED`
- `PROCESSING`
- `COMPLETED`
- `FAILED`

### 5. Get User with Sessions (Combined)

```graphql
query GetUserWithSessions {
  userWithSessions(email: "test@example.com", limit: 5) {
    id
    email
    fullName
    createdAt
    sessions {
      id
      jobId
      status
      heightCm
      weightKg
      createdAt
      measurements {
        bodyFatPercentage
        leanMassKg
        fatMassKg
      }
    }
  }
}
```

### 6. Get User Statistics

```graphql
query GetUserStats {
  userStats(email: "test@example.com") {
    totalAnalyses
    completedAnalyses
    failedAnalyses
    averageBodyFat
    averageProcessingTime
    firstAnalysisDate
    lastAnalysisDate
  }
}
```

### 7. Get Latest Measurements

```graphql
query GetLatestMeasurements {
  latestMeasurements(email: "test@example.com", limit: 5) {
    id
    sessionId
    bodyFatPercentage
    bodyVolumeLiters
    bodyDensityKgPerLiter
    leanMassKg
    fatMassKg
    confidenceScore
    createdAt
  }
}
```

---

## Complex Queries

### Complete User Analysis History

```graphql
query CompleteUserHistory {
  user: userWithSessions(email: "test@example.com", limit: 20) {
    id
    email
    fullName
    sessions {
      id
      jobId
      status
      heightCm
      weightKg
      age
      gender
      createdAt
      completedAt
      processingTimeSeconds
      measurements {
        bodyFatPercentage
        bodyVolumeLiters
        bodyDensityKgPerLiter
        leanMassKg
        fatMassKg
        confidenceScore
      }
    }
  }

  stats: userStats(email: "test@example.com") {
    totalAnalyses
    completedAnalyses
    failedAnalyses
    averageBodyFat
    averageProcessingTime
  }
}
```

### Track Body Composition Over Time

```graphql
query BodyCompositionTrend {
  latestMeasurements(email: "test@example.com", limit: 10) {
    bodyFatPercentage
    leanMassKg
    fatMassKg
    createdAt
  }
}
```

---

## Query Variables

You can use variables to make queries reusable:

```graphql
query GetUserSessions($email: String!, $limit: Int = 10) {
  userSessions(email: $email, limit: $limit) {
    id
    jobId
    status
    createdAt
    measurements {
      bodyFatPercentage
    }
  }
}
```

**Variables (in GraphiQL):**
```json
{
  "email": "test@example.com",
  "limit": 5
}
```

---

## Introspection Query

Get the complete GraphQL schema:

```graphql
query IntrospectionQuery {
  __schema {
    types {
      name
      kind
      description
    }
  }
}
```

---

## Error Handling

GraphQL returns errors in a structured format:

```json
{
  "data": null,
  "errors": [
    {
      "message": "User not found",
      "locations": [{"line": 2, "column": 3}],
      "path": ["user"]
    }
  ]
}
```

---

## Performance Tips

### 1. Request Only Needed Fields

❌ **Bad** - Requesting all fields:
```graphql
query GetSessions {
  userSessions(email: "test@example.com") {
    id
    jobId
    status
    frontImageUrl
    sideImageUrl
    backImageUrl
    heightCm
    weightKg
    # ... all fields
  }
}
```

✅ **Good** - Request only what you need:
```graphql
query GetSessions {
  userSessions(email: "test@example.com") {
    jobId
    status
    createdAt
  }
}
```

### 2. Use Pagination

```graphql
query PaginatedSessions($email: String!, $offset: Int!, $limit: Int!) {
  userSessions(email: $email, offset: $offset, limit: $limit) {
    id
    status
    createdAt
  }
}
```

### 3. Filter Early

Use status filters to reduce data:
```graphql
query CompletedOnly {
  userSessions(email: "test@example.com", status: COMPLETED, limit: 5) {
    jobId
    measurements {
      bodyFatPercentage
    }
  }
}
```

---

## Testing with curl

```bash
# Simple query
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{ user(email: \"test@example.com\") { id email } }"
  }'

# With variables
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "query GetUser($email: String!) { user(email: $email) { id email } }",
    "variables": {"email": "test@example.com"}
  }'
```

---

## Python Client Example

```python
import httpx

GRAPHQL_URL = "http://localhost:8000/graphql"

query = """
query GetUserStats($email: String!) {
  userStats(email: $email) {
    totalAnalyses
    completedAnalyses
    averageBodyFat
  }
}
"""

variables = {"email": "test@example.com"}

response = httpx.post(
    GRAPHQL_URL,
    json={"query": query, "variables": variables}
)

data = response.json()
print(data["data"]["userStats"])
```

---

## Next Steps

- Explore the schema in GraphiQL's Documentation Explorer (right panel)
- Try combining multiple queries in one request
- Use fragments to reuse field selections
- Implement mutations (coming soon) for data modification

---

Last Updated: 2025-11-02
