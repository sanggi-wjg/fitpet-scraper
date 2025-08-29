from typing import List

from sqlalchemy.orm import joinedload

from app.entity import ScrapedProduct
from app.enum.channel_enum import ChannelEnum
from app.repository.base_repository import BaseRepository


class ScrapedProductRepository(BaseRepository[ScrapedProduct]):

    def find_by_channel_and_name(self, channel: ChannelEnum, name: str) -> ScrapedProduct | None:
        return (
            self.session.query(self.entity)
            .filter(
                self.entity.channel == channel,
                self.entity.name == name,
            )
            .first()
        )

    def find_by_channel_and_product_id(self, channel: ChannelEnum, product_id: str) -> ScrapedProduct | None:
        return (
            self.session.query(self.entity)
            .filter(
                self.entity.channel == channel,
                self.entity.channel_product_id == product_id,
            )
            .first()
        )

    def find_all_by_channel_and_tracking_required(self, channel: ChannelEnum) -> List[ScrapedProduct]:
        return (
            self.session.query(self.entity)
            .options(joinedload(self.entity.keyword))
            .filter(
                self.entity.channel == channel,
                self.entity.is_tracking_required,
            )
            .order_by(self.entity.id.asc())
            .all()
        )
