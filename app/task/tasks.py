import logging
import os.path

from celery_once import QueueOnce

from app.api.naver_shopping_api import NaverShoppingApi
from app.api.slack_client import SlackClient
from app.config.settings import get_settings
from app.enum.channel_enum import ChannelEnum
from app.service.keyword_service import KeywordService
from app.service.scraped_product_service import ScrapedProductService
from app.task.celery import celery_app

logger = logging.getLogger(__name__)
settings = get_settings()


@celery_app.task(base=QueueOnce, once={"graceful": True, "timeout": 60 * 5})
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
    #         searched_items, keyword.id, keyword.word, is_tracking_required=True
    #     )
    logger.info("[SCRAPE_NAVER_SHOPPING_TASK] 😎 키워드 별 상품정보 수집 종료 😎")

    logger.info("[SCRAPE_NAVER_SHOPPING_TASK] 🚀 추가 트래킹 필요한 상품정보 수집 시작 🚀")
    scraped_products_tracking_required = scraped_product_service.get_tracking_required_products(
        ChannelEnum.NAVER_SHOPPING
    )
    # for product in scraped_products_tracking_required:
    #     searched_items = naver_shopping_api.search_with_all_pages(product.name)
    #     scraped_product_service.save_naver_shopping_search_result(
    #         searched_items,
    #         product.keyword.id,
    #         product.keyword.word,
    #         is_tracking_required=False,
    #     )
    logger.info("[SCRAPE_NAVER_SHOPPING_TASK] 😎 추가 트래킹 필요한 상품정보 수집 종료 😎")
    logger.info("[SCRAPE_NAVER_SHOPPING_TASK] 🚀 슬랙 웹훅 시작 🚀")
    file_path = os.path.join(settings.directory.data, "test.png")

    slack_client = SlackClient()
    upload_result = slack_client.upload_file(file_path, settings.slack.channel_test_id)
    if upload_result.is_failure:
        raise upload_result.exception_or_none()
    logger.info("[SCRAPE_NAVER_SHOPPING_TASK] 😎 슬랙 웹훅 종료 😎")
