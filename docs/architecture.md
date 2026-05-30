# Architecture

- `src/app/main.py`: FastAPI app and GraphQL router mounting.
- `src/app/schema.py`: Strawberry schema and resolvers — merges health + Petstore queries/mutations.
- `src/app/config.py`: Settings holder for runtime/build metadata and `petstore_base_url`.
- `src/app/context.py`: Per-request `AppContext` with REST client and DataLoaders.
- `src/app/petstore/rest_client.py`: Async `httpx` client for all Petstore REST endpoints.
- `src/app/petstore/types.py`: Strawberry output types (`Pet`, `Order`, `User`, …) + parse helpers.
- `src/app/petstore/inputs.py`: Strawberry input types for mutations + dict serialisers.
- `src/app/petstore/queries.py`: `PetstoreQuery` Strawberry type with all query resolvers.
- `src/app/petstore/mutations.py`: `PetstoreMutation` Strawberry type with all mutation resolvers.
- `src/app/petstore/loaders.py`: DataLoader factory for batched pet-by-ID lookups.
- `openapi.json`: OpenAPI 3.0 Petstore contract — single source of truth for the schema.

The schema is intentionally small and structured for future extension.
