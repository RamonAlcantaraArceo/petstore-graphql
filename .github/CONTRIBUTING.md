# Contributing

## Branching model
- Create feature branches from `main`.
- Branch names should be descriptive, for example: `feat/graphql-health`.

## Commit style
- Use clear, imperative commit messages.
- Keep commits focused and reviewable.

## Testing requirements
- Run tests before opening a PR:
  - `uv run pytest`

## Linting requirements
- Ruff is the only linting/formatting tool:
  - `uv run ruff check .`

## CHANGELOG requirements
- Add end-user-facing changes to `CHANGELOG.md` under `## [Unreleased]`.
- Use Keep a Changelog section types (Added, Changed, Fixed, etc.).
