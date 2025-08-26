from fastapi import status
from fastapi.exceptions import HTTPException


class StandardException(HTTPException):
    def __init__(self, **kwargs):
        super().__init__(status_code=kwargs.get("status", 400), detail=kwargs)


class ErrorCode:
    @staticmethod
    def ItemNotFound():
        return StandardException(
            type="cart/error/item-not-found",
            status=status.HTTP_404_NOT_FOUND,
            title="Item not found",
            detail="The item does not exist in the cart."
        )

    @staticmethod
    def GeneralError(message: str):
        return StandardException(
            type="cart/error/general",
            status=status.HTTP_400_BAD_REQUEST,
            title="Cart operation failed",
            detail=message
        )