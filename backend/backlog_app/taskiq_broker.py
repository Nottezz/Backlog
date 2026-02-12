from taskiq_aio_pika import AioPikaBroker
from backlog_app.config import settings

broker = AioPikaBroker(url=settings.taskiq.url)
