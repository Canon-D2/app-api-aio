from fastapi import status
from fastapi.exceptions import HTTPException


class StandardException(HTTPException):
    def __init__(self, **kwargs):
        super().__init__(status_code=kwargs.get("status", 400), detail=kwargs)


class ErrorCode:
    @staticmethod
    def CartEmpty():
        return StandardException(
            type="invoices/error/cart-empty",
            status=status.HTTP_400_BAD_REQUEST,
            title="Cart is empty",
            detail="Cart is empty, cannot create invoice"
        )

    @staticmethod
    def CartNotFound():
        return StandardException(
            type="invoices/error/cart-not-found",
            status=status.HTTP_404_NOT_FOUND,
            title="Cart not found",
            detail="No cart found for this user"
        )

    @staticmethod
    def InvoiceNotFound():
        return StandardException(
            type="invoices/error/not-found",
            status=status.HTTP_404_NOT_FOUND,
            title="Invoice not found",
            detail="The Invoice provided does not exist in the system"
        )
    
    @staticmethod
    def ProductNotFound():
        return StandardException(
            type="product/error/not-found",
            status=status.HTTP_404_NOT_FOUND,
            title="Product not found",
            detail="The product ID provided does not exist in the system."
        )

    @staticmethod
    def InvalidInvoiceId():
        return StandardException(
            type="invoices/error/invalid-id",
            status=status.HTTP_400_BAD_REQUEST,
            title="Invalid invoice id",
            detail="The invoice id provided is not valid"
        )

    @staticmethod
    def InsufficientStock(product_name: str, inventory: int):
        return StandardException(
            type="cart/error/insufficient-stock",
            status=status.HTTP_409_CONFLICT,
            title="Insufficient stock",
            detail=f"Product '{product_name}' quantity {inventory} not enough."
        )
