# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Default `APP_PETSTORE_BASE_URL` now targets the Docker Compose `api` service at `http://api:8000/api/v1` instead of the public Swagger Petstore endpoint.

### Added
- Initial FastAPI + Strawberry GraphQL service with `health` query.
- Project tooling with uv, Ruff, pytest, Docker, CI, and MkDocs.
- Community health and contribution standards under `.github/`.
