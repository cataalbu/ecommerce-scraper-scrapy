import scrapy


class Product(scrapy.Item):
    website_id = scrapy.Field()
    website_url = scrapy.Field()
    date = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    image_url = scrapy.Field()
    rating = scrapy.Field()
