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
    
    @staticmethod
    def SerialAlreadyExists():
        return StandardException(
            type="products/error/serial-already-exists",
            status=status.HTTP_400_BAD_REQUEST,
            title="Serial already exists",
            detail="The serial number provided already exists in this product."
        )

    @staticmethod
    def SerialNotFound():
        return StandardException(
            type="products/error/serial-not-found",
            status=status.HTTP_404_NOT_FOUND,
            title="Serial not found",
            detail="The serial number provided does not exist in this product."
        )