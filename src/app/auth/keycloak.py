# src/app/auth/keycloak.py
import time
import httpx
from jose import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from settings import settings  # ← src直下の settings.py を読む

security = HTTPBearer(auto_error=True)
_jwks_cache = {"ts": 0.0, "jwks": None}

def _fetch_jwks():
    """Keycloakの公開鍵(JWKS)を5分キャッシュして取得"""
    global _jwks_cache
    if not _jwks_cache["jwks"] or (time.time() - _jwks_cache["ts"] > 300):
        url = f"{settings.OIDC_ISSUER}/protocol/openid-connect/certs"
        try:
            resp = httpx.get(url, timeout=10)
            resp.raise_for_status()
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"JWKS fetch failed: {e}")
        _jwks_cache["jwks"] = resp.json()
        _jwks_cache["ts"] = time.time()
    return _jwks_cache["jwks"]

def _get_key_for_token(token: str):
    """トークンの kid に合う公開鍵をJWKSから探す"""
    header = jwt.get_unverified_header(token)
    kid = header.get("kid")
    for k in _fetch_jwks().get("keys", []):
        if k.get("kid") == kid:
            return k
    raise HTTPException(status_code=401, detail="Signing key not found (kid mismatch)")

async def current_user(creds: HTTPAuthorizationCredentials = Depends(security)):
    """Bearerトークンを検証してペイロードを返す"""
    token = creds.credentials
    key = _get_key_for_token(token)
    try:
        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=settings.OIDC_AUDIENCE,
            issuer=settings.OIDC_ISSUER,
        )
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")
    return payload  # 必要に応じて dict から必要フィールドを取り出してもOK