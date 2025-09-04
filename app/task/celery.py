import logging

from celery import Celery
from celery.schedules import crontab
from celery.signals import task_failure

from app.config.settings import get_settings

settings = get_settings()

celery_app = Celery(
    "fitpetScraper",
    broker=settings.celery.broker,
    # backend=settings.database.celery_result_backend, # todo 에러 발생하는데? 원인 확인 필요
)
celery_app.autodiscover_tasks(packages=["app.task"])
celery_app.conf.timezone = "UTC"

celery_app.conf.ONCE = {
    "backend": "celery_once.backends.Redis",
    "settings": {
        "url": settings.celery.once_backend,
        "default_timeout": settings.celery.once_default_timeout,
    },
}

celery_app.conf.beat_schedule = {
    "scrape_naver_shopping_task": {
        "task": "app.task.tasks.scrape_naver_shopping_task",
        "schedule": crontab(minute="10", hour="16"),  # KST 1시 10분 (UTC 16시 10분)
        "args": (),
    },
}

# @setup_logging.connect
# def config_loggers(*args, **kwargs):
#     sys.excepthook = log_exception_handler


@task_failure.connect
def task_failure_handler(
    sender=None,
    task_id=None,
    exception=None,
    args=None,
    kwargs=None,
    traceback=None,
    einfo=None,
    **kwds,
):
    logging.error(
        f"Task {sender.name} failed with task_id: {task_id}. " f"Exception: {exception}. Traceback: {traceback}",
        exc_info=einfo,
    )
