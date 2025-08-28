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
