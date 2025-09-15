import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="env/worker.env")

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_CHAT_TOPIC = os.getenv("KAFKA_CHAT_TOPIC")
KAFKA_CHAT_GROUP = os.getenv("KAFKA_CHAT_GROUP")