from aws_sqs_consumer import Consumer, Message
from dotenv import load_dotenv
import os
import json

from ecommerce_scraper.spiders.csrecommercespider import CSREcommerceSpider
from tasks.crawlrunner import CrawlRunner
from ecommerce_scraper.spiders.ssrecommercespider import SSREcommerceSpider

load_dotenv()


class FinishedTaskProducer():
   pass


# class TaskConsumer(Consumer):
#     def handle_message(self, message: Message):
#         data = json.loads(message.Body)
#         print(data)
#         if data['type'] == "csr":
#             print("Starting CSR")
#             csr_runner = CrawlRunner(CSREcommerceSpider)
#             csr_runner.run_spider()
#         elif data['type'] == "ssr":
#             print("Starting CSR")
#             ssr_runner = CrawlRunner(SSREcommerceSpider)
#             ssr_runner.run_spider()
#
#
# consumer = TaskConsumer(
#    queue_url= os.getenv("SCRAPY_TASKS_QUEUE_URL"),
#    polling_wait_time_ms=30000
# )
# consumer.start()


ssr_runner = CrawlRunner(CSREcommerceSpider)
ssr_runner.run_spider()