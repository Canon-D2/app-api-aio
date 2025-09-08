from fastapi import status
from fastapi.exceptions import HTTPException


class StandardException(HTTPException):
    def __init__(self, **kwargs):
        super().__init__(status_code=kwargs.get("status", 400), detail=kwargs)


class ErrorCode:
    @staticmethod
    def InvalidToken():
        return StandardException(
            type="auth/error/invalid-token",
            status=status.HTTP_401_BAD_REQUEST,
            title="Invalid Token",
            detail="Login failed, please try again."
        )

    @staticmethod
    def TokenExpired():
        return StandardException(
            type="auth/error/token-expired",
            status=status.HTTP_401_BAD_REQUEST,
            title="Token Expired",
            detail="Login expired, please try again."
        )

    @staticmethod
    def PermissionDenied():
        return StandardException(
            type="auth/error/permission-denied",
            status=status.HTTP_403_FORBIDDEN,
            title="Permission denied",
            detail="Access denied, please contact administrator."
        )
