import random
from bson import ObjectId
from app.mongo.base import BaseCRUD
from app.mongo.engine import engine_aio
from app.auth.services import auth_services
from .schemas import LoginRequest, ForgotPasswordRequest
from .exception import ErrorCode
from app.utils.helper import Helper
from worker.emails.controllers import EmailController


account_crud = BaseCRUD("users", engine_aio)


class AccountService:
    def __init__(self, crud: BaseCRUD):
        self.crud = crud
        self.email_controller = EmailController()

    async def login(self, data: LoginRequest):
        email = data.email
        user = await self.crud.get_one({"email": email})
        if not user:
            raise ErrorCode.InvalidCredentials()

        if not auth_services.check_password(data.password, user["password"].encode()):
            raise ErrorCode.InvalidCredentials()

        token_data = {
            "uid": str(user.get("_id")),
            "email": user.get("email"),
            "permission": user.get("permission"),
            "remember_me": data.remember_me
        }
        token = await auth_services.create_access_token(token_data)

        return {"token_type": "bearer", "access_token": token}

    async def get_otp(self, email: str):

        user = await self.crud.get_one({"email": email})
        if not user: raise ErrorCode.EmailNotFound()

        otp_code = random.randint(100000, 999999)

        expire_otp = Helper.get_timestamp() + 5 * 60  # 5 minures = 300 seconds

        await self.crud.collection.update_one(
            {"_id": ObjectId(user["_id"])},
            {
                "$set": {
                    "otp_code": otp_code,
                    "expire_otp": expire_otp,
                }
            }
        )
        # Call send OTP mail Rabbitmq
        await self.email_controller.send_email_producer(email=user["email"], fullname=user["fullname"], data={"otp_code": str(otp_code)}, mail_type="otp_val")

        return {"message": f"OTP sent to {email} and valid for 5 minutes"}
    
    
    async def forgot_password(self, data: ForgotPasswordRequest):
        user = await self.crud.get_one({"email": data.email})
        if not user:
            raise ErrorCode.EmailNotFound()
        if "otp_code" not in user or "expire_otp" not in user:
            raise ErrorCode.InvalidOTP()
        
        if str(user["otp_code"]) != str(data.otp_code):
            raise ErrorCode.InvalidOTP()
        
        if Helper.get_timestamp() > user["expire_otp"]:
            raise ErrorCode.ExpiredOTP()
        
        hashed_password = (await auth_services.hash_password(data.new_password)).decode()

        await self.crud.collection.update_one(
            {"_id": ObjectId(user["_id"])},
            {
                "$set": {"password": hashed_password},
                "$unset": {"otp_code": "", "expire_otp": ""}
            }
        )
        return {"message": "Password has been reset successfully"}
