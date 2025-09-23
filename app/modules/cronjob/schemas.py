from pydantic import BaseModel, Field
from typing import Optional, List

class CronCreate(BaseModel):
    task: str
    endpoint: str
    method: str
    header: Optional[str] = None
    request: Optional[dict] = None
    response: Optional[dict] = None
    schedule: str  # m h d M w
    enable: bool

class CronUpdate(BaseModel):
    task: Optional[str] = None
    endpoint: Optional[str] = None
    method: Optional[str] = None
    header: Optional[str] = None
    request: Optional[dict] = None
    response: Optional[dict] = None
    schedule: Optional[str] = None
    enable: Optional[bool] = None

class CronResponse(BaseModel):
    id: str = Field(alias="_id")
    task: Optional[str]
    endpoint: Optional[str]
    method: Optional[str]
    header: Optional[str] = None
    request: Optional[dict] = None
    response: Optional[dict] = None
    schedule: Optional[str] 
    enable: Optional[bool] 
    created_at: Optional[float] 
    updated_at: Optional[float] = None

class PaginatedCronResponse(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int
    results: List[CronResponse]
