from fastapi import status
from fastapi.exceptions import HTTPException


class StandardException(HTTPException):
    def __init__(self, **kwargs):
        super().__init__(status_code=kwargs.get("status", 400), detail=kwargs)


class ErrorCode:
    @staticmethod
    def InvalidEmailData():
        return StandardException(
            type="email/error/invalid-data",
            status=status.HTTP_400_BAD_REQUEST,
            title="Invalid Email Data",
            detail="Provided email data is invalid or incomplete."
        )

    @staticmethod
    def RabbitConnect():
        return StandardException(
            type="rabbitmq/error/connection-failed",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            title="RabbitMQ Connection Failed",
            detail="Cannot connect to RabbitMQ server."
        )

    @staticmethod
    def RabbitProducer():
        return StandardException(
            type="rabbitmq/error/publish-failed",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            title="RabbitMQ Publish Failed",
            detail="Failed to publish message to RabbitMQ."
        )

    @staticmethod
    def RabbitConsumer():
        return StandardException(
            type="rabbitmq/error/consumer-failed",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            title="RabbitMQ Consumer Failed",
            detail="Failed to process message from RabbitMQ."
        )

    @staticmethod
    def SendMailFailed():
        return StandardException(
            type="email/error/send-failed",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            title="Email Send Failed",
            detail="Failed to send email. Please try again later."
        )