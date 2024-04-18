import json
from boto3 import client


class TaskProducer:

    def __init__(self, queue_url):
        self._sqs_client = client('sqs')
        self._queue_url = queue_url

    def send_message(self, message):
        return self._sqs_client.send_message(
            QueueUrl=self._queue_url,
            MessageBody=message
        )

    def publish_crashed_task(self, task_data):
        data = {
            'id': task_data['id'],
            'website': task_data['website'],
            "status": "crashed"
        }
        return self.send_message(json.dumps(data))

    def publish_finished_task(self, task_data, scrapy_stats):
        data = {
            'id': task_data['id'],
            'website': task_data['website'],
            'startTime': scrapy_stats["start_time"].isoformat(),
            "endTime": scrapy_stats["finish_time"].isoformat(),
            "scrapeCount": scrapy_stats["item_scraped_count"],
            "status": "finished"
        }
        return self.send_message(json.dumps(data))
