from __future__ import annotations

from app.graphql.inputs.models import CategoryInput, OrderInput, PetInput, TagInput, UserInput
from app.graphql.types.models import (
    ApiResponse,
    Category,
    Order,
    OrderStatus,
    Pet,
    PetStatus,
    Tag,
    User,
)


def _pet_status(value: str | None) -> PetStatus | None:
    if value is None:
        return None
    try:
        return PetStatus(value)
    except ValueError:
        return None


def _order_status(value: str | None) -> OrderStatus | None:
    if value is None:
        return None
    try:
        return OrderStatus(value)
    except ValueError:
        return None


def map_category(payload: dict | None) -> Category | None:
    if not payload:
        return None
    return Category(id=payload.get("id"), name=payload.get("name"))


def map_tag(payload: dict | None) -> Tag | None:
    if not payload:
        return None
    return Tag(id=payload.get("id"), name=payload.get("name"))


def map_pet(payload: dict) -> Pet:
    tags_payload = payload.get("tags") or []
    return Pet(
        id=payload.get("id"),
        name=payload.get("name", ""),
        category=map_category(payload.get("category")),
        photo_urls=payload.get("photoUrls") or [],
        tags=[tag for tag in (map_tag(item) for item in tags_payload) if tag is not None],
        status=_pet_status(payload.get("status")),
    )


def map_order(payload: dict) -> Order:
    return Order(
        id=payload.get("id"),
        pet_id=payload.get("petId"),
        quantity=payload.get("quantity"),
        ship_date=payload.get("shipDate"),
        status=_order_status(payload.get("status")),
        complete=payload.get("complete"),
    )


def map_user(payload: dict) -> User:
    return User(
        **{
            "id": payload.get("id"),
            "username": payload.get("username"),
            "first_name": payload.get("firstName"),
            "last_name": payload.get("lastName"),
            "email": payload.get("email"),
            "password": payload.get("password"),
            "phone": payload.get("phone"),
            "user_status": payload.get("userStatus"),
        }
    )


def map_api_response(payload: dict | None, default_message: str | None = None) -> ApiResponse:
    payload = payload or {}
    return ApiResponse(
        code=payload.get("code"),
        type=payload.get("type"),
        message=payload.get("message") or default_message,
    )


def category_input_to_dict(value: CategoryInput | None) -> dict | None:
    if value is None:
        return None
    return {"id": value.id, "name": value.name}


def tag_input_to_dict(value: TagInput) -> dict:
    return {"id": value.id, "name": value.name}


def pet_input_to_dict(value: PetInput) -> dict:
    return {
        "id": value.id,
        "name": value.name,
        "category": category_input_to_dict(value.category),
        "photoUrls": value.photo_urls,
        "tags": [tag_input_to_dict(tag) for tag in value.tags or []],
        "status": value.status.value if value.status else None,
    }


def order_input_to_dict(value: OrderInput) -> dict:
    return {
        "id": value.id,
        "petId": value.pet_id,
        "quantity": value.quantity,
        "shipDate": value.ship_date,
        "status": value.status.value if value.status else None,
        "complete": value.complete,
    }


def user_input_to_dict(value: UserInput) -> dict:
    return {
        "id": value.id,
        "username": value.username,
        "firstName": value.first_name,
        "lastName": value.last_name,
        "email": value.email,
        "password": value.password,
        "phone": value.phone,
        "userStatus": value.user_status,
    }
