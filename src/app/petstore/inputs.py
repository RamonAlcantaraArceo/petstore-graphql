"""Input types for Petstore mutations (converted from OpenAPI requestBody schemas)."""

from __future__ import annotations

import strawberry


@strawberry.input
class CategoryInput:
    id: int | None = None
    name: str | None = None


@strawberry.input
class TagInput:
    id: int | None = None
    name: str | None = None


@strawberry.input
class PetInput:
    name: str
    photo_urls: list[str]
    id: int | None = None
    category: CategoryInput | None = None
    tags: list[TagInput] | None = None
    status: str | None = None  # "available" | "pending" | "sold"


@strawberry.input
class OrderInput:
    pet_id: int | None = None
    quantity: int | None = None
    ship_date: str | None = None
    status: str | None = None  # "placed" | "approved" | "delivered"
    complete: bool | None = None


@strawberry.input
class UserInput:
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    password: str | None = None
    phone: str | None = None
    user_status: int | None = None
    id: int | None = None


# ------------------------------------------------- input → dict serialisers --


def pet_input_to_dict(inp: PetInput) -> dict:
    data: dict = {"name": inp.name, "photoUrls": inp.photo_urls}
    if inp.id is not None:
        data["id"] = inp.id
    if inp.category is not None:
        data["category"] = {"id": inp.category.id, "name": inp.category.name}
    if inp.tags is not None:
        data["tags"] = [{"id": t.id, "name": t.name} for t in inp.tags]
    if inp.status is not None:
        data["status"] = inp.status
    return data


def order_input_to_dict(inp: OrderInput) -> dict:
    data: dict = {}
    if inp.pet_id is not None:
        data["petId"] = inp.pet_id
    if inp.quantity is not None:
        data["quantity"] = inp.quantity
    if inp.ship_date is not None:
        data["shipDate"] = inp.ship_date
    if inp.status is not None:
        data["status"] = inp.status
    if inp.complete is not None:
        data["complete"] = inp.complete
    return data


def user_input_to_dict(inp: UserInput) -> dict:
    data: dict = {}
    if inp.id is not None:
        data["id"] = inp.id
    if inp.username is not None:
        data["username"] = inp.username
    if inp.first_name is not None:
        data["firstName"] = inp.first_name
    if inp.last_name is not None:
        data["lastName"] = inp.last_name
    if inp.email is not None:
        data["email"] = inp.email
    if inp.password is not None:
        data["password"] = inp.password
    if inp.phone is not None:
        data["phone"] = inp.phone
    if inp.user_status is not None:
        data["userStatus"] = inp.user_status
    return data
