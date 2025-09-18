import os.path
from datetime import datetime

import pandas as pd
from celery_once import QueueOnce

from app.config.settings import get_settings
from app.enum.channel_enum import ChannelEnum
from app.repository.model.search_conditions import ScrapedProductSearchCondition
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
        flattened = product.flatten_last_detail_for_pet_friends()
        if flattened is not None:
            flattened_data.append(flattened)

    df = pd.DataFrame(flattened_data)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    excel_filepath = os.path.join(settings.directory.data, f"pet_friends_{timestamp}.xlsx")
    df.to_excel(excel_filepath, index=False, engine="xlsxwriter")
