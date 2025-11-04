from fastapi import FastAPI
from .routers import health, docs, search
from .models.base import Base
from .models.document import Document  # noqa
from .models.embedding import Embedding  # noqa
from .deps import engine

app = FastAPI(title="vectra-notes")

# 初回は簡易にcreate_all（実務では Alembic を）
Base.metadata.create_all(bind=engine)

app.include_router(health.router)
app.include_router(docs.router)
app.include_router(search.router)
