# Architecture

- `src/app/main.py`: FastAPI app and GraphQL router mounting.
- `src/app/graphql/`: OpenAPI-driven GraphQL types, inputs, resolvers, loaders, context, and SDL.
- `src/app/schema.py`: Backwards-compatible schema export.
- `src/app/config.py`: Settings holder for runtime/build metadata.
- `openapi.json`: OpenAPI contract used as the GraphQL source of truth.
