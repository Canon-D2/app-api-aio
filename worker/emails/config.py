import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="env/worker.env")

RABBITMQ_URL = os.getenv("RABBITMQ_URL")
USERNAME_SMTP = os.getenv("USERNAME_SMTP")
PASSWORD_SMTP = os.getenv("PASSWORD_SMTP")
HOST_SMTP = os.getenv("HOST_SMTP")
PORT_SMTP = os.getenv("PORT_SMTP")