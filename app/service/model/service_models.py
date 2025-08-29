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
    keyword: KeywordModel
