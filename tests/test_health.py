from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_query_returns_expected_shape() -> None:
    query = """
    query {
      health {
        status
        mode
        details {
          version
          build_date
          git_commit_sha
        }
      }
    }
    """

    response = client.post("/graphql", json={"query": query})

    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "health": {
                "status": "ok",
                "mode": "development",
                "details": {
                    "version": "0.1.0",
                    "build_date": "1970-01-01T00:00:00Z",
                    "git_commit_sha": "0000000",
                },
            }
        }
    }
