# Petstore GraphQL Examples

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
