# petstore-graphql

A minimal production-ready GraphQL service scaffolded with FastAPI + Strawberry.

## Overview

This project exposes a GraphQL API generated from the OpenAPI Petstore contract (`openapi.json`) and
includes local development tooling, tests, linting, Docker, CI, MkDocs, and GitHub community standards.

For the initial implementation, the service calls the existing OpenAPI development deployment rather than connecting directly to the database. The priority was to make the interface available end‑to‑end first; the database‑backed implementation will follow.

Deployment at this time is adhoc directly into fly. Upcoming tasks will address deployment via github actions.

## Install dependencies (uv)

```bash
uv sync --dev
```

## Run app with hot reload

```bash
uv run uvicorn app.main:app --app-dir src --reload --host 0.0.0.0 --port 8000
```

GraphQL endpoint: `http://localhost:8000/graphql`

## Run tests

```bash
uv run pytest
```

## Run linting (ruff)

```bash
uv run ruff check .
```

## Run with Docker

```bash
docker build -t petstore-graphql .
docker run --rm -p 8000:8000 petstore-graphql
```

## Run with docker-compose

```bash
docker compose up --build
```

## Serve documentation

```bash
uv run mkdocs serve
```

## GraphQL health query example

```graphql
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
```

## GraphQL pet query example

```graphql
query {
  pets_by_status(status: AVAILABLE) {
    id
    name
    status
  }
}
```

Expected response:

```json
{
  "data": {
    "pets_by_status": []
  }
}
```

**Note**: The development environment is fully ephemeral. If the service restarts or the environment is recycled, all data is lost.
