from __future__ import annotations

import asyncio

from strawberry.dataloader import DataLoader

from app.graphql.mappers import map_pet
from app.graphql.rest_client import RestClient
from app.graphql.types.models import Pet


def build_pet_loader(rest_client: RestClient) -> DataLoader[int, Pet | None]:
    async def load_fn(keys: list[int]) -> list[Pet | None]:
        tasks = [rest_client.get_pet_by_id(key) for key in keys]
        raw_results = await asyncio.gather(*tasks, return_exceptions=True)
        pets: list[Pet | None] = []
        for item in raw_results:
            if isinstance(item, Exception):
                pets.append(None)
            else:
                pets.append(map_pet(item))
        return pets

    return DataLoader(load_fn=load_fn)
