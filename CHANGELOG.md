# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial FastAPI + Strawberry GraphQL service with `health` query.
- Project tooling with uv, Ruff, pytest, Docker, CI, and MkDocs.
- Community health and contribution standards under `.github/`.
- Petstore GraphQL API generated from `openapi.json` (OpenAPI 3.0 source of truth).
  - Domain types: `Pet`, `Category`, `Tag`, `Order`, `User`, `InventoryEntry`.
  - Enums: `PetStatus` (available/pending/sold), `OrderStatus` (placed/approved/delivered).
  - Queries: `pet`, `pets_by_status`, `pets_by_tags`, `inventory`, `order`, `user`, `user_login`.
  - Mutations: `add_pet`, `update_pet`, `delete_pet`, `place_order`, `delete_order`,
    `create_user`, `update_user`, `delete_user`, `logout_user`.
  - Async REST client (`httpx`) wired to each OpenAPI endpoint.
  - DataLoader for batched pet-by-ID lookups (N+1 avoidance).
  - Per-request `AppContext` injected via Strawberry/FastAPI context getter.
