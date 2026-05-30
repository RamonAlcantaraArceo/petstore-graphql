"""Petstore query resolvers (GET endpoints from openapi.json)."""

from __future__ import annotations

import strawberry
from strawberry.types import Info

from app.petstore.types import (
    InventoryEntry,
    Order,
    Pet,
    PetStatus,
    User,
    parse_inventory,
    parse_order,
    parse_pet,
    parse_user,
)


@strawberry.type
class PetstoreQuery:
    # ------------------------------------------------------------------ pet --

    @strawberry.field
    async def pet(self, id: int, info: Info) -> Pet | None:
        """Fetch a single pet by its ID (GET /pet/{petId})."""
        try:
            return await info.context.pet_loader.load(id)
        except Exception:  # noqa: BLE001
            return None

    @strawberry.field
    async def pets_by_status(
        self,
        status: PetStatus = PetStatus.available,
        info: Info = strawberry.UNSET,  # type: ignore[assignment]
    ) -> list[Pet]:
        """Find pets by status (GET /pet/findByStatus)."""
        data = await info.context.rest_client.find_pets_by_status(status.value)
        return [parse_pet(p) for p in data]

    @strawberry.field
    async def pets_by_tags(
        self,
        tags: list[str],
        info: Info = strawberry.UNSET,  # type: ignore[assignment]
    ) -> list[Pet]:
        """Find pets by tags (GET /pet/findByTags)."""
        data = await info.context.rest_client.find_pets_by_tags(tags)
        return [parse_pet(p) for p in data]

    # --------------------------------------------------------------- store --

    @strawberry.field
    async def inventory(self, info: Info) -> list[InventoryEntry]:
        """Return inventory counts grouped by status (GET /store/inventory)."""
        data = await info.context.rest_client.get_inventory()
        return parse_inventory(data)

    @strawberry.field
    async def order(self, id: int, info: Info) -> Order | None:
        """Fetch a single order by its ID (GET /store/order/{orderId})."""
        try:
            data = await info.context.rest_client.get_order_by_id(id)
            return parse_order(data)
        except Exception:  # noqa: BLE001
            return None

    # ----------------------------------------------------------------- user --

    @strawberry.field
    async def user(self, username: str, info: Info) -> User | None:
        """Fetch a user by username (GET /user/{username})."""
        try:
            data = await info.context.rest_client.get_user_by_username(username)
            return parse_user(data)
        except Exception:  # noqa: BLE001
            return None

    @strawberry.field
    async def user_login(
        self,
        username: str,
        password: str,
        info: Info = strawberry.UNSET,  # type: ignore[assignment]
    ) -> str | None:
        """Log a user in and return a session token (GET /user/login)."""
        try:
            return await info.context.rest_client.login_user(username, password)
        except Exception:  # noqa: BLE001
            return None
