from fastapi import APIRouter
from .schemas import *
from .controllers import AccountController
from app.auth.depends import require_permission

router = APIRouter(prefix="/v1/account", tags=["account"])
controller = AccountController()

@router.get("/admin")
async def get_admin(current_user: dict = require_permission()):
    return {"user": current_user}

@router.get("/customer")
async def get_customer(current_user: dict = require_permission()):
    return {"user": current_user}

@router.post("/login", response_model=LoginResponse)
async def login(data: LoginRequest):
    return await controller.login(data)

@router.post("/get-otp", response_model=GetOTPResponse)
async def get_otp(data: GetOTPRequest):
    return await controller.get_otp(data)

@router.post("/forgot-password", response_model=ForgotPasswordResponse)
async def forgot_password(data: ForgotPasswordRequest):
    return await controller.forgot_password(data)