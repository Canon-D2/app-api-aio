import asyncio, json
from .config import *
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from app.modules.socket.services import socket_service


class KafkaService:
    def __init__(self):
        self._producer: AIOKafkaProducer | None = None
        self._consumer: AIOKafkaConsumer | None = None

    async def start_producer(self):
        if not self._producer:
            self._producer = AIOKafkaProducer(
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                key_serializer=lambda v: v.encode("utf-8"),
            )
            await self._producer.start()

    async def stop_producer(self):
        if self._producer:
            await self._producer.stop()

    async def send(self, topic: str, key: str, value: dict):
        if not self._producer:
            await self.start_producer()
        try:
            result = await self._producer.send_and_wait(topic, key=key, value=value)
            print(f"[KAFKA] Message sent: {result}")
        except Exception as e:
            print(f"[KAFKA] Error sending message: {e}")


    async def start_consumer(self, topic=KAFKA_CHAT_TOPIC, group_id=KAFKA_CHAT_GROUP):
        self._consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            group_id=group_id,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            key_deserializer=lambda v: v.decode("utf-8"),
            auto_offset_reset="earliest" 
        )
        await self._consumer.start()
        asyncio.create_task(self.consume_loop())

    async def stop_consumer(self):
        if self._consumer:
            await self._consumer.stop()

    async def consume_loop(self):
        try:
            async for msg in self._consumer:
                data = msg.value
                try:
                    await socket_service.send_message(data, data.get("token"))
                except Exception as e:
                    print(f"[KAFKA] Error processing message: {e}")
        except Exception as e:
            print(f"[KAFKA] Consumer fatal error: {e}")

kafka_service = KafkaService()
