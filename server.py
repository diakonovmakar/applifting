from flask import Flask, jsonify, abort, request, make_response
from sqlalchemy import create_engine
from json import dumps

app = Flask(__name__)
data = [
    {
        'id': 1,
        'name': 'Dosquarna',
        'description': 'The best gas station'
    },
    {
        'id': 2,
        'title': 'Lukoil',
        'description': 'The biggest gas company in Russia'
    }
]

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify({'products': data})

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    if product_id == 1:
        return 'qwerty'
    abort(404)

@app.route('/products', methods=['POST'])
def create_product():
    if not request.json or not 'name' in request.json:
        abort(400)
    product = {
        'id': data[-1]['id'] + 1,
        'name': request.json['name'],
        'description': request.json.get('description', "")
    }
    data.append(product)
    return jsonify({'product': product}), 201

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    if product_id == 1:
        return jsonify(product_id)
    abort(404)

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    if product_id == 1:
        return make_response(jsonify({'result': True}), 204)
    abort(404)

if __name__ == '__main__':
    app.run(debug=False)