import logging
import os.path
from collections import defaultdict
from datetime import datetime

import pandas as pd

from app.client.naver_shopping_client import NaverShoppingClient
from app.client.slack_client import SlackClient
from app.core.database import get_db_session
from app.core.settings import get_settings
from app.enum.channel_enum import ChannelEnum
from app.repository.model.search_conditions import ScrapedProductSearchCondition
from app.service.keyword_service import KeywordService
from app.service.scraped_product_service import ScrapedProductService

logger = logging.getLogger(__name__)
settings = get_settings()


def scrape_naver_shopping_task():
    naver_shopping_client = NaverShoppingClient()

    with get_db_session() as session:
        keyword_service = KeywordService(session)
        keywords = keyword_service.get_keywords()
        if len(keywords) <= 0:
            return
        logger.info(f"[SCRAPE_NAVER_SHOPPING_TASK] 🚀 키워드 별 상품정보 수집 시작. 키워드: {keywords} 🚀")

    with get_db_session() as session:
        scraped_product_service = ScrapedProductService(session)
        scraped_product_service.delete_by_channel(ChannelEnum.NAVER_SHOPPING)
        logger.info("[SCRAPE_NAVER_SHOPPING_TASK] 😎 이전 데이터 삭제 완료")

    for keyword in keywords:
        searched_items = naver_shopping_client.search_with_all_pages(keyword.word)

        with get_db_session() as session:
            scraped_product_service = ScrapedProductService(session)
            scraped_product_service.save_naver_shopping_search_result(
                searched_items,
                keyword.id,
                keyword.word,
                is_tracking_required=True,
            )
        logger.info("[SCRAPE_NAVER_SHOPPING_TASK] 😎 키워드 별 상품정보 수집 종료 😎")

    with get_db_session() as session:
        scraped_product_service = ScrapedProductService(session)
        scraped_products_tracking_required = scraped_product_service.get_tracking_required_products(
            ChannelEnum.NAVER_SHOPPING
        )

    for product in scraped_products_tracking_required:
        searched_items = naver_shopping_client.search_with_all_pages(product.name)
        scraped_product_service.save_naver_shopping_search_result(
            searched_items,
            product.keyword.id,
            product.keyword.word,
            is_tracking_required=False,
        )
    logger.info("[SCRAPE_TRACKING_REQUIRED_PRODUCTS] 😎 추가 트래킹 필요한 상품정보 수집 종료 😎")

    excel_filepath = create_excel_from_scraped_products(scraped_product_service)
    send_slack_notification(excel_filepath)


def create_excel_from_scraped_products(scraped_product_service: ScrapedProductService) -> str:
    with get_db_session() as session:
        scraped_product_service = ScrapedProductService(session)
        scraped_products = scraped_product_service.get_all_products_with_latest_detail(
            ScrapedProductSearchCondition(channel=ChannelEnum.NAVER_SHOPPING)
        )

    dataset = defaultdict(list)

    for product in scraped_products:
        flattened = product.flatten_last_detail_for_naver_shopping()
        if flattened is not None:
            dataset[product.keyword.word].append(flattened)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    excel_filepath = os.path.join(settings.directory.data, f"scraped_products_{timestamp}.xlsx")

    with pd.ExcelWriter(excel_filepath, engine="xlsxwriter") as writer:
        for keyword, data in dataset.items():
            df = pd.DataFrame(data)
            df.to_excel(writer, sheet_name=keyword, index=False)

    logger.info("[CREATE_EXCEL_FROM_SCRAPED_PRODUCTS] 😎 엑셀 생성 종료 😎")
    return excel_filepath


def send_slack_notification(filepath: str):
    slack_client = SlackClient()
    slack_client.upload_file(filepath, settings.slack.channel_fitpet_scraper_id)
    os.remove(filepath)
    logger.info("[SEND_SLACK_NOTIFICATION] 😎 슬랙 웹훅 종료 😎")
