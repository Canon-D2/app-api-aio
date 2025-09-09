from fastapi import status
from fastapi.exceptions import HTTPException


class StandardException(HTTPException):
    def __init__(self, **kwargs):
        super().__init__(status_code=kwargs.get("status", 400), detail=kwargs)


class ErrorCode:
    @staticmethod
    def InvalidLogin():
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
            status=status.HTTP_404_NOT_FOUND,
            title="Email not Found",
            detail="Email does not exist"
        )
    
    @staticmethod
    def InvalidOTP():
        return StandardException(
            type="auth/error/invalid-otp",
            status=status.HTTP_400_BAD_REQUEST,
            title="Invalid OTP",
            detail="OTP is incorrect"
        )
    
    @staticmethod
    def OTPNotFound():
        return StandardException(
            type="auth/error/otp-not-found",
            status=status.HTTP_404_NOT_FOUND,
            title="OTP not Found",
            detail="OTP does not exist"
        )
    
    def ExpiredOTP():
        return StandardException(
            type="auth/error/expired-otp",
            status=status.HTTP_400_BAD_REQUEST,
            title="Expired OTP",
            detail="OTP has expired"
        )