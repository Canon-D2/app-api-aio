from fastapi import APIRouter
from . import schemas 
from .controllers import AccountController
from app.auth.depends import require_permission


router = APIRouter(prefix="/v1/account", tags=["account"])
controller = AccountController()


@router.get("/admin", status_code=200, 
            responses={200: {"description": "Get items success"}})
async def get_admin(current_user: dict = require_permission()):
    result = {"user": current_user}
    return result


@router.get("/customer", status_code=200, 
            responses={200: {"description": "Get items success"}})
async def get_customer(current_user: dict = require_permission()):
    result = {"user": current_user}
    return result


@router.post("/login", status_code=201, responses={
                201: {"model": schemas.LoginResponse, "description": "Post items success"}})
async def login(data: schemas.LoginRequest):
    result = await controller.login(data)
    return result


@router.post("/get-otp", status_code=201, responses={
                201: {"model": schemas.GetOTPResponse, "description": "Post items success"}})
async def get_otp(data: schemas.GetOTPRequest):
    result = await controller.get_otp(data)
    return result


@router.post("/forgot-password", status_code=201, responses={
                201: {"model": schemas.ForgotPasswordRequest, "description": "Post items success"}})
async def forgot_password(data: schemas.ForgotPasswordRequest):
    result = await controller.forgot_password(data)
    return result