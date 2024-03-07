from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()


class SaveToMongoDBPipeline(object):
    def __init__(self):
        self._client = None
        self._db = None

    def open_spider(self, spider):
        self.create_connection()

    def close_spider(self, spider):
        self.close_connection()

    def process_item(self, item, spider):
        self.insert_product(item)

    def create_connection(self):
        self._client = MongoClient(os.getenv("MONGODB_URL"))
        self._db = self._client[os.getenv("MONGODB_DB_NAME")]

    def close_connection(self):
        self._client.close()

    def insert_product(self, item):
        collection = self._db["scrapedproducts"]
        collection.insert_one({
            "websiteId": item['website_id'],
            "name": item["name"],
            "price": item["price"],
            "imageUrl": item["imageUrl"],
            "rating": item["rating"]
        })
