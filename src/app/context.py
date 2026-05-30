"""Per-request application context holding the REST client and DataLoaders."""

from __future__ import annotations

from strawberry.dataloader import DataLoader
from strawberry.fastapi import BaseContext

from app.config import settings
from app.petstore.loaders import make_pet_loader
from app.petstore.rest_client import PetstoreClient
from app.petstore.types import Pet


class AppContext(BaseContext):
    """Carries the REST client and DataLoader instances for one GraphQL request."""

    rest_client: PetstoreClient
    pet_loader: DataLoader[int, Pet | None]

    def __init__(self, rest_client: PetstoreClient | None = None) -> None:
        super().__init__()
        self.rest_client = rest_client or PetstoreClient(
            base_url=settings.petstore_base_url
        )
        self.pet_loader = make_pet_loader(self.rest_client)


async def get_context() -> AppContext:
    """FastAPI dependency that creates a fresh context per request."""
    return AppContext()


__all__ = ["AppContext", "get_context"]
