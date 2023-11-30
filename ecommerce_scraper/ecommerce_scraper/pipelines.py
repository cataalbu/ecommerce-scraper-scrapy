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
        # collection = self._db["scrapy_scraped_products"]
        # result = collection.find_one({"websiteId": item["website_id"]})
        # if result is None:
        #     self.insert_product(item)
        # else:
        #     if result["price"][-1]["value"] != item["price"]:
        #         price = result["price"]
        #         price.append({
        #             "value": item["price"],
        #             "date": datetime.now()
        #         })
        #         item["price"] = price
        #         self.update_product(result["_id"], item)

    def create_connection(self):
        self._client = MongoClient("mongodb://localhost:27017/")
        self._db = self._client["mock_ecommerce_db"]

    def close_connection(self):
        self._client.close()

    def update_product(self, product_id, item):
        collection = self._db["scrapy_scraped_products"]
        updated_fields = {}
        if item['website_id']:
            updated_fields['websiteId'] = item['website_id']
        if item['name']:
            updated_fields['name'] = item['name']
        if item['price']:
            updated_fields['price'] = item['price']
        if item['imageUrl']:
            updated_fields['imageUrl'] = item['imageUrl']
        if item['rating']:
            updated_fields['rating'] = item['rating']

        collection.update_one({
            "_id": product_id
        }, {"$set": updated_fields})

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
