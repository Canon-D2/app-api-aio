import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="env/worker.env")

DSN_SENTRY = os.getenv("DSN_SENTRY")