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

for product_id in product_ids:
    new_offers = offer_service.product_offers(product_id)
    new_offer_ids = set()
    for i in range(len(new_offers)):
        new_offer_ids.add(new_offers[i]['id'])
    for offer_id in offer_ids:
        if offer_id not in new_offer_ids:
            repository.delete_offer_by_id(offer_id)
    for offer in new_offers:
        if offer['id'] in offer_ids:
            repository.update_offer(product_id, offer)
        elif offer['id'] not in offer_ids:
            repository.create_offer(product_id, offer)

db_connect.close()
