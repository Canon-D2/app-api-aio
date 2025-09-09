from fastapi import status
from fastapi.exceptions import HTTPException


class StandardException(HTTPException):
    def __init__(self, **kwargs):
        super().__init__(status_code=kwargs.get("status", 400), detail=kwargs)


class ErrorCode:
    @staticmethod
    def EventNotFound():
        return StandardException(
            type="fes/error/event-not-found",
            status=status.HTTP_404_NOT_FOUND,
            title="Event not found",
            detail="The event ID provided does not exist."
        )

    @staticmethod
    def InvalidTicket(ticket_type: str = ""):
        return StandardException(
            type="fes/error/invalid-ticket",
            status=status.HTTP_400_BAD_REQUEST,
            title="Invalid ticket type or quantity",
            detail=f"The ticket type `{ticket_type}` is invalid or exceeds available quantity."
        )

    @staticmethod
    def QrTokenNotFound():
        return StandardException(
            type="fes/error/qr-token-not-found",
            status=status.HTTP_404_NOT_FOUND,
            title="QR token not found",
            detail="The QR token provided does not exist."
        )
    
    @staticmethod
    def StaffNotFound():
        return StandardException(
            type="users/error/invalid-id",
            status=status.HTTP_404_NOT_FOUND,
            title="Staff not found",
            detail="The user ID provided does not exist in the system."
        )