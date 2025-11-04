# src/app/schemas/search.py
from pydantic import BaseModel, Field

class SearchRequest(BaseModel):
    q: str = Field(min_length=1, description="検索クエリ")
    k: int = Field(default=5, ge=1, le=50, description="返す件数")

class SearchHit(BaseModel):
    id: int
    title: str
    distance: float

class SearchResponse(BaseModel):
    hits: list[SearchHit]
