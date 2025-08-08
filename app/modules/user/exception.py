from fastapi import status
from fastapi.exceptions import HTTPException


class StandardException(HTTPException):
    def __init__(self, **kwargs):
        super().__init__(status_code=kwargs.get("status", 400), detail=kwargs)


class ErrorCode:
    @staticmethod
    def EmailExisted(email: str = ""):
        return StandardException(
            type="users/warning/email-existed",
            status=status.HTTP_400_BAD_REQUEST,
            title="Email already exists.",
            detail=f"The email `{email}` is already used by another user."
        )

    @staticmethod
    def InvalidUserId():
        return StandardException(
            type="users/error/invalid-id",
            status=status.HTTP_404_NOT_FOUND,
            title="User not found",
            detail="The user ID provided does not exist in the system."
        )