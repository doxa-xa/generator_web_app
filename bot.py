import os
from dotenv import load_dotenv
import requests
import time

load_dotenv()
#CHAT_IDS = [8955213165,8649603585,5653908863]

def check_for_new_members():
    URL = f'https://api.telegram.org/bot{os.environ["TELEGRAM_BOT_TOKEN"]}/getUpdates'
    try:
        res = requests.get(URL)
        if res.status_code == 200:
            data = res.json()
            for update in data['result']:
                if 'message' in update and 'chat' in update['message']:
                    new_members = update['message']['chat']
                    for member in new_members:
                        print(f"New member joined: {member['first_name']} (ID: {member['id']})")
                        send_notification(f"New member joined: {member['first_name']} (ID: {member['id']})")
                        with open('members.txt', 'a') as members_file:
                            members_file.write(f",{member['id']}")
        else:
            print(f"Failed to fetch updates: {res.text}")

        with open ('members.txt','r') as members_file:
                    for line in members_file:
                        chat_ids = line.strip().split(',')
                    return chat_ids
    except Exception as e:
        print(f"An error occurred while checking for new members: {e}")
        with open ('members.txt','r') as members_file:
            for line in members_file:
                chat_ids = line.strip().split(',')
        return chat_ids
        


def send_notification(message:str):
    chat_ids = check_for_new_members()
    URL = f'https://api.telegram.org/bot{os.environ["TELEGRAM_BOT_TOKEN"]}/sendMessage'
    for chat_id in chat_ids:
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
    


