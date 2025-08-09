from .rabbitmq import RabbitMQHandler
from .models import EmailData

class EmailController:
    def __init__(self):
        self.rabbitmq = RabbitMQHandler()

    async def send_email(self, data: dict):
        try:
            email_data = EmailData(**data)
            await self.rabbitmq.publish(email_data)
        except Exception as e:
            print(f"[EmailController] Error sending message to RabbitMQ: {e}")
