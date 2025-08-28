import logging

from celery_once import QueueOnce

from app.api.naver_shopping_api import NaverShoppingApi
from app.config.celery import app
from app.service.keyword_service import KeywordService
from app.service.scrape_service import ScrapeService

logger = logging.getLogger(__name__)


@app.task(base=QueueOnce, once={"graceful": True, "timeout": 60 * 60})
def scrape_naver_shopping_task():
    logger.info("[SCRAPE_NAVER_SHOPPING_TASK] 🚀 시작 🚀")

    naver_shopping_api = NaverShoppingApi()
    keyword_service = KeywordService()
    scrape_service = ScrapeService()

    keywords = keyword_service.get_available_keywords()
    if len(keywords) < 0:
        return

    for keyword in keywords:
        items = naver_shopping_api.search_with_all_pages(keyword.word)
        scrape_service.save_naver_shopping_result(
            items=items,
            keyword_id=keyword.id,
            is_tracking_required=True,
        )

    logger.info("[SCRAPE_NAVER_SHOPPING_TASK] 😎 종료 😎")
