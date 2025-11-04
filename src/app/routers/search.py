from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..services.embedder import embed
from ..services.searcher import top_k
from ..deps import get_session

router = APIRouter(prefix="/search", tags=["search"])

@router.get("/")
def search(q: str = Query(min_length=1), k: int = 5, session: Session = Depends(get_session)):
    qvec = embed(q)
    rows = top_k(session, qvec, k)
    return [{"id": r["id"], "title": r["title"], "distance": r["dist"]} for r in rows]
