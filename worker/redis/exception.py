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
    
    @staticmethod
    def DataNotDuplicate():
        return StandardException(
            type="data/error/invalid-id",
            status=status.HTTP_404_NOT_FOUND,
            title="User & Product not found",
            detail="The user ID or Product ID provided does not exist in the system."
        )
    
    @staticmethod
    def InsufficientStock(product_name: str, inventory: int):
        return StandardException(
            type="cart/error/insufficient-stock",
            status=status.HTTP_409_CONFLICT,
            title="Insufficient stock",
            detail=f"Product '{product_name}' quantity {inventory} not enough."
        )
