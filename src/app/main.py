from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from app.context import get_context
from app.schema import schema

app = FastAPI(title="petstore-graphql")
app.include_router(GraphQLRouter(schema, context_getter=get_context), prefix="/graphql")
