from pydantic import BaseModel
from datetime import datetime

class PostCreate(BaseModel):
    author: str
    title: str
    content: str
    category: str = "General"

class PostResponse(BaseModel):
    id: int
    author: str
    title: str
    content: str
    category: str
    created_at: datetime
