import scrapy
from ..items import Product
from ..itemsloaders import SSREcommerceProductLoader


class SSREcommerceSpider(scrapy.Spider):
    name = "ssrecommercespider"
    allowed_domains = ["localhost"]
    start_urls = ["http://localhost:3001/products"]

    def parse(self, response, **kwargs):
        products = response.css('[class*="ProductItem_product-item-container"]')

        product_item = Product()
        for product in products:
            prod = SSREcommerceProductLoader(item=Product(), selector=product)
            prod.add_value('website_id', product.attrib['data-id'])
            prod.add_css('name', '[class*="ProductItem_product-item-title"]::text')
            prod.add_css('price', '[class*="ProductItem_product-item-price"]::text')
            prod.add_css('rating', '.MuiRating-root::attr(aria-label)')
            prod.add_css('imageUrl', 'img::attr(src)')
            yield prod.load_item()

        next_page = response.css('.MuiPaginationItem-previousNext:not(.Mui-disabled)[aria-label="Go to next page"]::attr(href)').get()
        if next_page is not None:
            next_page_url = 'http://localhost:3001' + next_page
            yield response.follow(next_page_url, callback=self.parse)

    def close(self, spider, reason):
        pass

