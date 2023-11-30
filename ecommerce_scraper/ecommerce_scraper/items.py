import scrapy


class ShopifyProduct(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    imageUrl = scrapy.Field()
    rating = scrapy.Field()