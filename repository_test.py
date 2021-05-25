import sqlite3
from classes import ProductRepository

db_connect = sqlite3.connect('tables_for_tests.sqlite')
repository = ProductRepository(db_connect)


def test_create_product():
    id = 1
    name = 'name'
    description = 'description'
    repository.create_product(id, name, description)
    cursor = db_connect.cursor()
    cursor.execute("""
        SELECT *
        FROM products
        WHERE id=:id;
        """, {'id': id})
    test_result = cursor.fetchall()
    assert test_result == [(id, name, description)]

def test_read_product():
    id = 1
    query = repository.read_product(id)
    cursor = db_connect.cursor()
    cursor.execute("""
        SELECT *
        FROM products
        WHERE id=:id;
        """, {'id': id})
    test_result = cursor.fetchall()
    assert test_result == query

def test_read_all_products():
    query = repository.read_all_products()
    cursor = db_connect.cursor()
    cursor.execute("""
        SELECT *
        FROM products;
        """)
    result = cursor.fetchall()
    test_result = [{'id': '', 
                'name': '', 
                'description': ''}]
    for i in range(len(result)):
        test_result[i]['id'] = result[i][0]
        test_result[i]['name'] = result[i][1]
        test_result[i]['description'] = result[i][2]
    assert test_result == query

def test_read_all_product_ids():
    query = repository.read_all_product_ids()
    cursor = db_connect.cursor()
    cursor.execute("""
        SELECT id
        FROM products;
        """)
    test_result = cursor.fetchall()
    assert test_result == query

def test_update_product():
    id = 1
    new_name = 'New name'
    new_desc = 'New description'
    repository.update_product(new_name, new_desc, id)
    cursor = db_connect.cursor()
    cursor.execute("""
        SELECT *
        FROM products
        WHERE id=:id;
        """, {'id': id})
    test_result = cursor.fetchall()
    assert test_result == [(id, new_name, new_desc)]

def test_update_product_description():
    id = 1
    new_desc = 'New new description'
    repository.update_product_description(new_desc, id)
    cursor = db_connect.cursor()
    cursor.execute("""
        SELECT id, description
        FROM products
        WHERE id=:id;
        """, {'id': id})
    test_result = cursor.fetchall()
    assert test_result == [(id, new_desc)]

def test_update_product_name():
    id = 1
    new_name = 'New new name'
    repository.update_product_name(new_name, id)
    cursor = db_connect.cursor()
    cursor.execute("""
        SELECT id, name
        FROM products
        WHERE id=:id;
        """, {'id': id})
    test_result = cursor.fetchall()
    assert test_result == [(id, new_name)]

def test_delete_product():
    id = 1
    repository.delete_product(id)
    cursor = db_connect.cursor()
    cursor.execute("""
        SELECT *
        FROM products
        WHERE id=:id;
        """, {'id': id})
    test_result = cursor.fetchall()
    assert test_result == []

def test_create_offer():
    product_id = 1
    offer = {
        'id': 1,
        'price': 100,
        'items_in_stock': 150
    }
    repository.create_offer(product_id, offer)
    cursor = db_connect.cursor()
    cursor.execute("""
        SELECT *
        FROM offers
        WHERE id=:id;
        """, {'id': 1})
    test_result = cursor.fetchall()
    assert test_result == [(product_id, 1, 100, 150)]

def test_read_offer_by_product_id():
    product_id = 1
    query = repository.read_offer(product_id)
    cursor = db_connect.cursor()
    cursor.execute("""
        SELECT *
        FROM offers
        WHERE product_id=:product_id;
        """, {'product_id': product_id})
    result = cursor.fetchall()
    test_result = [{'product_id': product_id, 
                'offer_id': '', 
                'price': '', 
                'items_in_stock': ''}]
    for i in range(len(result)):
        test_result[i]['product_id'] = result[i][0]
        test_result[i]['offer_id'] = result[i][1]
        test_result[i]['price'] = result[i][2]
        test_result[i]['items_in_stock'] = result[i][3]
    assert test_result == query

def test_update_offer():
    product_id = 1
    new_offer = {
        'id': 1,
        'price': 200,
        'items_in_stock': 50
    }
    repository.update_offer(product_id, new_offer)
    cursor = db_connect.cursor()
    cursor.execute("""
        SELECT *
        FROM offers
        WHERE id=:id;
        """, {'id': new_offer['id']})
    test_result = cursor.fetchall()
    assert test_result == [(product_id, new_offer['id'], new_offer['price'], new_offer['items_in_stock'])]

def test_delete_offer():
    product_id = 1
    repository.delete_offer(product_id)
    cursor = db_connect.cursor()
    cursor.execute("""
        SELECT *
        FROM offers
        WHERE product_id=:product_id;
        """, {'product_id': product_id})
    test_result = cursor.fetchall()
    assert test_result == []
