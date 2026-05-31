from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from app.graphql.context import close_rest_client, get_context
from app.graphql.index import schema


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    yield
    await close_rest_client()


app = FastAPI(title="petstore-graphql", lifespan=lifespan)
app.include_router(GraphQLRouter(schema, context_getter=get_context), prefix="/graphql")
