import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="env/worker.env")

REDIS_DISABLE_COMMANDS = os.getenv("REDIS_DISABLE_COMMANDS")
REDIS_HOST_PASSWORD = os.getenv("REDIS_HOST_PASSWORD")
ENABLE_OVERCOMMIT_MEMORY = os.getenv("ENABLE_OVERCOMMIT_MEMORY")
REDIS_AOF_ENABLED = os.getenv("REDIS_AOF_ENABLED")