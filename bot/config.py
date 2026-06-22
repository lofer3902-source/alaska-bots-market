import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
TMA_URL = os.getenv("TMA_URL")
ADMIN_ID = int(os.getenv("ADMIN_ID"))