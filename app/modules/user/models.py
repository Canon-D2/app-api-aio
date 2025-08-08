from pydantic import BaseModel, EmailStr
from typing import Optional, Literal


class UserModel(BaseModel):
    email: EmailStr
    password: str
    fullname: str
    role: Literal["admin", "customer"]
    phone: str
    gender: Literal["male", "female", "other"]
    address: Optional[str]
    created_at: float
