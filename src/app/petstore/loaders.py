"""DataLoaders for avoiding N+1 REST calls in nested resolvers."""

from __future__ import annotations

from strawberry.dataloader import DataLoader

from app.petstore.rest_client import PetstoreClient
from app.petstore.types import Pet, parse_pet


def make_pet_loader(client: PetstoreClient) -> DataLoader[int, Pet | None]:
    """Return a DataLoader that fetches pets by ID, one request per unique ID.

    The Petstore REST API has no batch-by-ID endpoint, so each ID results in
    one HTTP call.  The DataLoader still deduplates within a single request
    and caches within the same GraphQL operation.
    """

    async def batch_load_pets(pet_ids: list[int]) -> list[Pet | None | BaseException]:
        results: list[Pet | None | BaseException] = []
        for pet_id in pet_ids:
            try:
                data = await client.get_pet_by_id(pet_id)
                results.append(parse_pet(data))
            except Exception as exc:  # noqa: BLE001
                results.append(exc)
        return results

    return DataLoader(load_fn=batch_load_pets)
