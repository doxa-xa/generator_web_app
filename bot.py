import os
from dotenv import load_dotenv
import requests
import time

load_dotenv()
CHAT_IDS = [8955213165,8649603585]
def send_notification(message:str):
    URL = f'https://api.telegram.org/bot{os.environ["TELEGRAM_BOT_TOKEN"]}/sendMessage'
    for chat_id in CHAT_IDS:
        try:
            payload = {
                "chat_id":chat_id,
                "text":message
            }

            res = requests.post(URL,payload)

            if res.status_code == 200:
                print("message sent successfully!")
            else:
                print(f"failed to send message: {res.text}")
        except Exception as e:
                print("An error occured")
        time.sleep(2)
    


