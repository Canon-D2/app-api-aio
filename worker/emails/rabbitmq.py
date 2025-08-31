import json, aio_pika
from .config import RABBITMQ_URL
from .schemas import EmailData
from .exception import ErrorCode
from .services import EmailService

class RabbitMQHandler:
    def __init__(self, queue_name: str = "email_queue"):
        self.queue_name = queue_name
        self.connection = None
        self.channel = None

    async def connect(self):
        try:
            if not self.connection:
                # print(f"[RabbitMQ] Connecting to: {RABBITMQ_URL}")
                self.connection = await aio_pika.connect_robust(RABBITMQ_URL)
                # print("[RabbitMQ] Connection successful.")
                self.channel = await self.connection.channel()
                await self.channel.declare_queue(self.queue_name, durable=True)
                # print(f"[RabbitMQ] Queue declared: {self.queue_name}")
        except Exception as e:
            # print(f"[RabbitMQ] Error while connecting: {e}")
            raise ErrorCode.RabbitConnect()

    async def producer(self, data: EmailData):
        try:
            # print(f"[RabbitMQ] Prepare to publish message: {data.dict()}")
            await self.connect()
            body = json.dumps(data.dict()).encode()
            await self.channel.default_exchange.publish(
                aio_pika.Message(body=body),
                routing_key=self.queue_name
            )
            # print(f"[RabbitMQ] Published message for {data.email}")
        except Exception as e:
            # print(f"[RabbitMQ] Error publishing message: {e}")
            raise ErrorCode.RabbitProducer()

    async def consumer(self):
        await self.connect()
        queue = await self.channel.declare_queue(self.queue_name, durable=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    try:
                        payload = json.loads(message.body)
                        # print(f"[RabbitMQ] Receive message: {payload}")
                        email_data = EmailData(**payload)
                        service = EmailService()
                        await service.send_otp_email(
                            email=email_data.email,
                            fullname=email_data.fullname,
                            otp=email_data.otp
                        )
                    except Exception as e:
                        # print(f"[RabbitMQ] Error processing message: {e}")
                        raise ErrorCode.RabbitConsumer()
