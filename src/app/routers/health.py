# src/app/routers/health.py
from fastapi import APIRouter
from settings import settings

router = APIRouter()

@router.get("/healthz")
def healthz():
    return {
        "ok": True,
        "db": settings.DATABASE_URL.split("@")[-1],  # 接続先のホスト表示だけ
        "auth": bool(settings.OIDC_ISSUER),
        "model": settings.EMBEDDING_MODEL,
    }
