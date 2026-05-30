# petstore-graphql

A minimal production-ready GraphQL service scaffolded with FastAPI + Strawberry.

## Overview

This project exposes a GraphQL API with a single `health` query and includes local development tooling,
tests, linting, Docker, CI, MkDocs, and GitHub community standards.

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

Expected response:

```json
{
  "data": {
    "health": {
      "status": "ok",
      "mode": "development",
      "details": {
        "version": "0.1.0",
        "build_date": "1970-01-01T00:00:00Z",
        "git_commit_sha": "0000000"
      }
    }
  }
}
```
