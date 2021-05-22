from flask import Flask, request, jsonify
import sqlite3

from classes import ProductRepository, OffersServiceClient

app = Flask(__name__, static_url_path='')

def create_repository():
    db_connect = sqlite3.connect('tables.sqlite')
    return ProductRepository(db_connect)

def validate_product(id, name='', description=''):
    if type(id) != int:  
        return False
    elif type(description) != str:    
        return False
    elif  type(name) != str:      
        return False
    else:
        return True
    
@app.route('/products/', methods=['GET'])
def get_products():
    repository = create_repository()
    response = repository.read_all_products()
    repository.close_connection()
    return response
    
@app.route('/products/<int:product_id>/', methods=['GET'])
def get_product(product_id):
    repository = create_repository()
    response = repository.read_product(product_id)
    repository.close_connection()
    return response
    
@app.route('/products/', methods=['POST'])
def create_product():
    repository = create_repository()
    offers_service = OffersServiceClient()
    id = request.json['id']
    name = request.json['name']
    description = request.json['description']
    try:
        if validate_product(id, name, description) == True:
            repository.create_product(id, name, description) 
            offers_service.product_register(id, name, description)   
            offers = offers_service.products_offer(id)
            for i in offers:
                repository.create_offer(id, i)
            repository.close_connection()
            return jsonify({'product': f'id {id}'})
        else:
            return jsonify({'Error': 'Invalid request'}), 401
    except sqlite3.IntegrityError:
        repository.close_connection()
        return jsonify('Product was registered before')
    except:
        repository.close_connection()
        return jsonify('Error')

@app.route('/products/<int:product_id>/', methods=['PUT'])
def update_product(product_id):
    repository = create_repository()
    id = product_id
    name = request.json['name']
    description = request.json['description']
    validate_product(id, name, description)
    if name != '' and description != '':
        repository.update_product(name, description, id)
        repository.close_connection()
        return jsonify({'name':'updated', 'description':'updated'})
    if name != '':
        repository.update_product_name(name, id)
        repository.close_connection()
        return jsonify({'name':'updated'})
    if description != '':
        repository.update_product_description(description, id)
        repository.close_connection()
        return jsonify({'description':'updated'})

@app.route('/products/<int:product_id>/', methods=['DELETE'])
def delete_product(product_id):
    repository = create_repository()
    repository.delete_product(product_id)
    repository.close_connection()
    return jsonify({'status':'deleted'})

@app.route('/offers/', methods=['GET'])
def get_offers():
    repository = create_repository()
    response = repository.read_all_offers()
    repository.close_connection()
    return response

@app.route('/offers/<int:product_id>/', methods=['GET'])
def get_offer(product_id):
    repository = create_repository()
    response = repository.read_offer(product_id)
    repository.close_connection()
    return response

if __name__ == '__main__':
     app.run()


