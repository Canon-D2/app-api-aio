import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="env/app.env")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

ACCESS_TOKEN_EXPIRE_DAY = 3
REMEMBER_TOKEN_DAY = 30