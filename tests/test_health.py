from fastapi.testclient import TestClient

from app.config import settings
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
                "mode": settings.mode,
                "details": {
                    "version": settings.version,
                    "build_date": settings.build_date,
                    "git_commit_sha": settings.git_commit_sha,
                },
            }
        }
    }
