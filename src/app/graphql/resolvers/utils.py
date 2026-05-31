from __future__ import annotations

from collections.abc import Sequence

from graphql import GraphQLError

from app.graphql.context_access import get_pet_loader as _get_pet_loader
from app.graphql.context_access import get_rest_client as _get_rest_client
from app.graphql.rest_client import RestClient, RestError
from app.graphql.types.models import PageInfo, Pet, PetConnection, PetEdge


def get_rest_client(info) -> RestClient:
    return _get_rest_client(info.context)


def get_pet_loader(info):
    return _get_pet_loader(info.context)


def handle_rest_error(exc: RestError) -> GraphQLError:
    return GraphQLError(
        "REST API request failed",
        extensions={"status_code": exc.status_code, "detail": exc.detail},
    )


def paginate_pets(items: Sequence[Pet], first: int | None, after: int | None) -> PetConnection:
    items_list = list(items)
    safe_after = max(after or 0, 0)
    if first is None:
        sliced = items_list[safe_after:]
    else:
        sliced = items_list[safe_after : safe_after + max(first, 0)]

    end_cursor = safe_after + len(sliced) if sliced else None
    has_next_page = bool(
        first is not None and end_cursor is not None and end_cursor < len(items_list)
    )

    edges = [PetEdge(cursor=safe_after + idx, node=pet) for idx, pet in enumerate(sliced)]
    return PetConnection(
        edges=edges,
        page_info=PageInfo(has_next_page=has_next_page, end_cursor=end_cursor),
        total_count=len(items_list),
    )
