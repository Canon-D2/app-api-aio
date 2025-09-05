import json, aio_pika
from .config import RABBITMQ_URL
from .exception import ErrorCode
from .services import EmailService

class RabbitMQHandler:
    def __init__(self, queue_name: str = "email_queue"):
        self.queue_name = queue_name
        self.connection = None
        self.channel = None
        self.service = EmailService()

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
            raise ErrorCode.RabbitConnect()

    async def producer(self, payload: dict):
        try:
            await self.connect()
            
            body = json.dumps(payload).encode()
            
            await self.channel.default_exchange.publish(aio_pika.Message(body=body), routing_key=self.queue_name)
            
            # print(f"[RabbitMQ] Published message for {data.email}")
        except Exception as e:
            raise ErrorCode.RabbitProducer()


    async def consumer(self):
        await self.connect()
        queue = await self.channel.declare_queue(self.queue_name, durable=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    try:
                        payload = json.loads(message.body)
                        data = payload.get("data", {})  
                        print(f"[Consumer] Payload data details", payload)

                        if payload.get("mail_type") == "otp_val":
                            await self.service.send_otp_email(email=payload.get("email"), fullname=payload.get("fullname"), data=data["otp_code"])

                        if payload.get("mail_type") == "bill_inf":
                            await self.service.send_invoice_email(email=payload.get("email"), fullname=payload.get("fullname"), data=data)
                        
                        else: raise ErrorCode.InvalidEmailData()

                    except Exception:
                        raise ErrorCode.RabbitConsumer()