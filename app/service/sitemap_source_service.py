import logging
import os
from urllib.request import urlretrieve

from sqlalchemy.orm import Session

from app.client.pet_friends_client import get_pet_friends_client
from app.core.settings import get_settings
from app.entity import ScrapedProduct, ScrapedProductDetail, SitemapSource
from app.enum.channel_enum import ChannelEnum
from app.repository.scraped_product_repository import ScrapedProductRepository
from app.repository.sitemap_source_repository import SitemapSourceRepository
from app.util.util_datetime import UtilDatetime
from app.util.util_string import extract_product_id_from_pet_friends_product_detail_url
from app.util.util_xml import extract_product_detail_urls_from_xml

settings = get_settings()
logger = logging.getLogger(__name__)


class SitemapSourceService:

    def __init__(self, session: Session):
        self.sitemap_source_repository = SitemapSourceRepository(session)
        self.scraped_product_repository = ScrapedProductRepository(session)

    def get_all(self) -> list[SitemapSource]:
        return self.sitemap_source_repository.find_all()

    def pull_sitemap_sources(self) -> None:
        sitemap_sources = self.sitemap_source_repository.find_all()

        for source in sitemap_sources:
            filepath = os.path.join(settings.directory.data, source.get_escaped_sitemap_url())
            urlretrieve(source.sitemap_url, filepath)
            source.pulled(filepath)

    def scrape_products_from_sitemap_sources(self) -> None:
        sitemap_sources = [
            sitemap_source
            for sitemap_source in self.sitemap_source_repository.find_all()
            if sitemap_source.is_syncable()
        ]

        product_detail_urls = set()

        for source in sitemap_sources:
            if source.filepath is None:
                continue

            urls = extract_product_detail_urls_from_xml(source.filepath)
            product_detail_urls.update(urls)

        scraped_products = self.scraped_product_repository.find_all_by_channel(ChannelEnum.PET_FRIENDS)
        scraped_product_by_id = dict(
            {scraped_product.channel_product_id: scraped_product for scraped_product in scraped_products}
        )

        pet_friend_client = get_pet_friends_client()

        for detail_url in product_detail_urls:
            product_id = extract_product_id_from_pet_friends_product_detail_url(detail_url)

            # 3시간 이내에 스크래핑한 상품은 스킵
            scraped_product = scraped_product_by_id.get(product_id)
            hours_ago = UtilDatetime.subtract_hours_from(3)
            if (
                scraped_product
                and scraped_product.last_scraped_at is not None
                and scraped_product.last_scraped_at > hours_ago
            ):
                continue

            # 한번 호출하고 나서
            response = pet_friend_client.get_product_detail(product_id)
            product_detail = response.data.product_detail.value

            if scraped_product is None:
                scraped_product = self.scraped_product_repository.save(
                    ScrapedProduct(
                        name=product_detail.product_name,
                        channel=ChannelEnum.PET_FRIENDS,
                        channel_product_id=product_id,
                        is_tracking_required=False,
                    )
                )

            scraped_product.last_scraped_at = UtilDatetime.utc_now()
            scraped_product.details.append(
                ScrapedProductDetail(
                    scraped_product_id=scraped_product.id,
                    link=detail_url,
                    image_link=product_detail.top_image_url,
                    price=product_detail.selling_price,
                    mall_name=ChannelEnum.PET_FRIENDS.value,
                    product_type=product_detail.product_type,
                    brand=product_detail.brand_name,
                    scraped_result=product_detail.model_dump_json(),
                )
            )
