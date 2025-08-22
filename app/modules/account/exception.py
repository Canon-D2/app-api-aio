from fastapi import status
from fastapi.exceptions import HTTPException


class StandardException(HTTPException):
    def __init__(self, **kwargs):
        super().__init__(status_code=kwargs.get("status", 400), detail=kwargs)


class ErrorCode:
    @staticmethod
    def InvalidCredentials():
        return StandardException(
            type="auth/error/invalid-credentials",
            status=status.HTTP_400_BAD_REQUEST,
            title="Invalid login credentials",
            detail="Incorrect email or password."
        )
    @staticmethod
    def EmailNotFound():
        return StandardException(
            type="auth/error/email-not-found",
            status=status.HTTP_404_BAD_REQUEST,
            title="Email not Found",
            detail="Email does not exist"
        )
    
    def InvalidOTP():
        return StandardException(
            type="auth/error/invalid-otp",
            status=status.HTTP_400_BAD_REQUEST,
            title="Invalid OTP",
            detail="OTP is incorrect"
        )
    
    def ExpiredOTP():
        return StandardException(
            type="auth/error/expired-otp",
            status=status.HTTP_400_BAD_REQUEST,
            title="Expired OTP",
            detail="OTP has expired"
        )