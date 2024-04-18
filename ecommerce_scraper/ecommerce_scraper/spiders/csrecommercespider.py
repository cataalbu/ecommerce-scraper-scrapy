import scrapy
from scrapy_playwright.page import PageMethod
from ..items import Product
from ..itemsloaders import CSREcommerceProductLoader

WEBSITE_BASE_URL = "http://localhost:5173"


class CSREcommerceSpider(scrapy.Spider):
    name = "csrecommercespider"
    custom_settings = {
        'DOWNLOAD_HANDLERS': {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        }
    }

    def start_requests(self):
        yield scrapy.Request(f'{WEBSITE_BASE_URL}/', meta={
            'playwright': True,
            'playwright_page_methods': [
                PageMethod('wait_for_selector', 'div[class*="_product-item-container"]')
            ],
            'playwright_include_page': True
        })

    async def parse(self, response, **kwargs):
        page = response.meta['playwright_page']
        start_time = self.crawler.stats.get_value('start_time')

        while True:
            products = response.css('[class*="_product-item-container"]')
            for product in products:
                prod = CSREcommerceProductLoader(item=Product(), selector=product)
                prod.add_value('website_id', product.attrib['data-id'])
                prod.add_value('website_url', WEBSITE_BASE_URL)
                prod.add_value('date', '')
                prod.add_css('name', '[class*="_product-item-title"]::text')
                prod.add_css('price', '[class*="_product-item-price"]::text')
                prod.add_css('rating', '.MuiRating-root::attr(aria-label)')
                prod.add_css('imageUrl', 'img::attr(src)')
                yield prod.load_item()

            next_page_button_selector = '.MuiPaginationItem-previousNext:not(.Mui-disabled)[aria-label="Go to next page"]'
            next_page_exists = await page.query_selector(next_page_button_selector)
            if not next_page_exists:
                await page.close()
                break
            await next_page_exists.click()
            await page.wait_for_selector('p[class*="_product-item-title"]')
            html_content = await page.content()
            response = response.replace(body=html_content.encode('utf-8'))

        await page.close()
