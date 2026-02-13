
from taskiq import TaskiqEvents, TaskiqState
from taskiq_aio_pika import AioPikaBroker
import taskiq_fastapi
from backlog_app.config import settings
import logging

logger = logging.getLogger(__name__)

broker = AioPikaBroker(url=settings.taskiq.url)

taskiq_fastapi.init(broker, "backlog_app.main:app")

@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def on_worker_startup(state: TaskiqState) -> None:
    logging.basicConfig(
        format=settings.logging.worker_log_format,
        level=settings.logging.log_level,
        datefmt=settings.logging.log_date_format,
    )

    logger.info("Worker startup complete, got state: %s", state)
