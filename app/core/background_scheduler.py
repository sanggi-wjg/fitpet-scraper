import multiprocessing

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from app.task.health_task import health_check_task
from app.task.scrape_tasks import scrape_naver_shopping_task

"""
https://apscheduler.readthedocs.io/en/3.x/userguide.html#
"""

_cpu_count = multiprocessing.cpu_count()


class _BackgroundSchedulerStores:
    DEFAULT = "default"


class _BackgroundSchedulerExecutors:
    DEFAULT = "default"
    PROCESS_POOL = "processpool"


scheduler = BackgroundScheduler(
    stores={
        _BackgroundSchedulerStores.DEFAULT: "memory",
    },
    executors={
        _BackgroundSchedulerExecutors.DEFAULT: ThreadPoolExecutor(10),
    },
    job_defaults={
        "misfire_grace_time": 3600,  # 1시간까지 지나도 실행 허용
        "max_instances": 1,  # 동일 작업 중복 실행 방지
        "coalesce": False,
    },
    timezone="UTC",
)

scheduler.add_job(health_check_task, "interval", minutes=1)
scheduler.add_job(
    scrape_naver_shopping_task,
    CronTrigger(hour=9, minute=0, timezone="Asia/Seoul"),
)
