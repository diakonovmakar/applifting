import sqlite3
from classes import OffersServiceClient, ProductRepository

db_connect = sqlite3.connect('tables.sqlite')

repository = ProductRepository(db_connect)
offer_service = OffersServiceClient()

products = repository.read_all_products()
offers = repository.read_all_offers()

offers_id = []
for i in range(len(offers)):
    offers_id.append(offers[i]['offer_id'])
set_of_offers_id = set(offers_id)

for i in range(len(products)):
    product_id = products[i]['id']
    new_offers = offer_service.products_offer(product_id)
    for offer in new_offers:
        dict_of_data = offer
        if dict_of_data['id'] in set_of_offers_id:
            repository.update_offer(product_id, dict_of_data)
        else:
            repository.create_offer(product_id, dict_of_data)

db_connect.close()