from typing import Optional, List, Literal
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    fullname: str
    email: EmailStr
    password: str
    permission: Literal["admin", "member", "memvip", "staff"]
    gender: Literal["male", "female", "other"]
    birthday: float
    avatar: Optional[str] = None
    phone: str  
    address: str
    company: Optional[str] = None
    tax_code: Optional[str] = None


class UserUpdate(BaseModel):
    fullname: Optional[str] = None
    password: Optional[str] = None
    permission: Optional[Literal["admin", "member", "memvip", "staff"]] = None
    gender: Optional[Literal["male", "female", "other"]] = None
    birthday: Optional[float] = None
    avatar: Optional[str] = None
    phone: Optional[str] = None  
    address: Optional[str] = None
    company: Optional[str] = None
    tax_code: Optional[str] = None


class UserResponse(BaseModel):
    id: str = Field(alias="_id")
    fullname: Optional[str]
    email: EmailStr
    # password: Optional[str]
    permission: Optional[str]
    gender: Optional[str]
    birthday: Optional[float]
    avatar: Optional[str] = None
    phone: Optional[str]
    address: Optional[str]
    company: Optional[str] = None
    tax_code: Optional[str] = None


class PaginatedUserResponse(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int
    results: List[UserResponse]
