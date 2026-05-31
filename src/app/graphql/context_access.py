from __future__ import annotations

from typing import Any

from strawberry.dataloader import DataLoader

from app.graphql.rest_client import RestClient


def get_rest_client(context: object) -> RestClient:
    if isinstance(context, dict):
        return context["rest_client"]  # type: ignore[return-value]
    return context.rest_client


def get_pet_loader(context: object) -> DataLoader[Any, Any]:
    if isinstance(context, dict):
        return context["pet_loader"]  # type: ignore[return-value]
    return context.pet_loader
