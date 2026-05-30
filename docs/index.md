# Petstore GraphQL

Minimal production-ready GraphQL service using FastAPI and Strawberry.

## Health query

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
