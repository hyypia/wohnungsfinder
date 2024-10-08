import os
from dotenv import load_dotenv


BASE_DIR = os.path.dirname((os.path.abspath(__name__)))

dotenv_path = os.path.join(BASE_DIR, ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")

DB_NAME = os.getenv("DB_NAME", "")

URL = "https://inberlinwohnen.de/wohnungsfinder/"
