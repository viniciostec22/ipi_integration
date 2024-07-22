import requests
from django.conf import settings


class CallMeBot:

    def __init__(self):
        self.__base_url = settings.CALLMEBOT_API_URL
        self.__phone_number = settings.CALMEBOT_PHONE_NUMBER
        self.__api_key = settings.CALMEBOT_API_KEY

    def send_message(self, messege):
        response = requests.get(
            url=f'{self.__base_url}?phone={self.__phone_number}&text={messege}&apikey={self.__api_key}'
        )
        return response.text