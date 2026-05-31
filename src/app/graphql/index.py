from __future__ import annotations

import strawberry
from strawberry.schema.config import StrawberryConfig

from app.graphql.resolvers import Mutation, Query

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    config=StrawberryConfig(auto_camel_case=False),
)
