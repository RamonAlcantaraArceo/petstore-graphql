from __future__ import annotations

from enum import Enum

import strawberry
from strawberry.types import Info

from app.graphql.context_access import get_pet_loader


@strawberry.enum
class PetStatus(Enum):
    AVAILABLE = "available"
    PENDING = "pending"
    SOLD = "sold"


@strawberry.enum
class OrderStatus(Enum):
    PLACED = "placed"
    APPROVED = "approved"
    DELIVERED = "delivered"


@strawberry.type
class HealthDetails:
    version: str
    build_date: str
    git_commit_sha: str


@strawberry.type
class HealthResponse:
    status: str
    mode: str
    details: HealthDetails


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
    id: int | None = None
    name: str
    category: Category | None = None
    photo_urls: list[str]
    tags: list[Tag] | None = None
    status: PetStatus | None = None


@strawberry.type
class Order:
    id: int | None = None
    pet_id: int | None = None
    quantity: int | None = None
    ship_date: str | None = None
    status: OrderStatus | None = None
    complete: bool | None = None

    @strawberry.field
    async def pet(self, info: Info) -> Pet | None:
        if self.pet_id is None:
            return None
        pet_loader = get_pet_loader(info.context)
        return await pet_loader.load(self.pet_id)


@strawberry.type
class User:
    id: int | None = None
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    password: str | None = None
    phone: str | None = None
    user_status: int | None = None


@strawberry.type
class ApiResponse:
    code: int | None = None
    type: str | None = None
    message: str | None = None


@strawberry.type
class InventoryEntry:
    status: str
    count: int


@strawberry.type
class PageInfo:
    has_next_page: bool
    end_cursor: int | None


@strawberry.type
class PetEdge:
    cursor: int
    node: Pet


@strawberry.type
class PetConnection:
    edges: list[PetEdge]
    page_info: PageInfo
    total_count: int


__all__ = [
    "ApiResponse",
    "Category",
    "HealthDetails",
    "HealthResponse",
    "InventoryEntry",
    "Order",
    "OrderStatus",
    "PageInfo",
    "Pet",
    "PetConnection",
    "PetEdge",
    "PetStatus",
    "Tag",
    "User",
]
