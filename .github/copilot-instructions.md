# Copilot Instructions

## Coding style
- Use Python with Ruff as the only linting/formatting tool.
- Prefer small, explicit modules under `src/app`.

## Testing
- Add or update `pytest` tests for behavior changes.
- Keep tests focused on GraphQL schema behavior and API responses.

## Documentation
- Keep MkDocs content in `docs/` and navigation in `mkdocs.yml`.
- Update docs when architecture, testing, or configuration changes.

## Changelog
- Add end-user-facing changes to `CHANGELOG.md` under `Unreleased`.

## GraphQL extensibility
- Extend the schema by adding new types and fields in `src/app/schema.py`.
- Keep resolver output models explicit to support future env/build metadata injection.
