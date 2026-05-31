from __future__ import annotations

import strawberry

from app.graphql.types.models import OrderStatus, PetStatus


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
    id: int | None = None
    name: str
    category: CategoryInput | None = None
    photo_urls: list[str]
    tags: list[TagInput] | None = None
    status: PetStatus | None = None


@strawberry.input
class OrderInput:
    id: int | None = None
    pet_id: int | None = None
    quantity: int | None = None
    ship_date: str | None = None
    status: OrderStatus | None = None
    complete: bool | None = None


@strawberry.input
class UserInput:
    id: int | None = None
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    password: str | None = None
    phone: str | None = None
    user_status: int | None = None


__all__ = [
    "CategoryInput",
    "OrderInput",
    "PetInput",
    "TagInput",
    "UserInput",
]
