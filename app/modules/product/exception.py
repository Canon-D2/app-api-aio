from fastapi import status
from fastapi.exceptions import HTTPException


class StandardException(HTTPException):
    def __init__(self, **kwargs):
        super().__init__(status_code=kwargs.get("status", 400), detail=kwargs)


class ErrorCode:

    @staticmethod
    def InvalidProductId():
        return StandardException(
            type="products/error/invalid-id",
            status=status.HTTP_404_NOT_FOUND,
            title="Product not found",
            detail="The product ID provided does not exist in the system."
        )