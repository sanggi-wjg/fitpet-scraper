import json
import os.path
from datetime import datetime
from typing import Any

import pandas as pd
from celery_once import QueueOnce

from app.config.settings import get_settings
from app.enum.channel_enum import ChannelEnum
from app.repository.model.search_conditions import ScrapedProductSearchCondition
from app.service.model.service_models import ScrapedProductWithRelatedModel
from app.service.scraped_product_service import get_scraped_product_service
from app.service.sitemap_source_service import get_sitemap_source_service
from app.task.celery import celery_app

settings = get_settings()


@celery_app.task(base=QueueOnce, once={"graceful": True, "timeout": 60 * 5})
def pull_sitemap_sources():
    sitemap_source_service = get_sitemap_source_service()
    sitemap_source_service.pull_sitemap_sources()


@celery_app.task(base=QueueOnce, once={"graceful": True, "timeout": 60 * 5})
def scrape_products_from_sitemap_sources():
    sitemap_source_service = get_sitemap_source_service()
    sitemap_source_service.scrape_products_from_sitemap_sources()


def create_pet_friends_excel_from_scraped_products():
    scraped_product_service = get_scraped_product_service()
    scraped_products = scraped_product_service.get_all_products_with_related(
        ScrapedProductSearchCondition(channel=ChannelEnum.PET_FRIENDS)
    )

    flattened_data = []
    for product in scraped_products:
        flattened = flatten_pet_friends_scraped_product_details(product)
        if flattened is not None:
            flattened_data.append(flattened)

    df = pd.DataFrame(flattened_data)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    excel_filepath = os.path.join(settings.directory.data, f"pet_friends_{timestamp}.xlsx")
    df.to_excel(excel_filepath, index=False, engine="xlsxwriter")


def flatten_pet_friends_scraped_product_details(
    scraped_product: ScrapedProductWithRelatedModel,
) -> dict[str, Any] | None:
    detail = scraped_product.details[-1]
    if not detail:
        return None

    scraped_result = json.loads(detail.scraped_result) if detail.scraped_result else dict()
    return {
        "name": scraped_product.name,
        "channel": scraped_product.channel.value,
        "channel_product_id": scraped_product.channel_product_id,
        # "product_created_at": str(scraped_product.created_at),
        "link": detail.link,
        "image_link": detail.image_link,
        "price": detail.price,
        "mall_name": detail.mall_name,
        "product_type": detail.product_type,
        "brand": detail.brand,
        "maker": detail.maker,
        "category1": scraped_result.get("product_group1_name", ""),
        "category2": scraped_result.get("product_group2_name", ""),
        "category3": scraped_result.get("product_group3_name", ""),
        # "detail_created_at": str(detail.created_at),
        "리뷰": str(scraped_result.get("review_count", "")),
        "리뷰 평점": str(scraped_result.get("review_rating_average", "")),
    }
