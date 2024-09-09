from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from typing import List, Optional
import uuid
import hashlib
import json

def generate_hash(obj: dict) -> str:
    # Sort the dictionary to ensure consistent ordering
    sorted_dict = json.dumps(obj, sort_keys=True, default=str)
    return hashlib.sha256(sorted_dict.encode()).hexdigest()

class NewsSubmission(BaseModel):
    url: HttpUrl

class NewsArticle(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    title: str
    content: str
    authors: str
    published_date: datetime
    url: str
    top_image: Optional[str] = None
    videos: List[str] = []
    keywords: List[str] = []
    summary: Optional[str] = None
    dag_address: Optional[str] = None
    hash: Optional[str] = None

    class Config:
        allow_population_by_field_name = True

    def __init__(self, **data):
        super().__init__(**data)
        self.hash = generate_hash(self.dict(exclude={'hash'}))

class NewsArticleResponse(NewsArticle):
    id: str = Field(..., alias="_id")

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
