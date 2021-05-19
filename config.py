import requests as rq
import json

url = 'https://applifting-python-excercise-ms.herokuapp.com/api/v1/'
url_params = {'auth': 'auth/',
              'products': 'products/',
              'register': 'register/',
              'offers': 'offers/'}


def take_token(url):
    response = rq.post(f'{url}{url_params["auth"]}')
    token = json.loads(response.text)
    return token

