import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="env/app.env")

AIO_DATABASE_NAME = os.getenv('DATABASE_NAME')
LOGS_DATABASE_NAME = os.getenv('DATABASE_LOGS_NAME')
TRACKING_DATABASE_NAME = os.getenv('DATABASE_TRACKING_NAME')