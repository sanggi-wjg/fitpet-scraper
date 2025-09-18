import json
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.enum.channel_enum import ChannelEnum


class KeywordModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    word: str


class ScrapedProductModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    channel: ChannelEnum
    channel_product_id: str
    is_tracking_required: bool
    created_at: datetime
    keyword: KeywordModel | None


class ScrapedProductDetailModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    link: str | None
    image_link: str | None
    price: Decimal
    mall_name: str | None
    product_type: str | None
    brand: str | None
    maker: str | None
    scraped_result: str | None
    created_at: datetime


class ScrapedProductWithRelatedModel(ScrapedProductModel):
    model_config = ConfigDict(from_attributes=True)

    details: list[ScrapedProductDetailModel]

    def flatten_last_detail_for_naver_shopping(self) -> dict | None:
        if len(self.details) == 0:
            return None

        detail = self.details[-1]
        scraped_result = json.loads(detail.scraped_result) if detail.scraped_result else dict()

        return {
            "name": self.name,
            "channel": self.channel.value,
            "channel_product_id": self.channel_product_id,
            "product_created_at": str(self.created_at),
            "link": detail.link,
            "image_link": detail.image_link,
            "price": detail.price,
            "mall_name": detail.mall_name,
            "product_type": detail.product_type,
            "brand": detail.brand,
            "maker": detail.maker,
            "category1": scraped_result.get("category1", ""),
            "category2": scraped_result.get("category2", ""),
            "category3": scraped_result.get("category3", ""),
            "category4": scraped_result.get("category4", ""),
            "detail_created_at": str(detail.created_at),
        }

    def flatten_last_detail_for_pet_friends(self) -> dict | None:
        if len(self.details) == 0:
            return None

        detail = self.details[-1]
        scraped_result = json.loads(detail.scraped_result) if detail.scraped_result else dict()
        return {
            "name": self.name,
            "channel": self.channel.value,
            "channel_product_id": self.channel_product_id,
            # "product_created_at": str(self.created_at),
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


class SitemapSourceModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    channel: ChannelEnum
    sitemap_url: str
    filepath: str | None
    created_at: datetime
    last_pulled_at: datetime | None
    last_synced_at: datetime | None
