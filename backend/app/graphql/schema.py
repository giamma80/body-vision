"""GraphQL schema for BodyVision."""

import strawberry

from app.graphql.queries import Query

# Create the GraphQL schema
schema = strawberry.Schema(
    query=Query,
    # Enable GraphiQL in development
    # mutation=Mutation,  # Add later if needed
)
