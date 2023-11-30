from datetime import datetime
from pymongo import MongoClient


class SaveToMongoDBPipeline(object):
    def __init__(self):
        self._client = None
        self._db = None
        self.create_connection()

    def __del__(self):
        self.close_connection()

    def process_item(self, item, spider):
        self.insert_product(item)

    def create_connection(self):
        self._client = MongoClient("mongodb://localhost:27017/")
        self._db = self._client["mock_ecommerce_db"]

    def close_connection(self):
        self._client.close()

    def update_product_price(self, product_id, item):
        collection = self._db["scrapy_scraped_products"]
        collection.update_one({
            "_id": product_id
        }, {
            "websiteId": item['website_id'],
            "name": item["name"],
            "price": item["price"],
            "imageUrl": item["imageUrl"],
            "rating": item["rating"]

        })

    def insert_product(self, item):
        collection = self._db["scrapy_scraped_products"]
        collection.insert_one({
            "websiteId": item['website_id'],
            "name": item["name"],
            "price": [{
                "value": item["price"],
                "date": datetime.now()
            }],
            "imageUrl": item["imageUrl"],
            "rating": item["rating"]
        })
