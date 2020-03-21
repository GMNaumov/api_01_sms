import time
import os
import requests
import sys

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

    try:
        response = requests.post(vk_url, params=params)
        response_result = response.json().get('response')[0]
        status = response_result['online']
        return status
    except requests.exceptions.ConnectionError as connection_error:
        exception_processing(connection_error)
    except requests.exceptions.HTTPError as http_error:
        exception_processing(http_error)
    except ValueError as value_error:
        exception_processing(value_error)
    except IndexError as index_error:
        exception_processing(index_error)
    except Exception as another_exception:
        exception_processing(another_exception)


def exception_processing(exception):
    print(f'Except details: {exception}')
    sys.exit()


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
