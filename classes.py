#external libraries
from config import take_token
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import requests as rq
#libraries
from sqlalchemy import create_engine
import json
from json import dumps
#files
import config

db_connect = create_engine('sqlite:///tables.sqlite')
app = Flask(__name__)

#, id='', name='', description='' 
#self.id = id
#self.name = name
#self.desc = description

class ProductRepository:
    def __init__(self):
        self.conn = db_connect.connect() # connect to database
        

    def create_product(self, name, desc):
        query = self.conn.execute(f"""
                                    INSERT INTO
                                    products (name, description)
                                    VALUES
                                    (?, ?);
                                    """, (f'{name}', f'{desc}'))
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

dosquana = ProductRepository()
dosquana.create_product('Dosquana', 'TLDR')