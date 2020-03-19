import time
import os
import requests

from dotenv import load_dotenv
from twilio.rest import Client


def get_status(user_id):
    load_dotenv()
    vk_url = 'https://api.vk.com/method/users.get'

    params = {
        'access_token': os.getenv('vk_token'),
        'fields': 'online',
        'user_ids': user_id,
        'v': '5.92',
    }

    response = requests.post(vk_url, params=params)
    response_result = response.json().get('response')[0]
    status = response_result['online']
    return status


def sms_sender(sms_text):
    client = Client(os.getenv('twilio_account_sid'), os.getenv('twilio_auth_token'))
    message = client.messages.create(body=f'{sms_text}', from_='+14807254780', to='+79209243400')
    return message.sid


if __name__ == "__main__":
    vk_id = input("Введите id ")
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
