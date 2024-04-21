import scrapy
from ..items import Product
from ..itemsloaders import SSREcommerceProductLoader

WEBSITE_BASE_URL = "https://ssr-scraping-website.whitecatdev.com"


class SSREcommerceSpider(scrapy.Spider):
    name = "ssrecommercespider"
    allowed_domains = ["localhost", "ssr-scraping-website.whitecatdev.com"]
    start_urls = [f"{WEBSITE_BASE_URL}/products"]

    def parse(self, response, **kwargs):
        start_time = self.crawler.stats.get_value('start_time')

        products = response.css('[class*="ProductItem_product-item-container"]')

        for product in products:
            prod = SSREcommerceProductLoader(item=Product(), selector=product)
            prod.add_value('website_id', product.attrib['data-id'])
            prod.add_value('website_url', WEBSITE_BASE_URL)
            prod.add_value('date', start_time.isoformat())
            prod.add_css('name', '[class*="ProductItem_product-item-title"]::text')
            prod.add_css('price', '[class*="ProductItem_product-item-price"]::text')
            prod.add_css('rating', '.MuiRating-root::attr(aria-label)')
            prod.add_css('image_url', 'img::attr(src)')
            yield prod.load_item()

        next_page = response.css('.MuiPaginationItem-previousNext:not(.Mui-disabled)[aria-label="Go to next '
                                 'page"]::attr(href)').get()
        if next_page is not None:
            next_page_url = WEBSITE_BASE_URL + next_page
            yield response.follow(next_page_url, callback=self.parse)

