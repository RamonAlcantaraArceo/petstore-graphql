# Petstore GraphQL Examples

## GraphQL Explorer

You can explore and query the API using the built‑in GraphQL Explorer: [petstore-graphql.fly.dev/graphql](https://petstore-graphql.fly.dev/graphql)

**Note**: The development environment is fully ephemeral. If the service restarts or the environment is recycled, all data is lost.

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
