from pydantic import BaseModel, Field

class DocCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    text: str = Field(min_length=1)

class DocOut(BaseModel):
    id: int
    title: str
