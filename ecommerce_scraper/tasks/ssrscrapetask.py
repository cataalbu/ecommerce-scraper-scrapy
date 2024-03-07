from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from ecommerce_scraper.spiders.ssrecommercespider import SSREcommerceSpider
import os

import sys

class CrawlRunner:
    def __init__(self):
        self.crawl_stats = {}

    def run_spider(self):
        os.environ['SCRAPY_SETTINGS_MODULE'] = 'ecommerce_scraper.settings'
        settings = get_project_settings()

        process = CrawlerProcess(settings)

        crawler = process.create_crawler(SSREcommerceSpider)

        process.crawl(crawler)
        process.start()
        self.crawl_stats = crawler.stats.get_stats()


if __name__ == '__main__':
    runner = CrawlRunner()
    runner.run_spider()
    print(runner.crawl_stats)
