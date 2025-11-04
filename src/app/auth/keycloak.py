# src/app/auth/keycloak.py
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
import httpx
from functools import lru_cache
from settings import settings

security = HTTPBearer(auto_error=False)

@lru_cache(maxsize=1)
def _jwks() -> dict | None:
    if not settings.OIDC_ISSUER:
        return None
    url = settings.OIDC_ISSUER.rstrip("/") + "/protocol/openid-connect/certs"
    with httpx.Client(timeout=5) as cl:
        return cl.get(url).json()

def _decode_token(token: str) -> dict:
    if not settings.OIDC_ISSUER:
        # 認証オフ（開発用）
        return {"sub": "anonymous", "roles": ["anonymous"]}

    jwks = _jwks()
    if not jwks:
        raise HTTPException(status_code=503, detail="JWKS not available")

    unverified = jwt.get_unverified_header(token)
    kid = unverified.get("kid")
    key = next((k for k in jwks.get("keys", []) if k.get("kid") == kid), None)
    if not key:
        raise HTTPException(status_code=401, detail="Unknown key")

    options = {"verify_aud": bool(settings.OIDC_AUDIENCE)}
    claims = jwt.decode(
        token,
        key,
        algorithms=key.get("alg", "RS256"),
        audience=settings.OIDC_AUDIENCE,
        issuer=settings.OIDC_ISSUER,
        options=options,
    )
    return claims

async def current_user(
    cred: Annotated[HTTPAuthorizationCredentials | None, Depends(security)]
) -> dict:
    if not cred:
        # 認証ヘッダなし
        if not settings.OIDC_ISSUER:
            return {"sub": "anonymous", "roles": ["anonymous"]}
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")
    try:
        return _decode_token(cred.credentials)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
