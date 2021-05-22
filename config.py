from flask.json import jsonify
import requests as rq
import json

token = '22fa2dfa-25a2-4f73-b4ec-9b908fddef9f' 
url = 'https://applifting-python-excercise-ms.herokuapp.com/api/v1/'
url_params = {'auth': 'auth/',
              'products': 'products/',
              'register': 'register/',
              'offers': 'offers/'}



'''
def take_token(url):
    response = rq.post(f'{url}{url_params["auth"]}')
    token = json.loads(response.text)
    return print(token)

print(take_token(url))
'''
