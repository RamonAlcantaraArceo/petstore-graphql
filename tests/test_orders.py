"""Tests for store (order) queries and mutations (mocked REST client)."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.context import AppContext, get_context
from app.main import app
from app.petstore.rest_client import PetstoreClient


@pytest.fixture()
def mock_rest() -> PetstoreClient:
    return AsyncMock(spec=PetstoreClient)


@pytest.fixture()
def tc(mock_rest: PetstoreClient) -> TestClient:
    async def override_context() -> AppContext:
        return AppContext(rest_client=mock_rest)

    app.dependency_overrides[get_context] = override_context
    return TestClient(app)


ORDER_PAYLOAD = {
    "id": 42,
    "petId": 1,
    "quantity": 2,
    "shipDate": "2024-01-15T10:00:00Z",
    "status": "placed",
    "complete": False,
}


def _post(client: TestClient, query: str, variables: dict | None = None) -> dict:
    resp = client.post("/graphql", json={"query": query, "variables": variables or {}})
    assert resp.status_code == 200
    return resp.json()


# --------------------------------------------------------- query: inventory --


def test_inventory_query(mock_rest: PetstoreClient, tc: TestClient) -> None:
    mock_rest.get_inventory = AsyncMock(
        return_value={"available": 10, "pending": 2, "sold": 5}
    )

    result = _post(tc, "query { inventory { status count } }")

    assert result.get("errors") is None
    entries = {e["status"]: e["count"] for e in result["data"]["inventory"]}
    assert entries["available"] == 10
    assert entries["pending"] == 2
    assert entries["sold"] == 5


# ------------------------------------------------------------ query: order --


def test_order_query_returns_order(mock_rest: PetstoreClient, tc: TestClient) -> None:
    mock_rest.get_order_by_id = AsyncMock(return_value=ORDER_PAYLOAD)

    result = _post(
        tc,
        "query { order(id: 42) { id pet_id quantity ship_date status complete } }",
    )

    assert result.get("errors") is None
    order = result["data"]["order"]
    assert order["id"] == 42
    assert order["pet_id"] == 1
    assert order["quantity"] == 2
    assert order["status"] == "placed"
    assert order["complete"] is False


def test_order_query_returns_null_for_missing(
    mock_rest: PetstoreClient, tc: TestClient
) -> None:
    mock_rest.get_order_by_id = AsyncMock(side_effect=Exception("404"))

    result = _post(tc, "query { order(id: 9999) { id } }")

    assert result.get("errors") is None
    assert result["data"]["order"] is None


# ------------------------------------------------------- mutation: order --


def test_place_order_mutation(mock_rest: PetstoreClient, tc: TestClient) -> None:
    mock_rest.place_order = AsyncMock(return_value=ORDER_PAYLOAD)

    result = _post(
        tc,
        """
        mutation PlaceOrder($order: OrderInput!) {
          place_order(order: $order) { id pet_id quantity status }
        }
        """,
        {"order": {"pet_id": 1, "quantity": 2, "status": "placed"}},
    )

    assert result.get("errors") is None
    order = result["data"]["place_order"]
    assert order["id"] == 42
    assert order["pet_id"] == 1


def test_delete_order_mutation_success(
    mock_rest: PetstoreClient, tc: TestClient
) -> None:
    mock_rest.delete_order = AsyncMock(return_value=None)

    result = _post(tc, "mutation { delete_order(id: 42) }")

    assert result.get("errors") is None
    assert result["data"]["delete_order"] is True


def test_delete_order_mutation_failure(
    mock_rest: PetstoreClient, tc: TestClient
) -> None:
    mock_rest.delete_order = AsyncMock(side_effect=Exception("404"))

    result = _post(tc, "mutation { delete_order(id: 9999) }")

    assert result.get("errors") is None
    assert result["data"]["delete_order"] is False
