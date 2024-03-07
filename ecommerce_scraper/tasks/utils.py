import os
from dotenv import load_dotenv
import requests
import sys
from repositories.productsrepository import ProductsRepository
from tasks.crawlrunner import CrawlRunner

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


def run_task(crawler):
    task_id = sys.argv[1]
    website = sys.argv[2]

    productsRepository = ProductsRepository()

    productsRepository.create_connection()

    productsRepository.delete_all()

    runner = CrawlRunner(crawler)
    runner.run_spider()

    scraped_products = productsRepository.get_products()

    update_results(task_id, website, scraped_products, runner.crawl_stats)

    productsRepository.close_connection()