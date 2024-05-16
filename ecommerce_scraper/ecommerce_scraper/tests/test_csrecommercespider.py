import sys
import os
import pytest
from datetime import datetime
from unittest import mock
from scrapy.http import HtmlResponse, Request
from scrapy.utils.test import get_crawler
from ecommerce_scraper.spiders.csrecommercespider import CSREcommerceSpider
from ecommerce_scraper.items import Product

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class MockElement:
    async def click(self):
        pass


class MockPage:
    def __init__(self, has_next_page=True):
        self.has_next_page = has_next_page
        self.next_page_clicked = False

    async def query_selector(self, selector):
        if selector == '.MuiPaginationItem-previousNext:not(.Mui-disabled)[aria-label="Go to next page"]':
            if self.has_next_page and not self.next_page_clicked:
                self.next_page_clicked = True
                return MockElement()
        return None

    async def wait_for_selector(self, selector):
        pass

    async def content(self):
        if self.next_page_clicked:
            return '''
            <div class="_product-item-container" data-id="789">
                <div class="_product-item-title">Product 3</div>
                <div class="_product-item-price">$29.99</div>
                <div class="MuiRating-root" aria-label="5"></div>
                <img src="http://example.com/image3.jpg" />
            </div>
            '''

    async def close(self):
        pass


@pytest.mark.asyncio
async def test_start_requests(spider):
    start_requests = list(spider.start_requests())
    assert len(start_requests) == 1
    request = start_requests[0]
    assert isinstance(request, Request)
    assert request.url == 'https://csr-scraping-website.whitecatdev.com/'
    assert request.meta['playwright'] is True
    assert request.meta['playwright_page_methods'][0].method == 'wait_for_selector'
    assert request.meta['playwright_page_methods'][0].args == ('div[class*="_product-item-container"]',)
    assert request.meta['playwright_include_page'] is True

@pytest.fixture
def crawler():
    return get_crawler(CSREcommerceSpider, {
        'DOWNLOAD_HANDLERS': {
            'http': 'scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler',
            'https': 'scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler',
        },
        'PLAYWRIGHT_BROWSER_TYPE': 'chromium',
    })


@pytest.fixture
def spider(crawler):
    spider = CSREcommerceSpider.from_crawler(crawler)
    start_time = datetime(2024, 5, 16, 12, 0, 0)
    spider.crawler.stats = mock.Mock()
    spider.crawler.stats.get_value = mock.Mock(return_value=start_time)
    return spider


@pytest.mark.asyncio
async def test_parse_page_with_next_page(spider):
    html_content = '''
    <div class="_product-item-container" data-id="123">
        <div class="_product-item-title">Product 1</div>
        <div class="_product-item-price">$9.99</div>
        <div class="MuiRating-root" aria-label="4"></div>
        <img src="http://example.com/image1.jpg" />
    </div>
    <div class="_product-item-container" data-id="456">
        <div class="_product-item-title">Product 2</div>
        <div class="_product-item-price">$19.99</div>
        <div class="MuiRating-root" aria-label="4"></div>
        <img src="http://example.com/image2.jpg" />
    </div>
    '''
    request = Request(url='https://csr-scraping-website.whitecatdev.com/')
    response = HtmlResponse(url=request.url, request=request, body=html_content, encoding='utf-8')
    response.meta['playwright_page'] = MockPage()

    results = [item async for item in spider.parse(response)]

    assert len(results) == 3
    product1 = results[0]
    assert isinstance(product1, Product)
    assert product1['website_id'] == '123'
    assert product1['name'] == 'Product 1'
    assert product1['price'] == 9.99
    assert product1['rating'] == 4
    assert product1['image_url'] == 'http://example.com/image1.jpg'
    assert product1['website_url'] == 'https://csr-scraping-website.whitecatdev.com'
    assert product1['date'] == spider.crawler.stats.get_value('start_time').isoformat()

    product2 = results[1]
    assert isinstance(product2, Product)
    assert product2['website_id'] == '456'
    assert product2['name'] == 'Product 2'
    assert product2['price'] == 19.99
    assert product2['rating'] == 4
    assert product2['image_url'] == 'http://example.com/image2.jpg'
    assert product2['website_url'] == 'https://csr-scraping-website.whitecatdev.com'
    assert product2['date'] == spider.crawler.stats.get_value('start_time').isoformat()

    product2 = results[2]
    assert isinstance(product2, Product)
    assert product2['website_id'] == '789'
    assert product2['name'] == 'Product 3'
    assert product2['price'] == 29.99
    assert product2['rating'] == 5
    assert product2['image_url'] == 'http://example.com/image3.jpg'
    assert product2['website_url'] == 'https://csr-scraping-website.whitecatdev.com'
    assert product2['date'] == spider.crawler.stats.get_value('start_time').isoformat()


@pytest.mark.asyncio
async def test_parse_page_without_next_page(spider):
    html_content = '''
    <div class="_product-item-container" data-id="123">
        <div class="_product-item-title">Product 1</div>
        <div class="_product-item-price">$9.99</div>
        <div class="MuiRating-root" aria-label="4"></div>
        <img src="http://example.com/image1.jpg" />
    </div>
    <div class="_product-item-container" data-id="456">
        <div class="_product-item-title">Product 2</div>
        <div class="_product-item-price">$19.99</div>
        <div class="MuiRating-root" aria-label="4"></div>
        <img src="http://example.com/image2.jpg" />
    </div>
    <a class="MuiPaginationItem-previousNext" aria-label="Go to next page" href="/products?page=2"></a>
    '''
    request = Request(url='https://csr-scraping-website.whitecatdev.com/')
    response = HtmlResponse(url=request.url, request=request, body=html_content, encoding='utf-8')
    response.meta['playwright_page'] = MockPage(has_next_page=False)

    results = [item async for item in spider.parse(response)]

    assert len(results) == 2
    product1 = results[0]
    assert isinstance(product1, Product)
    assert product1['website_id'] == '123'
    assert product1['name'] == 'Product 1'
    assert product1['price'] == 9.99
    assert product1['rating'] == 4
    assert product1['image_url'] == 'http://example.com/image1.jpg'
    assert product1['website_url'] == 'https://csr-scraping-website.whitecatdev.com'
    assert product1['date'] == spider.crawler.stats.get_value('start_time').isoformat()

    product2 = results[1]
    assert isinstance(product2, Product)
    assert product2['website_id'] == '456'
    assert product2['name'] == 'Product 2'
    assert product2['price'] == 19.99
    assert product2['rating'] == 4
    assert product2['image_url'] == 'http://example.com/image2.jpg'
    assert product2['website_url'] == 'https://csr-scraping-website.whitecatdev.com'
    assert product2['date'] == spider.crawler.stats.get_value('start_time').isoformat()
