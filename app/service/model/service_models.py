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


class SitemapSourceModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    channel: ChannelEnum
    sitemap_url: str
    filepath: str | None
    created_at: datetime
    last_pulled_at: datetime | None
    last_synced_at: datetime | None
