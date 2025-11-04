# src/settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@db:5432/vectra"
    OIDC_ISSUER: str | None = None
    OIDC_AUDIENCE: str | None = None
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    LOG_LEVEL: str = "INFO"

settings = Settings()
