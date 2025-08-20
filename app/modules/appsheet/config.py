import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="env/app.env")

URL_APPSHEET = os.getenv("URL_APPSHEET")