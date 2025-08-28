import logging

from celery_once import QueueOnce

from app.api.naver_shopping_api import NaverShoppingApi
from app.config.celery import app
from app.enum.channel_enum import ChannelEnum
from app.service.keyword_service import KeywordService
from app.service.scraped_product_service import ScrapedProductService

logger = logging.getLogger(__name__)


@app.task(base=QueueOnce, once={"graceful": True, "timeout": 60 * 60})
def scrape_naver_shopping_task():
    naver_shopping_api = NaverShoppingApi()
    keyword_service = KeywordService()
    scraped_product_service = ScrapedProductService()

    keywords = keyword_service.get_available_keywords()
    if len(keywords) < 0:
        return

    logger.info("[SCRAPE_NAVER_SHOPPING_TASK] 🚀 키워드 별 상품정보 수집 시작 🚀")
    # for keyword in keywords:
    #     searched_items = naver_shopping_api.search_with_all_pages(keyword.word)
    #     scraped_product_service.save_naver_shopping_search_result(
    #         items=searched_items,
    #         keyword_id=keyword.id,
    #         is_tracking_required=True,
    #     )
    logger.info("[SCRAPE_NAVER_SHOPPING_TASK] 😎 키워드 별 상품정보 수집 종료 😎")

    logger.info("[SCRAPE_NAVER_SHOPPING_TASK] 🚀 추가 트래킹 필요한 상품정보 수집 시작 🚀")
    scraped_products_tracking_required = scraped_product_service.get_tracking_required_products(
        ChannelEnum.NAVER_SHOPPING
    )
    for product in scraped_products_tracking_required:
        searched_items = naver_shopping_api.search_with_all_pages(product.name)
        scraped_product_service.save_naver_shopping_search_result(
            searched_items=searched_items,
            keyword_id=product.keyword_id,
            is_tracking_required=False,
        )

    logger.info("[SCRAPE_NAVER_SHOPPING_TASK] 😎 추가 트래킹 필요한 상품정보 수집 종료 😎")


def scrape_naver_shopping_tracking_required_task():
    pass
