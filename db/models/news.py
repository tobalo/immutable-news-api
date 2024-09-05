from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from typing import List, Optional
import uuid

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

    class Config:
        allow_population_by_field_name = True

class NewsArticleResponse(NewsArticle):
    id: str = Field(..., alias="_id")

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
