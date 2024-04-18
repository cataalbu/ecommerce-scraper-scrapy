from aws_sqs_consumer import Consumer, Message
import os
import json
from multiprocessing import Process, Queue

from ecommerce_scraper.spiders.csrecommercespider import CSREcommerceSpider
from tasks.crawlrunner import CrawlRunner
from ecommerce_scraper.spiders.ssrecommercespider import SSREcommerceSpider
from task_producer import TaskProducer


class TaskConsumer(Consumer):

    def __init__(self, queue_url, polling_wait_time_ms):
        super().__init__(queue_url=queue_url, polling_wait_time_ms=polling_wait_time_ms)

    @staticmethod
    def run_spider(runner, task_data, queue=None):
        try:
            task_producer = TaskProducer(os.getenv("NEST_TASKS_QUEUE_URL"))
            result = runner.run_spider()
            task_producer.publish_finished_task(task_data, result)
            if queue:
                queue.put(result)

        except Exception as e:
            task_producer.publish_crashed_task(task_data)

    def run_spider_process(self, runner, task_data):
        queue = Queue()
        p = Process(target=self.run_spider, args=(runner, task_data,))
        p.start()

    def handle_message(self, message: Message):
        data = json.loads(message.Body)
        if data['type'] == "csr":
            self.run_spider_process(CrawlRunner(CSREcommerceSpider), data)

        elif data['type'] == "ssr":
            self.run_spider_process(CrawlRunner(SSREcommerceSpider), data)
