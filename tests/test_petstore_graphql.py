import asyncio

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


async def _fake_request(self, method: str, path: str, **kwargs):
    await asyncio.sleep(0)
    if method == "GET" and path == "/pet/findByStatus":
        return [
            {
                "id": 1,
                "name": "doggie",
                "photoUrls": ["https://example.com/dog.jpg"],
                "status": "available",
            }
        ]

    if method == "POST" and path == "/user":
        return {"code": 200, "type": "unknown", "message": "ok"}

    raise AssertionError(f"Unexpected REST call: {method} {path}")


def test_pets_by_status_query_maps_rest_response(monkeypatch) -> None:
    monkeypatch.setattr("app.graphql.rest_client.RestClient.request", _fake_request)

    query = """
    query {
      pets_by_status(status: AVAILABLE) {
        id
        name
        status
        photo_urls
      }
    }
    """

    response = client.post("/graphql", json={"query": query})

    assert response.status_code == 200
    assert response.json()["data"]["pets_by_status"] == [
        {
            "id": 1,
            "name": "doggie",
            "status": "AVAILABLE",
            "photo_urls": ["https://example.com/dog.jpg"],
        }
    ]


def test_create_user_mutation_maps_rest_response(monkeypatch) -> None:
    monkeypatch.setattr("app.graphql.rest_client.RestClient.request", _fake_request)

    query = """
    mutation {
      create_user(input: {username: \"alice\", password: \"secret\"}) {
        code
        type
        message
      }
    }
    """

    response = client.post("/graphql", json={"query": query})

    assert response.status_code == 200
    assert response.json()["data"]["create_user"] == {
        "code": 200,
        "type": "unknown",
        "message": "ok",
    }
