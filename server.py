from flask import Flask, request, jsonify, make_response, abort
import sqlite3
from classes import ProductRepository, OffersServiceClient

app = Flask(__name__, static_url_path='')

offers_service = OffersServiceClient()

def create_repository():
    db_connect = sqlite3.connect('tables.sqlite')
    return ProductRepository(db_connect)

@app.route('/products/', methods=['GET'])
def get_products():
    return create_repository().read_all_products()

@app.route('/products/<int:product_id>/', methods=['GET'])
def get_product(product_id):
    return create_repository().read_product(product_id)
    
@app.route('/products/', methods=['POST'])
def create_product():
    id = request.json['id']
    name = request.json['name']
    description = request.json['description']    
    create_repository().create_product(id, name, description) 
    offers_service.product_register(id, name, description)   
    #offers = offers_service.products_offer(id)
    #for i in offers:
    #    create_repository().create_offer(i)
    return jsonify({'status':'created', 'status':'registered'})

@app.route('/products/<int:product_id>/', methods=['PUT'])
def update_product(product_id):
    id = product_id
    name = request.json['name']
    description = request.json['description']
    if name != '' and description != '':
        create_repository().update_product_name(name, id)
        create_repository().update_product_description(description, id)
        return jsonify({'name':'updated', 'description':'updated'})
    if name != '':
        create_repository().update_product_name(name, id)
        return jsonify({'name':'updated'})
    if description != '':
        create_repository().update_product_description(description, id)
        return jsonify({'description':'updated'})

@app.route('/products/<int:product_id>/', methods=['DELETE'])
def delete_product(product_id):
    create_repository().delete_product(product_id)
    return jsonify({'status':'deleted'})

@app.route('/offers/', methods=['GET'])
def get_offers():
    return create_repository().read_all_offers()

@app.route('/products/<int:offer_id>/', methods=['GET'])
def get_offer(offer_id):
    return create_repository().read_offer(offer_id)

if __name__ == '__main__':
     app.run()


