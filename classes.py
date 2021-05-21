#external libraries
from flask.json import jsonify
import requests as rq
#libraries
import json
#files
import config


class ProductRepository:
    def __init__(self, connection):
        self.conn = connection # connect to database        

    def create_product(self, id, name, desc):
        self.conn.execute("""
                        INSERT INTO
                        products (id, name, description)
                        VALUES
                        (:id, :name, :desc);
                        """, {'id': id, 'name': name, 'desc': desc})
        self.conn.commit()
        self.conn.close()
        print('OK')                     
        
    def read_product(self, id):
        cursor = self.conn.cursor()
        cursor.execute("""
                        SELECT *
                        FROM products
                        WHERE id=:id;
                        """, {'id':id})
        return jsonify(cursor.fetchall())

    def read_all_products(self):
        cursor = self.conn.cursor()
        cursor.execute("""
                        SELECT *
                        FROM products;
                        """)
        return jsonify(cursor.fetchall())

    def update_product_name(self, name, id):
        self.conn.execute("""
                        UPDATE products
                        SET name=:name
                        WHERE id=:id;
                        """, {'name': name, 'id': id})
        self.conn.commit()
        self.conn.close()

    def update_product_description(self, desc, id):
        self.conn.execute("""
                        UPDATE products
                        SET description=:desc
                        WHERE id=:id;
                        """, {'desc': desc, 'id': id})
        self.conn.commit()
        self.conn.close()
        
    def delete_product(self, id):
        self.conn.execute("""
                        DELETE FROM products
                        WHERE id=:id;
                        """, {'id': id})
        self.conn.commit()
        self.conn.close()
        
    def create_offer(self, id, price, items_in_stock):
        self.conn.execute("""
                        INSERT INTO
                        offers(id, price, items_in_stock)
                        VALUES
                        (:id, :price, :items_in_stock);
                        """, {'id': id, 'price': price, 'items_in_stock': items_in_stock})
        self.conn.commit()
        self.conn.close()
        print(f'Offer with id #{id} was created!')

    def read_all_offers(self):
        cursor = self.conn.cursor()
        cursor.execute("""
                        SELECT *
                        FROM offers;
                        """)
        return jsonify(cursor.fetchall())

    def read_offer(self, id):
        cursor = self.conn.cursor()
        cursor.execute("""
                        SELECT *
                        FROM offers
                        WHERE id=:id;
                        """, {'id': id})
        return jsonify(cursor.fetchall())

    def update_offer(self, dict_of_data):
        self.conn.execute("""
                        UPDATE offers
                        SET price=:price, items_in_stock=:items_in_stock
                        WHERE id=:id;
                        """, dict_of_data)
        self.conn.commit()
        self.conn.close()
        print(f'Offer with id #{id} was updated')
    
    def delete_offer(self, id):
        self.conn.execute("""
                        DELETE FROM offers
                        WHERE id=:id;
                        """, {'id': id})
        self.conn.commit()
        self.conn.close()
        print(f'Offer with id #{id} was deleted')


class OffersServiceClient:
    def __init__(self):   
        self.token = config.token

    def product_register(self, id, name, desc):
        headers = {'Bearer': self.token}
        data = {'id': f'{id}',
                'name': f'{name}',
                'description': f'{desc}'}
        url = f'{config.url}{config.url_params["products"]}{config.url_params["register"]}'
        response = rq.post(url, headers=headers, json=data)
        if response.status_code == 201:
            print(f'Item with id #{id} was registered successfully')
        return json.loads(response.text)

    def products_offer(self, id):
        headers = {'Bearer': self.token}
        url = f'{config.url}{config.url_params["products"]}{id}/{config.url_params["offers"]}'
        response = rq.get(url, headers=headers)
        return json.loads(response.text)


offers_service = OffersServiceClient()
print(offers_service.product_register(1, '1234', 'qwerty'))