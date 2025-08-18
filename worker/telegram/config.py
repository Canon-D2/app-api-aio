import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="env/worker.env")

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
ENVIRONMENT = os.getenv("ENVIRONMENT")