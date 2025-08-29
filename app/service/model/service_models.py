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
    keyword: KeywordModel


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
    details: list[ScrapedProductDetailModel]
