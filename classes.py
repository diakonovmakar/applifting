from config import take_token
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import requests as rq

from sqlalchemy import create_engine
import json
from json import dumps

import config

db_connect = create_engine('sqlite:///tables.sqlite')
app = Flask(__name__)

"""
сделай отдельный класс,
который будет работать только с базой данных.
Там должны быть методы для создания, чтения и обновления товаров.
Назови его ProductRepository. Соединение с базой данных
не создавай внутри класса, а передавай его в конструктор.
"""

class ProductRepository:
    def __init__(self, id='', name='', description=''):
        self.conn = db_connect.connect() # connect to database
        self.id = id
        self.name = name
        self.desc = description

    def create_product(self):
        query = self.conn.execute(f"""
                                    INSERT INTO
                                    products (name, description)
                                    VALUES
                                    ('{self.name}', '{self.desc}');
                                    """)
        return query

    def read_product(self):
        query = self.conn.execute(f"""
                                    SELECT *
                                    FROM products
                                    WHERE id={self.id};
                                    """)
        return query
        
    def update_product_name(self):
        query = self.conn.execute(f"""
                                    UPDATE products
                                    SET name='{self.name}'
                                    WHERE id={self.id};
                                    """)
        return query

    def update_product_description(self):
        query = self.conn.execute(f"""
                                    UPDATE products
                                    SET description='{self.desc}'
                                    WHERE id={self.id};
                                    """)
        return query

    def delete_product(self):
        query = self.conn.execute(f"""
                                    DELETE FROM products
                                    WHERE id={self.id};
                                    """)
        return query

    def read_offers(self):
        query = self.conn.execute(f"""
                                    SELECT *
                                    FROM offers
                                    WHERE id={self.id};
                                    """)
        return query

class OffersServiceClient:
    def __init__(self, id='', name='', description=''):
        self.id = id
        self.name = name
        self.desc = description
        self.url = 'https://applifting-python-excercise-ms.herokuapp.com/api/v1/'
        self.url_params =   {'auth': 'auth/',
                            'products': 'products/',
                            'register': 'register/',
                            'offers': 'offers/'}
        self.token = take_token(self.url)

    def take_token(self):
        response = rq.post(f'{config.url}{config.url_params["auth"]}')
        token = json.loads(response.text)
        return token

    def product_register(self):
        headers = {'Bearer': f'{self.token["access_token"]}'}
        data = {'id': f'{self.id}',
                'name': f'{self.name}',
                'description': f'{self.desc}'}
        url = f'{config.url}{config.url_params["products"]}{config.url_params["register"]}'
        response = rq.post(url, headers=headers, json=data)
        if response.status_code == 201:
            print(f'Item with id #{self.id} was registered successfully')
        return json.loads(response.text)

    def products_offer(self):
        headers = {'Bearer': f'{self.token["access_token"]}'}
        url = f'{config.url}{config.url_params["products"]}{self.id}/{config.url_params["offers"]}'
        response = rq.get(url, headers=headers)
        return json.loads(response.text)

token = OffersServiceClient()
dosquran = OffersServiceClient('1', 'Dosquran', 'TLDR')
print(dosquran.product_register())
print(dosquran.products_offer())