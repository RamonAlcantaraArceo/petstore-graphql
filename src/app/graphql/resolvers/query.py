from __future__ import annotations

import strawberry

from app.config import settings
from app.graphql.mappers import map_order, map_pet, map_user
from app.graphql.resolvers.utils import get_rest_client, handle_rest_error, paginate_pets
from app.graphql.rest_client import RestError
from app.graphql.types.models import (
    HealthDetails,
    HealthResponse,
    InventoryEntry,
    Order,
    Pet,
    PetConnection,
    PetStatus,
    User,
)


@strawberry.type
class Query:
    @strawberry.field
    def health(self) -> HealthResponse:
        return HealthResponse(
            status="ok",
            mode=settings.mode,
            details=HealthDetails(
                version=settings.version,
                build_date=settings.build_date,
                git_commit_sha=settings.git_commit_sha,
            ),
        )

    @strawberry.field
    async def pet(self, info: strawberry.Info, pet_id: int) -> Pet | None:
        try:
            payload = await get_rest_client(info).get_pet_by_id(pet_id)
            return map_pet(payload)
        except RestError as exc:
            if exc.status_code == 404:
                return None
            raise handle_rest_error(exc) from exc

    @strawberry.field
    async def pets_by_status(self, info: strawberry.Info, status: PetStatus) -> list[Pet]:
        try:
            payload = await get_rest_client(info).find_pets_by_status(status.value)
            return [map_pet(item) for item in payload]
        except RestError as exc:
            raise handle_rest_error(exc) from exc

    @strawberry.field
    async def pets_by_status_connection(
        self,
        info: strawberry.Info,
        status: PetStatus,
        first: int | None = 20,
        after: int | None = 0,
    ) -> PetConnection:
        pets = await self.pets_by_status(info, status)
        return paginate_pets(pets, first, after)

    @strawberry.field
    async def pets_by_tags(self, info: strawberry.Info, tags: list[str]) -> list[Pet]:
        try:
            payload = await get_rest_client(info).find_pets_by_tags(tags)
            return [map_pet(item) for item in payload]
        except RestError as exc:
            raise handle_rest_error(exc) from exc

    @strawberry.field
    async def pets_by_tags_connection(
        self,
        info: strawberry.Info,
        tags: list[str],
        first: int | None = 20,
        after: int | None = 0,
    ) -> PetConnection:
        pets = await self.pets_by_tags(info, tags)
        return paginate_pets(pets, first, after)

    @strawberry.field
    async def store_inventory(self, info: strawberry.Info) -> list[InventoryEntry]:
        try:
            payload = await get_rest_client(info).get_inventory()
            return [InventoryEntry(status=key, count=value) for key, value in payload.items()]
        except RestError as exc:
            raise handle_rest_error(exc) from exc

    @strawberry.field
    async def order(self, info: strawberry.Info, order_id: int) -> Order | None:
        try:
            payload = await get_rest_client(info).get_order_by_id(order_id)
            return map_order(payload)
        except RestError as exc:
            if exc.status_code == 404:
                return None
            raise handle_rest_error(exc) from exc

    @strawberry.field
    async def user(self, info: strawberry.Info, username: str) -> User | None:
        try:
            payload = await get_rest_client(info).get_user_by_name(username)
            return map_user(payload)
        except RestError as exc:
            if exc.status_code == 404:
                return None
            raise handle_rest_error(exc) from exc

    @strawberry.field
    async def login(self, info: strawberry.Info, username: str, password: str) -> str:
        try:
            return await get_rest_client(info).login_user(username, password)
        except RestError as exc:
            raise handle_rest_error(exc) from exc

    @strawberry.field
    async def logout(self, info: strawberry.Info) -> str:
        try:
            return await get_rest_client(info).logout_user()
        except RestError as exc:
            raise handle_rest_error(exc) from exc
