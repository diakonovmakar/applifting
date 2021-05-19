#external libraries
from sqlalchemy import create_engine
import requests as rq
#libraries
import json
from json import dumps
#files
import config
from config import take_token

db_connect = create_engine('sqlite:///tables.sqlite')
#app = Flask(__name__)

#, id='', name='', description='' 
#self.id = id
#self.name = name
#self.desc = description

#self.id = id
#self.name = name
#self.desc = description

class ProductRepository:
    def __init__(self):
        self.conn = db_connect.connect() # connect to database
        

    def create_product(self, name, desc):
        self.conn.execute(f"""
                        INSERT INTO
                        products (name, description)
                        VALUES
                        (?, ?);
                        """, (name, desc))
        
    def read_product(self, id):
        self.conn.execute(f"""
                        SELECT *
                        FROM products
                        WHERE id=?;
                        """, (id))
        
    def update_product_name(self, name, id):
        self.conn.execute(f"""
                        UPDATE products
                        SET name=(?)
                        WHERE id=(?);
                        """, (name, id))

    def update_product_description(self, desc, id):
        self.conn.execute(f"""
                        UPDATE products
                        SET description=?
                        WHERE id=?;
                        """, (desc, id))
        
    def delete_product(self, id):
        self.conn.execute(f"""
                        DELETE FROM products
                        WHERE id=?;
                        """, (id))
        
    def read_offers(self, id):
        self.conn.execute(f"""
                        SELECT *
                        FROM offers
                        WHERE id=?;
                        """, (id))
        
class OffersServiceClient:
    def __init__(self):   
        self.token = take_token(config.url)

    def take_token(self):
        response = rq.post(f'{config.url}{config.url_params["auth"]}')
        token = json.loads(response.text)
        return token

    def product_register(self, id, name, desc):
        headers = {'Bearer': f'{self.token["access_token"]}'}
        data = {'id': f'{id}',
                'name': f'{name}',
                'description': f'{desc}'}
        url = f'{config.url}{config.url_params["products"]}{config.url_params["register"]}'
        response = rq.post(url, headers=headers, json=data)
        if response.status_code == 201:
            print(f'Item with id #{id} was registered successfully')
        return json.loads(response.text)

    def products_offer(self, id):
        headers = {'Bearer': f'{self.token["access_token"]}'}
        url = f'{config.url}{config.url_params["products"]}{id}/{config.url_params["offers"]}'
        response = rq.get(url, headers=headers)
        return json.loads(response.text)

dosquana = ProductRepository()

dosquana.delete_product(1)
#dosquana.create_product('Dosquana', 'TLDR')
#dosquana.update_product_name('NeDosquana', 1)
#dosquana.update_product_description('---', 1)



