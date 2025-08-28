from typing import List

from app.entity import ScrapedProduct
from app.enum.channel_enum import ChannelEnum
from app.repository.base_repository import BaseRepository


class ScrapedProductRepository(BaseRepository[ScrapedProduct]):

    def find_by_channel_and_name(self, channel: ChannelEnum, name: str) -> ScrapedProduct | None:
        return (
            self.session.query(self.entity)
            .filter(
                ScrapedProduct.channel == channel,
                ScrapedProduct.name == name,
            )
            .first()
        )

    def find_by_channel_and_product_id(self, channel: ChannelEnum, product_id: str) -> ScrapedProduct | None:
        return (
            self.session.query(self.entity)
            .filter(
                ScrapedProduct.channel == channel,
                ScrapedProduct.channel_product_id == product_id,
            )
            .first()
        )

    def find_all_channel_and_tracking_required(self, channel: ChannelEnum) -> List[ScrapedProduct]:
        return (
            self.session.query(self.entity)
            .filter(
                ScrapedProduct.channel == channel,
                ScrapedProduct.is_tracking_required,
            )
            .all()
        )
