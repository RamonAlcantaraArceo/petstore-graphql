import strawberry
from strawberry.schema.config import StrawberryConfig

from app.config import settings


@strawberry.type
class HealthDetails:
    version: str
    build_date: str
    git_commit_sha: str


@strawberry.type
class HealthResponse:
    status: str
    mode: str
    details: HealthDetails


@strawberry.type
class Query:
    @strawberry.field
    def health(self) -> HealthResponse:
        return HealthResponse(
            status="ok",
            mode=settings.mode,
            details=HealthDetails(
                version=settings.version,
                build_date=settings.build_date,
                git_commit_sha=settings.git_commit_sha,
            ),
        )


schema = strawberry.Schema(query=Query, config=StrawberryConfig(auto_camel_case=False))
