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
            detail="Invoice not found"
        )

    @staticmethod
    def InvalidInvoiceId():
        return StandardException(
            type="invoices/error/invalid-id",
            status=status.HTTP_400_BAD_REQUEST,
            title="Invalid invoice id",
            detail="The invoice id provided is not valid"
        )
