import os.path
from datetime import datetime

import pandas as pd

from app.core.database import get_db_session
from app.core.settings import get_settings
from app.enum.channel_enum import ChannelEnum
from app.repository.model.search_conditions import ScrapedProductSearchCondition
from app.service.scraped_product_service import ScrapedProductService
from app.service.sitemap_source_service import SitemapSourceService

settings = get_settings()


# @celery_app.task(base=QueueOnce, once={"graceful": True, "timeout": 60 * 5})
def pull_sitemap_sources():
    with get_db_session() as session:
        sitemap_source_service = SitemapSourceService(session)
        sitemap_source_service.pull_sitemap_sources()


# @celery_app.task(base=QueueOnce, once={"graceful": True, "timeout": 60 * 5})
def scrape_products_from_sitemap_sources():
    with get_db_session() as session:
        sitemap_source_service = SitemapSourceService(session)
        sitemap_source_service.scrape_products_from_sitemap_sources()


def create_pet_friends_excel_from_scraped_products():
    with get_db_session() as session:
        scraped_product_service = ScrapedProductService(session)
        scraped_products = scraped_product_service.get_all_products_with_latest_detail(
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
