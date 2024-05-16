import unittest
from datetime import datetime
import mock
from scrapy.http import HtmlResponse, Request
from ecommerce_scraper.spiders.ssrecommercespider import SSREcommerceSpider
from ecommerce_scraper.items import Product


class SSREcommerceSpiderTest(unittest.TestCase):

    def setUp(self):
        self.spider = SSREcommerceSpider()
        self.start_time = datetime(2024, 5, 16, 12, 0, 0)
        self.spider.crawler = mock.Mock()
        self.spider.crawler.stats.get_value = mock.Mock(return_value=self.start_time)

    def test_parse_page_with_next_page(self):
        html_content = '''
        <div class="ProductItem_product-item-container" data-id="123">
            <div class="ProductItem_product-item-title">Product 1</div>
            <div class="ProductItem_product-item-price">$9.99</div>
            <div class="MuiRating-root" aria-label="4"></div>
            <img src="http://example.com/image1.jpg" />
        </div>
        <div class="ProductItem_product-item-container" data-id="456">
            <div class="ProductItem_product-item-title">Product 2</div>
            <div class="ProductItem_product-item-price">$19.99</div>
            <div class="MuiRating-root" aria-label="4"></div>
            <img src="http://example.com/image2.jpg" />
        </div>
        <a class="MuiPaginationItem-previousNext" aria-label="Go to next page" href="/products?page=2"></a>
        '''
        request = Request(url='https://ssr-scraping-website.whitecatdev.com/products')
        response = HtmlResponse(url=request.url, request=request, body=html_content, encoding='utf-8')
        results = list(self.spider.parse(response))

        self.assertEqual(len(results), 3)

        product1 = results[0]
        self.assertIsInstance(product1, Product)
        self.assertEqual(product1['website_id'], '123')
        self.assertEqual(product1['name'], 'Product 1')
        self.assertEqual(product1['price'], 9.99)
        self.assertEqual(product1['rating'], 4)
        self.assertEqual(product1['image_url'], 'http://example.com/image1.jpg')
        self.assertEqual(product1['website_url'], 'https://ssr-scraping-website.whitecatdev.com')
        self.assertEqual(product1['date'], self.start_time.isoformat())

        product2 = results[1]
        self.assertIsInstance(product2, Product)
        self.assertEqual(product2['website_id'], '456')
        self.assertEqual(product2['name'], 'Product 2')
        self.assertEqual(product2['price'], 19.99)
        self.assertEqual(product2['rating'], 4)
        self.assertEqual(product2['image_url'], 'http://example.com/image2.jpg')
        self.assertEqual(product2['website_url'], 'https://ssr-scraping-website.whitecatdev.com')
        self.assertEqual(product2['date'], self.start_time.isoformat())

        next_page_request = results[2]
        self.assertIsInstance(next_page_request, Request)
        self.assertEqual(next_page_request.url, 'https://ssr-scraping-website.whitecatdev.com/products?page=2')

    def test_parse_page_without_next_page(self):
        html_content = '''
        <div class="ProductItem_product-item-container" data-id="123">
            <div class="ProductItem_product-item-title">Product 1</div>
            <div class="ProductItem_product-item-price">$9.99</div>
            <div class="MuiRating-root" aria-label="4"></div>
            <img src="http://example.com/image1.jpg" />
        </div>
        <div class="ProductItem_product-item-container" data-id="456">
            <div class="ProductItem_product-item-title">Product 2</div>
            <div class="ProductItem_product-item-price">$19.99</div>
            <div class="MuiRating-root" aria-label="4"></div>
            <img src="http://example.com/image2.jpg" />
        </div>
        <a class="MuiPaginationItem-previousNext Mui-disabled" aria-label="Go to next page" href="/products?page=2"></a>
        '''
        request = Request(url='https://ssr-scraping-website.whitecatdev.com/products')
        response = HtmlResponse(url=request.url, request=request, body=html_content, encoding='utf-8')
        results = list(self.spider.parse(response))

        self.assertEqual(len(results), 2)

        product1 = results[0]
        self.assertIsInstance(product1, Product)
        self.assertEqual(product1['website_id'], '123')
        self.assertEqual(product1['name'], 'Product 1')
        self.assertEqual(product1['price'], 9.99)
        self.assertEqual(product1['rating'], 4)
        self.assertEqual(product1['image_url'], 'http://example.com/image1.jpg')
        self.assertEqual(product1['website_url'], 'https://ssr-scraping-website.whitecatdev.com')
        self.assertEqual(product1['date'], self.start_time.isoformat())

        product2 = results[1]
        self.assertIsInstance(product2, Product)
        self.assertEqual(product2['website_id'], '456')
        self.assertEqual(product2['name'], 'Product 2')
        self.assertEqual(product2['price'], 19.99)
        self.assertEqual(product2['rating'], 4)
        self.assertEqual(product2['image_url'], 'http://example.com/image2.jpg')
        self.assertEqual(product2['website_url'], 'https://ssr-scraping-website.whitecatdev.com')
        self.assertEqual(product2['date'], self.start_time.isoformat())
