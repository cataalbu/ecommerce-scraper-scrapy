from task_consumer import TaskConsumer
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    consumer = TaskConsumer(
        queue_url=os.getenv("SCRAPY_TASKS_QUEUE_URL"),
        polling_wait_time_ms=os.getenv("POLLING_WAIT_TIME_MS")
    )
    consumer.start()
