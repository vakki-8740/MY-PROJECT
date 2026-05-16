import requests
from config import Config

def send_to_discord(message):
    if not Config.DISCORD_WEBHOOK_URL:
        return print("⚠️ Discord Webhook not set in .env")
    try:
        requests.post(Config.DISCORD_WEBHOOK_URL, json={"content": message})
        return True
    except Exception as e:
        print(f"❌ Discord Error: {e}")
        return False