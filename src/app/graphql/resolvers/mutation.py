from __future__ import annotations

import strawberry

from app.graphql.inputs.models import OrderInput, PetInput, UserInput
from app.graphql.mappers import (
    map_api_response,
    map_order,
    map_pet,
    order_input_to_dict,
    pet_input_to_dict,
    user_input_to_dict,
)
from app.graphql.resolvers.utils import get_rest_client, handle_rest_error
from app.graphql.rest_client import RestError
from app.graphql.types.models import ApiResponse, Order, Pet


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def add_pet(self, info: strawberry.Info, input: PetInput) -> Pet:
        try:
            payload = await get_rest_client(info).add_pet(pet_input_to_dict(input))
            return map_pet(payload)
        except RestError as exc:
            raise handle_rest_error(exc) from exc

    @strawberry.mutation
    async def update_pet(self, info: strawberry.Info, input: PetInput) -> Pet:
        try:
            payload = await get_rest_client(info).update_pet(pet_input_to_dict(input))
            return map_pet(payload)
        except RestError as exc:
            raise handle_rest_error(exc) from exc

    @strawberry.mutation
    async def update_pet_with_form(
        self,
        info: strawberry.Info,
        pet_id: int,
        name: str | None = None,
        status: str | None = None,
    ) -> ApiResponse:
        try:
            payload = await get_rest_client(info).update_pet_with_form(pet_id, name, status)
            return map_api_response(payload, default_message="pet updated")
        except RestError as exc:
            raise handle_rest_error(exc) from exc

    @strawberry.mutation
    async def delete_pet(
        self,
        info: strawberry.Info,
        pet_id: int,
        api_key: str | None = None,
    ) -> ApiResponse:
        try:
            payload = await get_rest_client(info).delete_pet(pet_id, api_key)
            return map_api_response(payload, default_message="pet deleted")
        except RestError as exc:
            raise handle_rest_error(exc) from exc

    @strawberry.mutation
    async def upload_pet_image(
        self,
        info: strawberry.Info,
        pet_id: int,
        additional_metadata: str | None = None,
        content: str | None = None,
    ) -> ApiResponse:
        try:
            body = content.encode() if content is not None else None
            payload = await get_rest_client(info).upload_file(pet_id, additional_metadata, body)
            return map_api_response(payload)
        except RestError as exc:
            raise handle_rest_error(exc) from exc

    @strawberry.mutation
    async def place_order(self, info: strawberry.Info, input: OrderInput) -> Order:
        try:
            payload = await get_rest_client(info).place_order(order_input_to_dict(input))
            return map_order(payload)
        except RestError as exc:
            raise handle_rest_error(exc) from exc

    @strawberry.mutation
    async def delete_order(self, info: strawberry.Info, order_id: int) -> ApiResponse:
        try:
            payload = await get_rest_client(info).delete_order(order_id)
            return map_api_response(payload, default_message="order deleted")
        except RestError as exc:
            raise handle_rest_error(exc) from exc

    @strawberry.mutation
    async def create_user(self, info: strawberry.Info, input: UserInput) -> ApiResponse:
        try:
            payload = await get_rest_client(info).create_user(user_input_to_dict(input))
            return map_api_response(payload, default_message="user created")
        except RestError as exc:
            raise handle_rest_error(exc) from exc

    @strawberry.mutation
    async def create_users_with_list(
        self,
        info: strawberry.Info,
        input: list[UserInput],
    ) -> ApiResponse:
        try:
            payload = await get_rest_client(info).create_users_with_list(
                [user_input_to_dict(user) for user in input]
            )
            return map_api_response(payload, default_message="users created")
        except RestError as exc:
            raise handle_rest_error(exc) from exc

    @strawberry.mutation
    async def update_user(
        self,
        info: strawberry.Info,
        username: str,
        input: UserInput,
    ) -> ApiResponse:
        try:
            payload = await get_rest_client(info).update_user(username, user_input_to_dict(input))
            return map_api_response(payload, default_message="user updated")
        except RestError as exc:
            raise handle_rest_error(exc) from exc

    @strawberry.mutation
    async def delete_user(self, info: strawberry.Info, username: str) -> ApiResponse:
        try:
            payload = await get_rest_client(info).delete_user(username)
            return map_api_response(payload, default_message="user deleted")
        except RestError as exc:
            raise handle_rest_error(exc) from exc
