import sqlite3
from classes import OffersServiceClient, ProductRepository

db_connect = sqlite3.connect('tables.sqlite')

repository = ProductRepository(db_connect)
offer_service = OffersServiceClient()

products = repository.read_all_product_ids()
offers = repository.read_all_offer_ids()
offer_ids = set()
product_ids = []
for id in offers:
    offer_ids.add(id[0])
for id in products:
    product_ids.append(id[0])

for id in product_ids:
    product_id = id
    new_offers = offer_service.product_offers(product_id)
    for offer in new_offers:
        if offer['id'] in offer_ids:
            repository.update_offer(product_id, offer)
        else:
            repository.create_offer(product_id, offer)

db_connect.close()
