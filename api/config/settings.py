from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DATABASE_")

    type: str
    user: str | None = None
    password: str | None = None
    server: str | None = None
    db: str | None = None
    location: str | None = None


class Settings(BaseSettings):
    database: DatabaseSettings = DatabaseSettings()

    model_config = SettingsConfigDict(extra="allow")


settings = Settings()
