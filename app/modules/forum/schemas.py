from pydantic import BaseModel, Field
from typing import Literal, Optional, List, Dict


class ThreadCreate(BaseModel):
    theme: str
    description: Optional[str] = None
    title: str
    author_id: str
    comments: int = 0


class ThreadUpdate(BaseModel):
    theme: Optional[str] = None
    description: Optional[str] = None
    title: Optional[str] = None


class ThreadResponse(BaseModel):
    id: str = Field(alias="_id")
    theme: str
    description: Optional[str] = None
    title: str
    author_id: str
    comments: int
    created_at: float
    updated_at: Optional[int] = None


class PaginatedThreadResponse(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int
    results: List[ThreadResponse]


class AuthorInfo(BaseModel):
    user_id: str
    fullname: str
    avatar: Optional[str] = None


class PostCreate(BaseModel):
    thread_id: str
    author: AuthorInfo
    content: str
    attachments: Optional[List[str]] = []
    reply_to: Optional[str] = None 
    reactions: Optional[Dict[Literal["like", "love", "haha", "sad"], List[str]]] = {}


class PostUpdate(BaseModel):
    content: Optional[str] = None
    attachments: Optional[List[str]] = None


class PostResponse(BaseModel):
    id: str = Field(alias="_id")
    thread_id: str
    author: AuthorInfo
    content: str
    attachments: List[str]
    reply_to: Optional[str] = None
    reactions: Dict[str, List[str]]
    created_at: float
    updated_at: Optional[int] = None


class PaginatedPostResponse(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int
    results: List[PostResponse]
