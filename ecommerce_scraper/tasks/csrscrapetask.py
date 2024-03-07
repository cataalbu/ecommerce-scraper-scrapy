from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from ecommerce_scraper.spiders.csrecommercespider import CSREcommerceSpider
from dotenv import load_dotenv
import os
import sys
import requests
from productsrepository import ProductsRepository

load_dotenv()


def update_results(f_task_id, f_website, f_scraped_products, crawl_stats):
    for product in f_scraped_products:
        product['_id'] = str(product['_id'])
        product["price"] = {"price": product["price"], "date": crawl_stats["start_time"].isoformat()}
        product["website"] = f_website

    data = {
        "id": f_task_id,
        "scrapedProducts": f_scraped_products,
        "startTime": crawl_stats["start_time"].isoformat(),
        "endTime": crawl_stats["finish_time"].isoformat(),
        "scrapeCount": crawl_stats["item_scraped_count"]
    }

    print(os.getenv("SCRAPE_SENSE_API_URL"))

    response = requests.patch(os.getenv("SCRAPE_SENSE_API_URL") + '/scrape-tasks/results', json=data, headers={
        'Content-Type': 'application/json',
        'x-api-key': os.getenv("SCRAPE_SENSE_API_KEY"),
    })

    print(f"Status Code: {response.status_code}")
    print(response.text)


class CrawlRunner:
    def __init__(self):
        self.crawl_stats = {}

    def run_spider(self):
        os.environ['SCRAPY_SETTINGS_MODULE'] = 'ecommerce_scraper.settings'
        settings = get_project_settings()

        process = CrawlerProcess(settings)

        crawler = process.create_crawler(CSREcommerceSpider)

        process.crawl(crawler)
        process.start()
        self.crawl_stats = crawler.stats.get_stats()


if __name__ == '__main__':
    task_id = sys.argv[1]
    website = sys.argv[2]

    productsRepository = ProductsRepository()

    productsRepository.create_connection()

    productsRepository.delete_all()

    runner = CrawlRunner()
    runner.run_spider()

    scraped_products = productsRepository.get_products()

    update_results(task_id, website, scraped_products, runner.crawl_stats)

    productsRepository.close_connection()
