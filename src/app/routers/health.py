# src/app/routers/health.py
from fastapi import APIRouter, Depends
from app.auth.keycloak import current_user

router = APIRouter(prefix="/healthz", tags=["health"])

@router.get("")
def healthz():
    return {"ok": True}

@router.get("/secure")
def healthz_secure(user=Depends(current_user)):
    # user は JWT のペイロード(dict)
    return {"ok": True, "sub": user.get("sub")}