from collections.abc import Generator
from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@db:5432/vectra"
    OIDC_ISSUER: str | None = "http://keycloak:8080/realms/dev"
    OIDC_AUDIENCE: str | None = "vectra-api"

settings = Settings()

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(engine, expire_on_commit=False, autoflush=False)

def get_session() -> Generator[Session, None, None]:
    with SessionLocal() as s:
        yield s
