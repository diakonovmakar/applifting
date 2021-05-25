from flask import Flask, request, jsonify, make_response
from flask_httpauth import HTTPBasicAuth
from decouple import config
import sqlite3
from classes import ProductRepository, OffersServiceClient

app = Flask(__name__)
auth = HTTPBasicAuth()
username = config('USERNAME')
password = config('PASSWORD')


def create_repository():
    db_connect = sqlite3.connect('tables.sqlite')
    return ProductRepository(db_connect)


def validate_product(id, name='', description=''):
    if type(id) != int:
        return False
    elif type(description) != str:
        return False
    elif type(name) != str:
        return False
    else:
        return True


@auth.get_password
def get_password(usr):
    if usr == f'{usr}':
        return f'{password}'
    return None


@auth.error_handler
def unauthorized():
    return jsonify({'error': 'Unauthorized access'}), 401


@app.route('/products/', methods=['GET'])
@auth.login_required
def get_products():
    repository = create_repository()
    try:
        response = repository.read_all_products()
        repository.close_connection()
        return jsonify(response)
    except:
        repository.close_connection
        return jsonify('Error'), 404


@app.route('/products/<int:product_id>/', methods=['GET'])
@auth.login_required
def get_product(product_id: int):
    repository = create_repository()
    try:
        response = repository.read_product(product_id)
        product_ids = repository.read_all_product_ids()
        if product_id in product_ids:
            return jsonify(response)
        else:
            return jsonify(f"Product with id #{product_id} doesn't exsist."), 404
    except:
        repository.close_connection
        return jsonify('Error'), 404
    finally:
        repository.close_connection()


@app.route('/products/', methods=['POST'])
@auth.login_required
def create_product():
    repository = create_repository()
    offers_service = OffersServiceClient()
    id = request.json['id']
    name = request.json['name']
    description = request.json['description']
    try:
        if validate_product(id, name, description):
            repository.create_product(id, name, description)
            offers_service.register_product(id, name, description)
            offers = offers_service.product_offers(id)
            for i in offers:
                repository.create_offer(id, i)
            return jsonify({'product': f'id {id}'}), 201
        else:
            return jsonify({'Error': 'Invalid request'}), 400
    except sqlite3.IntegrityError:
        return jsonify('Product was registered before'), 409
    except:
        return jsonify('Error'), 404
    finally:
        repository.close_connection()


@app.route('/products/<int:product_id>/', methods=['PUT'])
@auth.login_required
def update_product(product_id: int):
    try:
        repository = create_repository()
        id = product_id
        name = request.json['name']
        description = request.json['description']
        validate_product(id, name, description)
        if name != '' and description != '':
            repository.update_product(name, description, id)
            return jsonify({'name': 'updated', 'description': 'updated'})
        if name != '':
            repository.update_product_name(name, id)
            return jsonify({'name': 'updated'})
        if description != '':
            repository.update_product_description(description, id)
            return jsonify({'description': 'updated'})
    except:
        return jsonify('Error'), 404
    finally:
        repository.close_connection()


@app.route('/products/<int:product_id>/', methods=['DELETE'])
@auth.login_required
def delete_product(product_id: int):
    repository = create_repository()
    try:
        repository.delete_product(product_id)
        repository.delete_offer(product_id)
        return jsonify({'status': 'deleted'}), 204
    except:
        return jsonify('Error'), 404
    finally:
        repository.close_connection()


@app.route('/offers/', methods=['GET'])
@auth.login_required
def get_offers():
    repository = create_repository()
    try:
        response = repository.read_all_offers()
        return jsonify(response)
    except:
        return jsonify('Error'), 404
    finally:
        repository.close_connection()


@app.route('/offers/<int:product_id>/', methods=['GET'])
@auth.login_required
def get_offer(product_id: int):
    repository = create_repository()
    try:
        response = repository.read_offer(product_id)
        product_ids = repository.read_all_product_ids()
        if product_id in product_ids:
            return jsonify(response)
        else:
            return jsonify(f"Product with id #{product_id} doesn't exsist."), 404
    except:
        return jsonify('Error'), 404
    finally:
        repository.close_connection()


if __name__ == '__main__':
    app.run()
