# src/settings.py
from pathlib import Path
from pydantic_settings import BaseSettings

ROOT = Path(__file__).resolve().parents[1]

class Settings(BaseSettings):
    OIDC_ISSUER: str = "http://localhost:8080/realms/dev"
    OIDC_AUDIENCE: str = "vectra-api"
    DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@localhost:5432/vectra"

    class Config:
        env_file = ROOT / ".env"
        env_file_encoding = "utf-8"

settings = Settings()
