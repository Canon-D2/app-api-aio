from pydantic import BaseModel, EmailStr
from typing import Optional, List


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    fullname: str
    role: str
    phone: Optional[str]
    gender: Optional[str]
    address: Optional[str]


class UserUpdate(BaseModel):
    fullname: Optional[str]
    password: Optional[str]
    role: Optional[str]
    phone: Optional[str]
    gender: Optional[str]
    address: Optional[str]


class UserResponse(BaseModel):
    _id: str
    email: EmailStr
    fullname: str
    role: str
    phone: Optional[str]
    gender: Optional[str]
    address: Optional[str]
    created_at: Optional[float] = None
    updated_at: Optional[float] = None


class PaginatedUserResponse(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int
    results: List[UserResponse]
