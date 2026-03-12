import json
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Enum, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utc import UtcDateTime, utcnow

from app.core.database import Base
from app.enum.channel_enum import ChannelEnum

if TYPE_CHECKING:
    from app.entity.keyword import Keyword
    from app.entity.scraped_product_detail import ScrapedProductDetail


class ScrapedProduct(Base):
    __tablename__ = "scraped_product"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False, index=True)
    channel: Mapped[ChannelEnum] = mapped_column(Enum(ChannelEnum), nullable=False, index=True)
    channel_product_id: Mapped[str] = mapped_column(String(256), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(UtcDateTime(), default=utcnow(), nullable=False)
    is_tracking_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # relationships
    keyword_id: Mapped[int] = mapped_column(ForeignKey("keyword.id", ondelete="RESTRICT"), nullable=True, index=True)
    keyword: Mapped["Keyword"] = relationship("Keyword", back_populates="scraped_products")
    details: Mapped[list["ScrapedProductDetail"]] = relationship(
        "ScrapedProductDetail", back_populates="scraped_product", cascade="all, delete-orphan", lazy="selectin"
    )

    def __repr__(self):
        return (
            f"<Product(name='{self.name}', channel='{self.channel}', channel_product_id='{self.channel_product_id}')>"
        )

    def update_tracking_require(self):
        self.is_tracking_required = True

    def update_tracking_disable(self):
        self.is_tracking_required = False

    def flatten_last_detail_for_naver_shopping(self) -> dict | None:
        if len(self.details) == 0:
            return None

        detail = self.details[-1]
        scraped_result = json.loads(detail.scraped_result) if detail.scraped_result else {}

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
        scraped_result = json.loads(detail.scraped_result) if detail.scraped_result else {}

        return {
            "name": self.name,
            "channel": self.channel.value,
            "channel_product_id": self.channel_product_id,
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
            "리뷰": str(scraped_result.get("review_count", "")),
            "리뷰 평점": str(scraped_result.get("review_rating_average", "")),
        }
