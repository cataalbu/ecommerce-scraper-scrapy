import scrapy


class Product(scrapy.Item):
    website_id = scrapy.Field()
    website_url = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    imageUrl = scrapy.Field()
    rating = scrapy.Field()
