from fastapi import status
from fastapi.exceptions import HTTPException


class StandardException(HTTPException):
    def __init__(self, **kwargs):
        super().__init__(status_code=kwargs.get("status", 400), detail=kwargs)


class ErrorCode:
    @staticmethod
    def ThreadNotFound():
        return StandardException(
            type="threads/error/not-found",
            status=status.HTTP_404_NOT_FOUND,
            title="Thread not found",
            detail="The thread ID provided does not exist in the system."
        )

    @staticmethod
    def PostNotFound():
        return StandardException(
            type="posts/error/not-found",
            status=status.HTTP_404_NOT_FOUND,
            title="Post not found",
            detail="The post ID provided does not exist in the system."
        )

    @staticmethod
    def ReactionNotFound():
        return StandardException(
            type="posts/error/reaction-not-found",
            status=status.HTTP_404_NOT_FOUND,
            title="Reaction not found",
            detail="The reaction for this user does not exist."
        )
    
    @staticmethod
    def UserNotFound():
        return StandardException(
            type="users/error/invalid-id",
            status=status.HTTP_404_NOT_FOUND,
            title="User not found",
            detail="The user ID provided does not exist in the system."
        )