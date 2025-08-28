import logging.config

from celery import Celery
from celery.schedules import crontab
from celery.signals import setup_logging

from app.config.log import LOGGING_CONFIG
from app.config.settings import get_settings

settings = get_settings()

app = Celery(
    "fitpetScraper",
    broker=settings.celery.broker,
    backend=settings.celery.backend,
)
app.autodiscover_tasks(packages=["app.task"])
app.conf.timezone = "UTC"

app.conf.ONCE = {
    "backend": "celery_once.backends.Redis",
    "settings": {
        "url": settings.celery.once_backend,
        "default_timeout": settings.celery.once_default_timeout,
    },
}

app.conf.beat_schedule = {
    "scrape_products_task": {
        "task": "app.task.tasks.scrape_products_task",
        "schedule": crontab(minute="*/5"),
        "args": (),
    },
}


@setup_logging.connect
def config_loggers(*args, **kwargs):
    logging.config.dictConfig(LOGGING_CONFIG)
