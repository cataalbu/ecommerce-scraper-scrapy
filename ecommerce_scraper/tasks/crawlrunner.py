from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os


class CrawlRunner:
    def __init__(self, crawler):
        self.crawl_stats = {}
        self._crawler = crawler

    def run_spider(self):
        os.environ['SCRAPY_SETTINGS_MODULE'] = 'ecommerce_scraper.settings'
        settings = get_project_settings()

        process = CrawlerProcess(settings)

        crawler = process.create_crawler(self._crawler)

        process.crawl(crawler)
        process.start()
        self.crawl_stats = crawler.stats.get_stats()
