# src/app/main.py
from fastapi import FastAPI, Depends
from fastapi.openapi.utils import get_openapi

# ← ここを“絶対 import”で統一（作業ディレクトリを src にして起動する前提）
from app.routers import health, docs, search
from app.models.base import Base
from app.deps import engine
from app.auth.keycloak import current_user  # Keycloak のJWT検証

app = FastAPI(title="vectra-notes", version="0.1.0")

# DBテーブルは起動時にまとめて作成（実務は Alembic 推奨）
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# 公開OKのルーター
app.include_router(health.router)
app.include_router(search.router)

# 認証が必要なルーター（例：/docs を保護したい場合）
# 既存の docs ルーター全体に認証を必須にする
app.include_router(docs.router, dependencies=[Depends(current_user)])

# Swagger で「Authorize（Bearer）」ボタンを出すためのスキーマ追加
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )
    schema.setdefault("components", {}).setdefault("securitySchemes", {}).update({
        "bearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    })
    app.openapi_schema = schema
    return schema

app.openapi = custom_openapi
