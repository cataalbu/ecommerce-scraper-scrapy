from ecommerce_scraper.spiders.csrecommercespider import CSREcommerceSpider
from utils import run_task

if __name__ == '__main__':
    run_task(CSREcommerceSpider)
