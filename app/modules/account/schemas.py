from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    remember_me: bool = False

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class GetOTPRequest(BaseModel):
    email: EmailStr

class GetOTPResponse(BaseModel):
    message: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr
    otp_code: str
    new_password: str

class ForgotPasswordResponse(BaseModel):
    message: str
