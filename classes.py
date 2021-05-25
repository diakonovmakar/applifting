# external libraries
from decouple import config
import requests as rq
# libraries
import json


class ProductRepository:
    def __init__(self, connection):
        self.conn = connection  # connect to database

    def create_product(self, id: int, name: str, desc: str):
        self.conn.execute("""
            INSERT INTO
            products (id, name, description)    
            VALUES
            (:id, :name, :desc);
            """, {'id': id, 'name': name, 'desc': desc})
        self.conn.commit()
        #print(f'Product with id #{id} was created!')

    def read_product(self, id: int):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT *
            FROM products
            WHERE id=:id;
            """, {'id': id})
        return cursor.fetchall()

    def read_all_product_ids(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id
            FROM products;
            """)
        return cursor.fetchall()

    def read_all_products(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT *
            FROM products;
            """)
        data = cursor.fetchall()
        result = []
        for i in data:
            item = {'id': i[0],
                    'name': i[1],
                    'description': i[2]}
            result.append(item)
        return result

    def update_product(self, name: str, desc: str, id: int):
        self.conn.execute("""
            UPDATE products
            SET name=:name, description=:desc
            WHERE id=:id;
            """, {'name': name, 'desc': desc, 'id': id})
        self.conn.commit()
        #print(f'Product with id #{id} was updated!')

    def update_product_name(self, name: str, id: int):
        self.conn.execute("""
            UPDATE products
            SET name=:name
            WHERE id=:id;
            """, {'name': name, 'id': id})
        self.conn.commit()
        #print(f'Name of product with id #{id} was updated!')

    def update_product_description(self, desc: str, id: int):
        self.conn.execute("""
            UPDATE products
            SET description=:desc
            WHERE id=:id;
            """, {'desc': desc, 'id': id})
        self.conn.commit()
        #print(f'Description of product with id #{id} was updated!')

    def delete_product(self, id: int):
        self.conn.execute("""
            DELETE FROM products
            WHERE id=:id;
            """, {'id': id})
        self.conn.commit()
        #print(f'Product with id #{id} was deleted!')

    def create_offer(self, product_id: int, offer: dict):
        data = {'product_id': product_id,
                'id': offer['id'],
                'price': offer['price'],
                'items_in_stock': offer['items_in_stock']}
        self.conn.execute("""
            INSERT INTO
            offers(product_id, id, price, items_in_stock)
            VALUES
            (:product_id, :id, :price, :items_in_stock);
            """, data)
        self.conn.commit()
        #id = data['id']
        #print(f'Offer with id #{id} was created!')

    def read_all_offer_ids(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id
            FROM offers;
            """)
        return cursor.fetchall()


    def read_all_offers(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT *
            FROM offers;
            """)
        data = cursor.fetchall()
        result = []
        for i in data:
            item = {'product_id': i[0],
                    'offer_id': i[1],
                    'price': i[2],
                    'items_in_stock': i[3]}
            result.append(item)
        return result

    def read_offer(self, product_id: int):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT *
            FROM offers
            WHERE product_id=:product_id;
            """, {'product_id': product_id})
        data = cursor.fetchall()
        result = []
        for i in data:
            item = {'product_id': '',
                              'offer_id': '',
                              'price': '',
                              'items_in_stock': ''}
            item['product_id'] = i[0]
            item['offer_id'] = i[1]
            item['price'] = i[2]
            item['items_in_stock'] = i[3]
            result.append(item)
        return result

    def update_offer(self, product_id: int, offer: dict):
        data = {'product_id': product_id,
                'id': offer['id'],
                'price': offer['price'],
                'items_in_stock': offer['items_in_stock']}
        self.conn.execute("""
            UPDATE offers
            SET price=:price, items_in_stock=:items_in_stock
            WHERE id=:id AND product_id=:product_id;
            """, data)
        self.conn.commit()
        #print(f'Offer with id #{data[id]} was updated!')

    def delete_offer(self, product_id: int):
        self.conn.execute("""
            DELETE FROM offers
            WHERE product_id=:product_id;
            """, {'product_id': product_id})
        self.conn.commit()
        #print(f'Offers for product with id #{product_id} was deleted!')

    def delete_offer_by_id(self, offer_id: int):
        self.conn.execute("""
            DELETE FROM offers
            WHERE id=:offer_id;
            """, {'offer_id': offer_id})
        self.conn.commit()
        #print(f'Offer with id #{offer_id} was deleted!')

    def close_connection(self):
        self.conn.close()
        #print('Connection was closed successful')


class OffersServiceClient:
    def __init__(self):
        self.url = config('BASE_URL')
        self.token = config('TOKEN')

    def take_token(self):
        url= f'{self.url}/auth/'
        response = rq.post(url)
        return json.loads(response.text)

    def register_product(self, id, name, desc):
        headers = {'Bearer': self.token}
        data = {'id': f'{id}',
                'name': f'{name}',
                'description': f'{desc}'}
        url = f'{self.url}/products/register/'
        response = rq.post(url, headers=headers, json=data)
        #if response.status_code == 201:
            #print(f'Product with id #{id} was registered!')
        return json.loads(response.text)

    def product_offers(self, id):
        headers = {'Bearer': self.token}
        url = f'{self.url}/products/{id}/offers/'
        response = rq.get(url, headers=headers)
        return json.loads(response.text)

