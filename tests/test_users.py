"""Tests for user queries and mutations (mocked REST client)."""

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


USER_PAYLOAD = {
    "id": 7,
    "username": "jdoe",
    "firstName": "John",
    "lastName": "Doe",
    "email": "john@example.com",
    "phone": "555-0100",
    "userStatus": 1,
}


def _post(client: TestClient, query: str, variables: dict | None = None) -> dict:
    resp = client.post("/graphql", json={"query": query, "variables": variables or {}})
    assert resp.status_code == 200
    return resp.json()


# ------------------------------------------------------------- query: user --


def test_user_query_returns_user(mock_rest: PetstoreClient, tc: TestClient) -> None:
    mock_rest.get_user_by_username = AsyncMock(return_value=USER_PAYLOAD)

    result = _post(
        tc,
        "query { user(username: \"jdoe\") { id username first_name last_name email phone"
        " user_status } }",
    )

    assert result.get("errors") is None
    user = result["data"]["user"]
    assert user["id"] == 7
    assert user["username"] == "jdoe"
    assert user["first_name"] == "John"
    assert user["last_name"] == "Doe"
    assert user["email"] == "john@example.com"


def test_user_query_returns_null_for_missing(
    mock_rest: PetstoreClient, tc: TestClient
) -> None:
    mock_rest.get_user_by_username = AsyncMock(side_effect=Exception("404"))

    result = _post(tc, 'query { user(username: "nobody") { id } }')

    assert result.get("errors") is None
    assert result["data"]["user"] is None


def test_user_login_query(mock_rest: PetstoreClient, tc: TestClient) -> None:
    mock_rest.login_user = AsyncMock(return_value="logged-in-token-xyz")

    result = _post(
        tc,
        'query { user_login(username: "jdoe", password: "secret") }',
    )

    assert result.get("errors") is None
    assert result["data"]["user_login"] == "logged-in-token-xyz"


# ---------------------------------------------------------- mutation: user --


def test_create_user_mutation(mock_rest: PetstoreClient, tc: TestClient) -> None:
    mock_rest.create_user = AsyncMock(return_value=USER_PAYLOAD)

    result = _post(
        tc,
        """
        mutation CreateUser($user: UserInput!) {
          create_user(user: $user) { id username email }
        }
        """,
        {"user": {"username": "jdoe", "email": "john@example.com", "password": "secret"}},
    )

    assert result.get("errors") is None
    user = result["data"]["create_user"]
    assert user["id"] == 7
    assert user["username"] == "jdoe"


def test_update_user_mutation_success(
    mock_rest: PetstoreClient, tc: TestClient
) -> None:
    mock_rest.update_user = AsyncMock(return_value=None)

    result = _post(
        tc,
        """
        mutation UpdateUser($username: String!, $user: UserInput!) {
          update_user(username: $username, user: $user)
        }
        """,
        {"username": "jdoe", "user": {"email": "new@example.com"}},
    )

    assert result.get("errors") is None
    assert result["data"]["update_user"] is True


def test_delete_user_mutation_success(
    mock_rest: PetstoreClient, tc: TestClient
) -> None:
    mock_rest.delete_user = AsyncMock(return_value=None)

    result = _post(tc, 'mutation { delete_user(username: "jdoe") }')

    assert result.get("errors") is None
    assert result["data"]["delete_user"] is True


def test_delete_user_mutation_failure(
    mock_rest: PetstoreClient, tc: TestClient
) -> None:
    mock_rest.delete_user = AsyncMock(side_effect=Exception("404"))

    result = _post(tc, 'mutation { delete_user(username: "ghost") }')

    assert result.get("errors") is None
    assert result["data"]["delete_user"] is False


def test_logout_user_mutation(mock_rest: PetstoreClient, tc: TestClient) -> None:
    mock_rest.logout_user = AsyncMock(return_value=None)

    result = _post(tc, "mutation { logout_user }")

    assert result.get("errors") is None
    assert result["data"]["logout_user"] is True
