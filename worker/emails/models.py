from pydantic import BaseModel, EmailStr

class EmailData(BaseModel):
    email: EmailStr
    fullname: str
    otp: str
