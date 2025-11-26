import requests
import os
from dotenv import load_dotenv

#load env 
load_dotenv()

def sendmessage(message):
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    if not webhook_url:
        print("ไม่พบ DISCORD_WEBHOOK_URL ใน .env")
        return
    data = {'content': message}
    try:
        response = requests.post(webhook_url, json=data)
        if response.status_code == 204:
            print("Discord Notification sent!")
        else:
            print(f"Discord status: {response.status_code}")
    except Exception as e:
        print(f"Failed to send Discord: {e}")
