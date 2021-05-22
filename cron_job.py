import requests as rq

import json
import sqlite3

import config

token = config.token
db_connect = sqlite3.connect('tables.sqlite')

def read_all_products():
    cursor = db_connect.cursor()
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

def read_all_offers():
    cursor = db_connect.cursor()
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
                  

def products_offer(id):
    headers = {'Bearer': config.token}
    url = f'{config.url}{config.url_params["products"]}{id}/{config.url_params["offers"]}'
    response = rq.get(url, headers=headers)
    return json.loads(response.text)


def update_offer(product_id, dict_of_data):
    data = {'product_id': product_id,
            'id': dict_of_data['id'],
            'price': dict_of_data['price'],
            'items_in_stock': dict_of_data['items_in_stock']}
    db_connect.execute("""
                    UPDATE offers
                    SET price=:price, items_in_stock=:items_in_stock
                    WHERE id=:id AND product_id=:product_id;
                    """, data)
    db_connect.commit()
    id = data['id']
    print(f'Offer with id #{id} was updated!')


def create_offer(product_id, dict_of_data):
    data = {'product_id': product_id,
            'id': dict_of_data['id'],
            'price': dict_of_data['price'],
            'items_in_stock': dict_of_data['items_in_stock']}
    db_connect.execute("""
                    INSERT INTO
                    offers(product_id, id, price, items_in_stock)
                    VALUES
                    (:product_id, :id, :price, :items_in_stock);
                    """, data)
    db_connect.commit()
    id = data['id']
    print(f'Offer with id #{id} was created!')

products = read_all_products()
offers = read_all_offers()

offers_id = []
for i in range(len(offers)):
    offers_id.append(offers[i]['offer_id'])
set_of_offers_id = set(offers_id)

for i in range(len(products)):
    product_id = products[i]['id']
    new_offers = products_offer(product_id)
    for offer in new_offers:
        dict_of_data = offer
        if dict_of_data['id'] in set_of_offers_id:
            update_offer(product_id, dict_of_data)
        else:
            create_offer(product_id, dict_of_data)

db_connect.close()