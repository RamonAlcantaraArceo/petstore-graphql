"""Strawberry GraphQL types that mirror the OpenAPI domain model."""

from __future__ import annotations

import enum

import strawberry


@strawberry.enum
class PetStatus(enum.Enum):
    available = "available"
    pending = "pending"
    sold = "sold"


@strawberry.enum
class OrderStatus(enum.Enum):
    placed = "placed"
    approved = "approved"
    delivered = "delivered"


@strawberry.type
class Category:
    id: int | None = None
    name: str | None = None


@strawberry.type
class Tag:
    id: int | None = None
    name: str | None = None


@strawberry.type
class Pet:
    id: int | None
    name: str
    photo_urls: list[str]
    category: Category | None
    tags: list[Tag] | None
    status: PetStatus | None


@strawberry.type
class Order:
    id: int | None
    pet_id: int | None
    quantity: int | None
    ship_date: str | None
    status: OrderStatus | None
    complete: bool | None


@strawberry.type
class User:
    id: int | None
    username: str | None
    first_name: str | None
    last_name: str | None
    email: str | None
    phone: str | None
    user_status: int | None


@strawberry.type
class InventoryEntry:
    status: str
    count: int


# ------------------------------------------------------------------ parsers --


def parse_category(data: dict) -> Category:
    return Category(id=data.get("id"), name=data.get("name"))


def parse_tag(data: dict) -> Tag:
    return Tag(id=data.get("id"), name=data.get("name"))


def parse_pet(data: dict) -> Pet:
    raw_status = data.get("status")
    status: PetStatus | None = None
    if raw_status in ("available", "pending", "sold"):
        status = PetStatus(raw_status)
    return Pet(
        id=data.get("id"),
        name=data["name"],
        photo_urls=data.get("photoUrls", []),
        category=parse_category(data["category"]) if data.get("category") else None,
        tags=[parse_tag(t) for t in data.get("tags", [])] if data.get("tags") else None,
        status=status,
    )


def parse_order(data: dict) -> Order:
    raw_status = data.get("status")
    status: OrderStatus | None = None
    if raw_status in ("placed", "approved", "delivered"):
        status = OrderStatus(raw_status)
    return Order(
        id=data.get("id"),
        pet_id=data.get("petId"),
        quantity=data.get("quantity"),
        ship_date=data.get("shipDate"),
        status=status,
        complete=data.get("complete"),
    )


def parse_user(data: dict) -> User:
    return User(
        id=data.get("id"),
        username=data.get("username"),
        first_name=data.get("firstName"),
        last_name=data.get("lastName"),
        email=data.get("email"),
        phone=data.get("phone"),
        user_status=data.get("userStatus"),
    )


def parse_inventory(data: dict[str, int]) -> list[InventoryEntry]:
    return [InventoryEntry(status=k, count=v) for k, v in data.items()]
