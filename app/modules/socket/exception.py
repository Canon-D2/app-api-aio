from fastapi import status
from fastapi.exceptions import HTTPException


class StandardException(HTTPException):
    def __init__(self, **kwargs):
        super().__init__(status_code=kwargs.get("status", 400), detail=kwargs)


class ErrorCode:
    @staticmethod
    def UserNotFound():
        return StandardException(
            type="user/not-found",
            status=status.HTTP_404_NOT_FOUND,
            title="User not found",
            detail="The specified user does not exist."
        )

    @staticmethod
    def ChannelNotFound():
        return StandardException(
            type="channel-not-found",
            status=status.HTTP_404_NOT_FOUND,
            title="Channel not found",
            detail="The specified chat channel does not exist."
        )