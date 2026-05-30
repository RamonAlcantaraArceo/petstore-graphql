"""Petstore mutation resolvers (POST/PUT/DELETE endpoints from openapi.json)."""

from __future__ import annotations

import strawberry
from strawberry.types import Info

from app.petstore.inputs import (
    OrderInput,
    PetInput,
    UserInput,
    order_input_to_dict,
    pet_input_to_dict,
    user_input_to_dict,
)
from app.petstore.types import Order, Pet, User, parse_order, parse_pet, parse_user


@strawberry.type
class PetstoreMutation:
    # ------------------------------------------------------------------ pet --

    @strawberry.mutation
    async def add_pet(self, pet: PetInput, info: Info) -> Pet:
        """Add a new pet to the store (POST /pet)."""
        data = await info.context.rest_client.add_pet(pet_input_to_dict(pet))
        return parse_pet(data)

    @strawberry.mutation
    async def update_pet(self, pet: PetInput, info: Info) -> Pet:
        """Update an existing pet (PUT /pet)."""
        data = await info.context.rest_client.update_pet(pet_input_to_dict(pet))
        return parse_pet(data)

    @strawberry.mutation
    async def delete_pet(self, id: int, info: Info) -> bool:
        """Delete a pet by ID (DELETE /pet/{petId}). Returns true on success."""
        try:
            await info.context.rest_client.delete_pet(id)
            return True
        except Exception:  # noqa: BLE001
            return False

    # --------------------------------------------------------------- store --

    @strawberry.mutation
    async def place_order(self, order: OrderInput, info: Info) -> Order:
        """Place a new order for a pet (POST /store/order)."""
        data = await info.context.rest_client.place_order(order_input_to_dict(order))
        return parse_order(data)

    @strawberry.mutation
    async def delete_order(self, id: int, info: Info) -> bool:
        """Delete a purchase order (DELETE /store/order/{orderId}). Returns true on success."""
        try:
            await info.context.rest_client.delete_order(id)
            return True
        except Exception:  # noqa: BLE001
            return False

    # ----------------------------------------------------------------- user --

    @strawberry.mutation
    async def create_user(self, user: UserInput, info: Info) -> User | None:
        """Create a new user account (POST /user)."""
        data = await info.context.rest_client.create_user(user_input_to_dict(user))
        return parse_user(data)

    @strawberry.mutation
    async def update_user(self, username: str, user: UserInput, info: Info) -> bool:
        """Update an existing user (PUT /user/{username}). Returns true on success."""
        try:
            await info.context.rest_client.update_user(username, user_input_to_dict(user))
            return True
        except Exception:  # noqa: BLE001
            return False

    @strawberry.mutation
    async def delete_user(self, username: str, info: Info) -> bool:
        """Delete a user account (DELETE /user/{username}). Returns true on success."""
        try:
            await info.context.rest_client.delete_user(username)
            return True
        except Exception:  # noqa: BLE001
            return False

    @strawberry.mutation
    async def logout_user(self, info: Info) -> bool:
        """Log out the current user session (GET /user/logout). Returns true on success."""
        try:
            await info.context.rest_client.logout_user()
            return True
        except Exception:  # noqa: BLE001
            return False
