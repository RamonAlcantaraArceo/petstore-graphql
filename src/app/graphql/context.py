from __future__ import annotations

from app.config import settings
from app.graphql.loaders.pet_loader import build_pet_loader
from app.graphql.rest_client import RestClient

_rest_client: RestClient | None = None


def _get_or_create_rest_client() -> RestClient:
    global _rest_client
    if _rest_client is None:
        _rest_client = RestClient(base_url=settings.petstore_base_url)
    return _rest_client


async def get_context() -> dict[str, object]:
    rest_client = _get_or_create_rest_client()
    return {
        "rest_client": rest_client,
        "pet_loader": build_pet_loader(rest_client),
    }


async def close_rest_client() -> None:
    global _rest_client
    if _rest_client is None:
        return
    await _rest_client.close()
    _rest_client = None
