from fastapi import FastAPI
from app.routers import health, docs, search
from app.models.base import Base
from app.deps import engine
from sqlalchemy import text

app = FastAPI(title="vectra-notes")

@app.on_event("startup")
def on_startup():
    print("[BOOT] checking DB connection...")
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))  # DB疎通チェック
    print("[BOOT] DB OK ✅")

    # --- ★ 初回のみ: DBにテーブルを自動作成 ---
    print("[BOOT] creating tables (if not exist)...")
    Base.metadata.create_all(bind=engine)
    print("[BOOT] tables ready ✅")

# 📌 /health エンドポイント（FastAPI 独自の health なので名前衝突回避）
@app.get("/health")
def health_check():
    return {"status": "ok"}

# --- ルータ登録 ---
app.include_router(health.router)
app.include_router(docs.router)
app.include_router(search.router)
