from .rabbitmq import RabbitMQHandler
from .schemas import EmailData
from .exception import ErrorCode

class EmailController:
    def __init__(self):
        self.rabbitmq = RabbitMQHandler()

    async def send_email_producer(self, data: dict):
        try:
            email_data = EmailData(**data)
            await self.rabbitmq.producer(email_data)
        except Exception as e:
            # print(f"[EmailController] Error sending message to RabbitMQ: {e}")
            raise ErrorCode.InvalidEmailData()
