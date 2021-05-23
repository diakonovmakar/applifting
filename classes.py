#external libraries
from decouple import config
import requests as rq
#libraries
import json

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
        print(f'Product with id #{id} was created!')                    
        
    def read_product(self, id):
        cursor = self.conn.cursor()
        cursor.execute("""
                        SELECT *
                        FROM products
                        WHERE id=:id;
                        """, {'id':id})
        return cursor.fetchall()

    def read_all_products(self):
        cursor = self.conn.cursor()
        cursor.execute("""
                        SELECT *
                        FROM products;
                        """)
        data = cursor.fetchall()
        result= []
        for i in data:
            dict_of_result = {'id':'',
                            'name': '',
                            'description': ''}
            dict_of_result['id'] = i[0]
            dict_of_result['name'] = i[1]
            dict_of_result['description'] = i[2]
            result.append(dict_of_result)
        return result

    def update_product(self, name, desc, id):
            self.conn.execute("""
                            UPDATE products
                            SET name=:name, description=:desc
                            WHERE id=:id;
                            """, {'name': name, 'desc': desc, 'id': id})
            self.conn.commit()
            print(f'Product with id #{id} was updated!') 

    def update_product_name(self, name, id):
        self.conn.execute("""
                        UPDATE products
                        SET name=:name
                        WHERE id=:id;
                        """, {'name': name, 'id': id})
        self.conn.commit()
        print(f'Name of product with id #{id} was updated!') 

    def update_product_description(self, desc, id):
        self.conn.execute("""
                        UPDATE products
                        SET description=:desc
                        WHERE id=:id;
                        """, {'desc': desc, 'id': id})
        self.conn.commit()
        print(f'Description of product with id #{id} was updated!')
        
    def delete_product(self, id):
        self.conn.execute("""
                        DELETE FROM products
                        WHERE id=:id;
                        """, {'id': id})
        self.conn.commit()
        print(f'Product with id #{id} was deleted!') 
        
    def create_offer(self, product_id, dict_of_data):
        data = {'product_id': product_id,
                'id': dict_of_data['id'],
                'price': dict_of_data['price'],
                'items_in_stock': dict_of_data['items_in_stock']}
        self.conn.execute("""
                        INSERT INTO
                        offers(product_id, id, price, items_in_stock)
                        VALUES
                        (:product_id, :id, :price, :items_in_stock);
                        """, data)
        self.conn.commit()
        id = data['id']
        print(f'Offer with id #{id} was created!')

    def read_all_offers(self):
        cursor = self.conn.cursor()
        cursor.execute("""
                        SELECT *
                        FROM offers;
                        """)
        data = cursor.fetchall()
        result = []
        for i in data:
            dict_of_result = {'product_id':'',
            'offer_id': '',
            'price': '',
            'items_in_stock': ''}
            dict_of_result['product_id'] = i[0]
            dict_of_result['offer_id'] = i[1]
            dict_of_result['price'] = i[2]
            dict_of_result['items_in_stock'] = i[3]
            result.append(dict_of_result)
        return result
        

    def read_offer(self, product_id):
        cursor = self.conn.cursor()
        cursor.execute("""
                        SELECT *
                        FROM offers
                        WHERE product_id=:product_id;
                        """, {'product_id': product_id})
        data = cursor.fetchall()
        result= []
        for i in data:
            dict_of_result = {'product_id':'',
                'offer_id': '',
                'price': '',
                'items_in_stock': ''}
            dict_of_result['product_id'] = i[0]
            dict_of_result['offer_id'] = i[1]
            dict_of_result['price'] = i[2]
            dict_of_result['items_in_stock'] = i[3]
            result.append(dict_of_result)
        return result

    def update_offer(self, product_id, dict_of_data):
        data = {'product_id': product_id,
                'id': dict_of_data['id'],
                'price': dict_of_data['price'],
                'items_in_stock': dict_of_data['items_in_stock']}
        self.conn.execute("""
                        UPDATE offers
                        SET price=:price, items_in_stock=:items_in_stock
                        WHERE id=:id AND product_id=:product_id;
                        """, data)
        self.conn.commit()
        id = data['id']
        print(f'Offer with id #{id} was updated!')
    
    def delete_offer(self, product_id):
        self.conn.execute("""
                        DELETE FROM offers
                        WHERE product_id=:product_id;
                        """, {'product_id': product_id})
        self.conn.commit()
        print(f'Offer with id #{id} was deleted!')

    def close_connection(self):
        self.conn.close()
        print('Connection was closed successful')


class OffersServiceClient:
    def __init__(self):
        self.url = config('BASE_URL')
        self.token = config('TOKEN')
        self.url_params = {'auth': 'auth',
                        'products': 'products',
                        'register': 'register',
                        'offers': 'offers'}

    def product_register(self, id, name, desc):
        headers = {'Bearer': self.token}
        data = {'id': f'{id}',
                'name': f'{name}',
                'description': f'{desc}'}
        url = f'{self.url}/{self.url_params["products"]}/{self.url_params["register"]}/'
        response = rq.post(url, headers=headers, json=data)
        if response.status_code == 201:
            print(f'Product with id #{id} was registered!')
        return json.loads(response.text)

    def products_offer(self, id):
        headers = {'Bearer': self.token}
        url = f'{self.url}/{self.url_params["products"]}/{id}/{self.url_params["offers"]}/'
        response = rq.get(url, headers=headers)
        return json.loads(response.text)
