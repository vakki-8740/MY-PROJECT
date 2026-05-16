import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_key')
    DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')
    DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL', '')