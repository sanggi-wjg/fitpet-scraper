from typing import List

from sqlalchemy.orm import joinedload

from app.entity import ScrapedProduct, Keyword
from app.enum.channel_enum import ChannelEnum
from app.repository.base_repository import BaseRepository
from app.repository.model.search_conditions import ScrapedProductSearchCondition


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
            .options(
                joinedload(self.entity.details),
            )
            .filter(
                self.entity.channel == channel,
                self.entity.channel_product_id == product_id,
            )
            .first()
        )

    def find_all_by_channel_and_tracking_required(self, channel: ChannelEnum) -> List[ScrapedProduct]:
        return (
            self.session.query(self.entity)
            .options(
                joinedload(self.entity.keyword),
            )
            .filter(
                self.entity.channel == channel,
                self.entity.is_tracking_required,
            )
            .order_by(self.entity.id.asc())
            .all()
        )

    def find_all_with_related(self, search_condition: ScrapedProductSearchCondition) -> list[ScrapedProduct]:
        query = (
            self.session.query(self.entity)
            .options(
                joinedload(self.entity.keyword),
                joinedload(self.entity.details),
            )
            .filter(
                Keyword.is_deleted.is_(False),
            )
        )
        if search_condition.created_at_before:
            query = query.filter(self.entity.created_at <= search_condition.created_at_before)
        if search_condition.created_at_after:
            query = query.filter(self.entity.created_at >= search_condition.created_at_after)
        if search_condition.name:
            query = query.filter(self.entity.name.contains(search_condition.name))
        if search_condition.channel:
            query = query.filter(self.entity.channel == search_condition.channel)

        return (
            query.order_by(
                self.entity.keyword_id.asc(),
                self.entity.id.asc(),
                # ScrapedProductDetail.id.asc(),
            )
            .distinct()
            .all()
        )
