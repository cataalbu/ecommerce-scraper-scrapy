from pymongo import MongoClient


class ProductsRepository:
    def __init__(self):
        self._client = None
        self._db = None

    def create_connection(self):
        self._client = MongoClient("mongodb://localhost:27017/")
        self._db = self._client["mock_ecommerce_db"]

    def close_connection(self):
        self._client.close()

    def get_products(self):
        collection = self._db["scrapy_scraped_products"]
        items = collection.find()
        return list(items)

    def delete_all(self):
        collection = self._db["scrapy_scraped_products"]
        collection.delete_many({})

