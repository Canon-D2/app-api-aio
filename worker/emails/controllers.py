from .rabbitmq import RabbitMQHandler
from .exception import ErrorCode

class EmailController:
    def __init__(self):
        self.rabbitmq = RabbitMQHandler()

    async def send_email_producer(self, data: dict, mail_type: str):
        try:
            await self.rabbitmq.producer(data, mail_type)
        except Exception as e:
            # print(f"[EmailController] Error sending message to RabbitMQ: {e}")
            raise ErrorCode.InvalidEmailData()
