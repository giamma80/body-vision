"""GraphQL endpoint configuration."""

from strawberry.fastapi import GraphQLRouter

from app.graphql.schema import schema

# Create GraphQL router with GraphiQL enabled in development
graphql_router = GraphQLRouter(
    schema,
    graphiql=True,  # Enable GraphiQL UI
    path="/graphql",
)
