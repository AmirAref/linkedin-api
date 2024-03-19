# custom models
from typing import Optional
from pydantic import BaseModel, HttpUrl


class Document(BaseModel):
    url: HttpUrl
    title: str


class Video(BaseModel):
    url: HttpUrl
    bitrate: float


class Post(BaseModel):
    url: HttpUrl
    text: Optional[str] = None
    reactions: int = 0
    comments: int = 0
    images: list[str] = []
    document: Document | None = None
    videos: list[Video] = []
