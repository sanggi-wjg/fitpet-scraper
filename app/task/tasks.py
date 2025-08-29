import logging
import os.path
from collections import defaultdict
from datetime import datetime
from typing import Any

import pandas as pd
from celery_once import QueueOnce

from app.api.naver_shopping_api import NaverShoppingApi
from app.api.slack_client import SlackClient
from app.config.settings import get_settings
from app.enum.channel_enum import ChannelEnum
from app.repository.model.search_conditions import ScrapedProductSearchCondition
from app.service.keyword_service import KeywordService
from app.service.model.service_models import ScrapedProductWithRelatedModel
from app.service.scraped_product_service import ScrapedProductService
from app.task.celery import celery_app
from app.util.util_datetime import DateTimeUtil

logger = logging.getLogger(__name__)
settings = get_settings()


@celery_app.task(base=QueueOnce, once={"graceful": True, "timeout": 60 * 5})
def scrape_naver_shopping_task():
    naver_shopping_api = NaverShoppingApi()
    keyword_service = KeywordService()
    scraped_product_service = ScrapedProductService()

    scrape_products_by_keywords(
        naver_shopping_api,
        keyword_service,
        scraped_product_service,
    )
    scrape_tracking_required_products(
        naver_shopping_api,
        scraped_product_service,
    )
    excel_filepath = create_excel_from_scraped_products(scraped_product_service)
    send_slack_notification(excel_filepath)


def create_excel_from_scraped_products(scraped_product_service: ScrapedProductService) -> str:
    logger.info("[CREATE_EXCEL_FROM_SCRAPED_PRODUCTS] 🚀 엑셀 생성 시작 🚀")

    scraped_products = scraped_product_service.get_all_products_with_related(
        ScrapedProductSearchCondition(
            created_at_after=DateTimeUtil.subtract_hours_from(1),
            channel=ChannelEnum.NAVER_SHOPPING,
        )
    )
    dataset = defaultdict(list)

    for product in scraped_products:
        dataset[product.keyword.word].extend(flatten_scraped_product_details(product))

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    excel_filepath = os.path.join(settings.directory.data, f"scraped_products_{timestamp}.xlsx")

    with pd.ExcelWriter(excel_filepath, engine="openpyxl") as writer:
        for keyword, rows in dataset.items():
            df = pd.DataFrame(rows)
            df.to_excel(writer, sheet_name=keyword, index=False)

    logger.info("[CREATE_EXCEL_FROM_SCRAPED_PRODUCTS] 😎 엑셀 생성 종료 😎")
    return excel_filepath


def flatten_scraped_product_details(
    scraped_product: ScrapedProductWithRelatedModel,
) -> list[dict[str, Any]]:
    return [
        {
            "name": scraped_product.name,
            "channel": scraped_product.channel.value,
            "channel_product_id": scraped_product.channel_product_id,
            "product_created_at": scraped_product.created_at,
            "link": detail.link,
            "image_link": detail.image_link,
            "price": detail.price,
            "mall_name": detail.mall_name,
            "product_type": detail.product_type,
            "brand": detail.brand,
            "maker": detail.maker,
            "scraped_result": detail.scraped_result,
            "detail_created_at": detail.created_at,
        }
        for detail in scraped_product.details
    ]


def scrape_products_by_keywords(
    naver_shopping_api: NaverShoppingApi,
    keyword_service: KeywordService,
    scraped_product_service: ScrapedProductService,
):
    logger.info("[SCRAPE_PRODUCTS_BY_KEYWORDS] 🚀 키워드 별 상품정보 수집 시작 🚀")

    keywords = keyword_service.get_available_keywords()
    if len(keywords) <= 0:
        return

    for keyword in keywords:
        searched_items = naver_shopping_api.search_with_all_pages(keyword.word)
        scraped_product_service.save_naver_shopping_search_result(
            searched_items,
            keyword.id,
            keyword.word,
            is_tracking_required=True,
        )

    logger.info("[SCRAPE_PRODUCTS_BY_KEYWORDS] 😎 키워드 별 상품정보 수집 종료 😎")


def scrape_tracking_required_products(
    naver_shopping_api: NaverShoppingApi,
    scraped_product_service: ScrapedProductService,
):
    logger.info("[SCRAPE_TRACKING_REQUIRED_PRODUCTS] 🚀 추가 트래킹 필요한 상품정보 수집 시작 🚀")

    scraped_products_tracking_required = scraped_product_service.get_tracking_required_products(
        ChannelEnum.NAVER_SHOPPING
    )
    for product in scraped_products_tracking_required:
        searched_items = naver_shopping_api.search_with_all_pages(product.name)
        scraped_product_service.save_naver_shopping_search_result(
            searched_items,
            product.keyword.id,
            product.keyword.word,
            is_tracking_required=False,
        )

    logger.info("[SCRAPE_TRACKING_REQUIRED_PRODUCTS] 😎 추가 트래킹 필요한 상품정보 수집 종료 😎")


def send_slack_notification(filepath: str):
    logger.info("[SEND_SLACK_NOTIFICATION] 🚀 슬랙 웹훅 시작 🚀")

    slack_client = SlackClient()
    upload_result = slack_client.upload_file(filepath, settings.slack.channel_test_id)
    if upload_result.is_failure:
        logger.warning("Failed to upload file to slack")

    logger.info("[SEND_SLACK_NOTIFICATION] 😎 슬랙 웹훅 종료 😎")
