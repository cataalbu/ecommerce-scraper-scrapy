from ecommerce_scraper.spiders.ssrecommercespider import SSREcommerceSpider
from utils import run_task


if __name__ == '__main__':
    run_task(SSREcommerceSpider)
