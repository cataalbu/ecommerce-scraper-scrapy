from aws_sqs_consumer import Consumer, Message
from dotenv import load_dotenv
import os
import json
from multiprocessing import Process, Queue

from ecommerce_scraper.spiders.csrecommercespider import CSREcommerceSpider
from tasks.crawlrunner import CrawlRunner
from ecommerce_scraper.spiders.ssrecommercespider import SSREcommerceSpider

load_dotenv()

class FinishedTaskProducer():
    pass


class TaskConsumer(Consumer):

    def __init__(self, queue_url, polling_wait_time_ms):
        super().__init__(queue_url=queue_url, polling_wait_time_ms=polling_wait_time_ms)
        self.stats = {}

    @staticmethod
    def run_spider(runner, queue):
        result = runner.run_spider()
        queue.put(result)

    def run_spider_process(self, runner):
        queue = Queue()
        p = Process(target=self.run_spider, args=(runner, queue))
        p.start()
        p.join()
        result = queue.get()
        print("ITEMS SCRP CONT", result)

    def handle_message(self, message: Message):
        data = json.loads(message.Body)
        print(data)
        if data['type'] == "csr":
            self.run_spider_process(CrawlRunner(CSREcommerceSpider))

        elif data['type'] == "ssr":
            self.run_spider_process(CrawlRunner(SSREcommerceSpider))


if __name__ == "__main__":
    consumer = TaskConsumer(
        queue_url=os.getenv("SCRAPY_TASKS_QUEUE_URL"),
        polling_wait_time_ms=1000
    )
    consumer.start()
