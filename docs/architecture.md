# Architecture

- `src/app/main.py`: FastAPI app and GraphQL router mounting.
- `src/app/schema.py`: Strawberry schema and resolvers.
- `src/app/config.py`: Settings holder for runtime/build metadata.

The schema is intentionally small and structured for future extension.
