from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mode: str = "development"
    version: str = "0.1.0"
    build_date: str = "1970-01-01T00:00:00Z"
    git_commit_sha: str = "0000000"

    model_config = SettingsConfigDict(env_prefix="APP_", env_file=".env", extra="ignore")


settings = Settings()
