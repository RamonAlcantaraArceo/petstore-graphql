"""Tests for pet queries and mutations (mocked REST client)."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.context import AppContext
from app.petstore.rest_client import PetstoreClient


def _make_client(rest_client: PetstoreClient) -> TestClient:
    """Return a TestClient whose GraphQL context uses the provided REST client mock."""

    async def override_context() -> AppContext:
        return AppContext(rest_client=rest_client)


    from app.context import get_context
    from app.main import app as _app

    _app.dependency_overrides[get_context] = override_context
    return TestClient(_app)


@pytest.fixture()
def mock_rest() -> PetstoreClient:
    client = AsyncMock(spec=PetstoreClient)
    return client


@pytest.fixture()
def tc(mock_rest: PetstoreClient) -> TestClient:
    return _make_client(mock_rest)


# ------------------------------------------------------------------ helpers --

PET_PAYLOAD = {
    "id": 1,
    "name": "Rex",
    "photoUrls": ["http://example.com/rex.jpg"],
    "category": {"id": 10, "name": "Dogs"},
    "tags": [{"id": 5, "name": "friendly"}],
    "status": "available",
}


def _post(client: TestClient, query: str, variables: dict | None = None) -> dict:
    resp = client.post("/graphql", json={"query": query, "variables": variables or {}})
    assert resp.status_code == 200
    return resp.json()


# --------------------------------------------------------------- query: pet --


def test_pet_query_returns_pet(mock_rest: PetstoreClient, tc: TestClient) -> None:
    mock_rest.get_pet_by_id = AsyncMock(return_value=PET_PAYLOAD)

    result = _post(
        tc,
        """
        query GetPet($id: Int!) {
          pet(id: $id) {
            id name photo_urls status
            category { id name }
            tags { id name }
          }
        }
        """,
        {"id": 1},
    )

    assert result.get("errors") is None
    pet = result["data"]["pet"]
    assert pet["id"] == 1
    assert pet["name"] == "Rex"
    assert pet["photo_urls"] == ["http://example.com/rex.jpg"]
    assert pet["status"] == "available"
    assert pet["category"]["name"] == "Dogs"
    assert pet["tags"][0]["name"] == "friendly"
    mock_rest.get_pet_by_id.assert_called_once_with(1)


def test_pet_query_returns_null_for_missing_pet(
    mock_rest: PetstoreClient, tc: TestClient
) -> None:
    mock_rest.get_pet_by_id = AsyncMock(side_effect=Exception("404 Not Found"))

    result = _post(tc, "query { pet(id: 999) { id name } }")

    assert result.get("errors") is None
    assert result["data"]["pet"] is None


def test_pets_by_status_query(mock_rest: PetstoreClient, tc: TestClient) -> None:
    mock_rest.find_pets_by_status = AsyncMock(return_value=[PET_PAYLOAD])

    result = _post(
        tc,
        "query { pets_by_status(status: available) { id name status } }",
    )

    assert result.get("errors") is None
    pets = result["data"]["pets_by_status"]
    assert len(pets) == 1
    assert pets[0]["name"] == "Rex"
    mock_rest.find_pets_by_status.assert_called_once_with("available")


def test_pets_by_tags_query(mock_rest: PetstoreClient, tc: TestClient) -> None:
    mock_rest.find_pets_by_tags = AsyncMock(return_value=[PET_PAYLOAD])

    result = _post(
        tc,
        'query { pets_by_tags(tags: ["friendly"]) { id name } }',
    )

    assert result.get("errors") is None
    assert result["data"]["pets_by_tags"][0]["name"] == "Rex"


# ---------------------------------------------------------- mutation: pet --


def test_add_pet_mutation(mock_rest: PetstoreClient, tc: TestClient) -> None:
    mock_rest.add_pet = AsyncMock(return_value=PET_PAYLOAD)

    result = _post(
        tc,
        """
        mutation AddPet($pet: PetInput!) {
          add_pet(pet: $pet) { id name status }
        }
        """,
        {"pet": {"name": "Rex", "photo_urls": ["http://example.com/rex.jpg"]}},
    )

    assert result.get("errors") is None
    assert result["data"]["add_pet"]["name"] == "Rex"


def test_update_pet_mutation(mock_rest: PetstoreClient, tc: TestClient) -> None:
    updated = {**PET_PAYLOAD, "status": "sold"}
    mock_rest.update_pet = AsyncMock(return_value=updated)

    result = _post(
        tc,
        """
        mutation UpdatePet($pet: PetInput!) {
          update_pet(pet: $pet) { id name status }
        }
        """,
        {"pet": {"id": 1, "name": "Rex", "photo_urls": [], "status": "sold"}},
    )

    assert result.get("errors") is None
    assert result["data"]["update_pet"]["status"] == "sold"


def test_delete_pet_mutation_success(mock_rest: PetstoreClient, tc: TestClient) -> None:
    mock_rest.delete_pet = AsyncMock(return_value=None)

    result = _post(tc, "mutation { delete_pet(id: 1) }")

    assert result.get("errors") is None
    assert result["data"]["delete_pet"] is True


def test_delete_pet_mutation_failure(mock_rest: PetstoreClient, tc: TestClient) -> None:
    mock_rest.delete_pet = AsyncMock(side_effect=Exception("404"))

    result = _post(tc, "mutation { delete_pet(id: 999) }")

    assert result.get("errors") is None
    assert result["data"]["delete_pet"] is False
