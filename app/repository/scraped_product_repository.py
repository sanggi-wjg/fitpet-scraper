from sqlalchemy import select, func
from sqlalchemy.orm import joinedload, contains_eager, Session

from app.entity import ScrapedProduct, ScrapedProductDetail, Keyword
from app.enum.channel_enum import ChannelEnum
from app.repository.model.search_conditions import ScrapedProductSearchCondition


class ScrapedProductRepository:

    def __init__(self, session: Session):
        self.session = session

    def save(self, scraped_product: ScrapedProduct) -> ScrapedProduct:
        self.session.add(scraped_product)
        self.session.flush()
        return scraped_product

    def find_by_channel_and_name(self, channel: ChannelEnum, name: str) -> ScrapedProduct | None:
        stmt = select(ScrapedProduct).where(
            ScrapedProduct.channel == channel,
            ScrapedProduct.name == name,
        )
        return self.session.scalar(stmt)

    def find_by_channel_and_product_id(self, channel: ChannelEnum, product_id: str) -> ScrapedProduct | None:
        stmt = (
            select(ScrapedProduct)
            .options(joinedload(ScrapedProduct.details))
            .where(
                ScrapedProduct.channel == channel,
                ScrapedProduct.channel_product_id == product_id,
            )
        )
        return self.session.scalar(stmt)

    def find_all_by_channel(self, channel: ChannelEnum) -> list[ScrapedProduct]:
        stmt = (
            select(ScrapedProduct)
            .options(joinedload(ScrapedProduct.details))
            .where(ScrapedProduct.channel == channel)
            .order_by(ScrapedProduct.id.asc())
        )
        return list(self.session.scalars(stmt).unique())

    def find_all_by_channel_and_tracking_required(self, channel: ChannelEnum) -> list[ScrapedProduct]:
        stmt = (
            select(ScrapedProduct)
            .options(joinedload(ScrapedProduct.keyword))
            .where(
                ScrapedProduct.channel == channel,
                ScrapedProduct.is_tracking_required.is_(True),
            )
            .order_by(ScrapedProduct.id.asc())
        )
        return list(self.session.scalars(stmt).unique())

    def find_all_with_related(self, search_condition: ScrapedProductSearchCondition) -> list[ScrapedProduct]:
        stmt = (
            select(ScrapedProduct)
            .join(ScrapedProduct.keyword)
            .options(
                contains_eager(ScrapedProduct.keyword),
                joinedload(ScrapedProduct.details),
            )
            .where(Keyword.is_deleted.is_(False))
        )
        if search_condition.created_at_before:
            stmt = stmt.where(ScrapedProduct.created_at <= search_condition.created_at_before)
        if search_condition.created_at_after:
            stmt = stmt.where(ScrapedProduct.created_at >= search_condition.created_at_after)
        if search_condition.name:
            stmt = stmt.where(ScrapedProduct.name.contains(search_condition.name))
        if search_condition.channel:
            stmt = stmt.where(ScrapedProduct.channel == search_condition.channel)

        stmt = stmt.order_by(
            ScrapedProduct.keyword_id.asc(),
            ScrapedProduct.id.asc(),
        ).distinct()
        return list(self.session.scalars(stmt).unique())

    def find_all_with_latest_detail(self, search_condition: ScrapedProductSearchCondition) -> list[ScrapedProduct]:
        latest_detail_subquery = (
            select(
                ScrapedProductDetail.scraped_product_id,
                func.max(ScrapedProductDetail.id).label("max_detail_id"),
            )
            .group_by(ScrapedProductDetail.scraped_product_id)
            .subquery()
        )

        stmt = (
            select(ScrapedProduct)
            .join(
                ScrapedProductDetail,
                ScrapedProduct.id == ScrapedProductDetail.scraped_product_id,
            )
            .join(
                latest_detail_subquery,
                (ScrapedProductDetail.scraped_product_id == latest_detail_subquery.c.scraped_product_id)
                & (ScrapedProductDetail.id == latest_detail_subquery.c.max_detail_id),
            )
            .join(ScrapedProduct.keyword)
            .options(
                contains_eager(ScrapedProduct.keyword),
                contains_eager(ScrapedProduct.details),
            )
            .where(Keyword.is_deleted.is_(False))
        )

        if search_condition.created_at_before:
            stmt = stmt.where(ScrapedProduct.created_at <= search_condition.created_at_before)
        if search_condition.created_at_after:
            stmt = stmt.where(ScrapedProduct.created_at >= search_condition.created_at_after)
        if search_condition.name:
            stmt = stmt.where(ScrapedProduct.name.contains(search_condition.name))
        if search_condition.channel:
            stmt = stmt.where(ScrapedProduct.channel == search_condition.channel)

        return list(
            self.session.scalars(
                stmt.order_by(
                    ScrapedProduct.keyword_id.asc(),
                    ScrapedProduct.id.asc(),
                )
            ).unique()
        )

    def delete_by_channel(self, channel: ChannelEnum):
        stmt = select(ScrapedProduct).where(ScrapedProduct.channel == channel)
        products = list(self.session.scalars(stmt))
        for product in products:
            self.session.delete(product)
