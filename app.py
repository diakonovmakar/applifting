#Libraries
import json
import sqlite3
from sqlite3 import Error
import requests as rq
#Files
import config
import queries as q




def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def product_register(id, name, description):
    headers = {'Bearer': f'{token["access_token"]}'}
    data = {'id': f'{id}',
            'name': f'{name}',
            'description': f'{description}'}
    url = f'{config.url}{config.url_params["products"]}{config.url_params["register"]}'
    response = rq.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print(f'Item with id #{id} was registered successfully')
    return json.loads(response.text)


def products_offer(id):
    headers = {'Bearer': f'{token["access_token"]}'}
    url = f'{config.url}{config.url_params["products"]}{id}/{config.url_params["offers"]}'
    response = rq.get(url, headers=headers)
    return json.loads(response.text)


token = config.take_token(config.url)
#connection = create_connection("R:\\Dev/project1/tables.sqlite")
#execute_query(connection, q.create_products_table)
#execute_query(connection, q.create_offers_table)
print(product_register(int(1), 'Benzinová sekačka Dosquarna', 'Nejlepší sekačka na trhu. TLDR'))
#products_offer(1)
