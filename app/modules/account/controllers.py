from .services import AccountService, account_crud
from .schemas import LoginRequest, GetOTPRequest, ForgotPasswordRequest


class AccountController:
    def __init__(self):
        self.service = AccountService(account_crud)

    async def login(self, data: LoginRequest):
        return await self.service.login(data)
    
    async def get_otp(self, data: GetOTPRequest):
        return await self.service.get_otp(data.email)

    async def forgot_password(self, data: ForgotPasswordRequest):
        return await self.service.forgot_password(data)