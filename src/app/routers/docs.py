from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas.document import DocCreate, DocOut
from ..models.document import Document
from ..models.embedding import Embedding
from ..services.embedder import embed
from ..deps import get_session

router = APIRouter(prefix="/docs", tags=["docs"])

@router.post("/", response_model=DocOut)
def create_doc(payload: DocCreate, session: Session = Depends(get_session)):
    doc = Document(title=payload.title, text=payload.text)
    session.add(doc); session.flush()  # doc.id を得る
    vec = embed(payload.text)
    session.add(Embedding(doc_id=doc.id, vector=vec))
    session.commit()
    return {"id": doc.id, "title": doc.title}
