from .services import kafka_service
from .config import KAFKA_CHAT_TOPIC


class KafkaController:
    async def publish_message(self, channel_id: str, token: str, message: dict):
        
        await kafka_service.send(topic=KAFKA_CHAT_TOPIC, key=channel_id, 
            value={"channel_id": channel_id, "token": token, **message}
        )

kafka_controller = KafkaController()
