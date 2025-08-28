from decimal import Decimal

from sqlalchemy import Column, Integer, String, DateTime, Enum, func, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.config.database import Base
from app.enum.channel_enum import ChannelEnum


class ScrapedProduct(Base):
    __tablename__ = "scraped_product"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(1024), nullable=False, index=True)
    channel = Column(Enum(ChannelEnum), nullable=False, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    is_tracking_required = Column(Boolean, nullable=False, default=False)

    # relationships
    keyword_id = Column(Integer, ForeignKey("keyword.id", ondelete="RESTRICT"), nullable=True, index=True)
    keyword = relationship("Keyword", back_populates="scraped_products")
    details = relationship("ScrapedProductDetail", back_populates="scraped_product")

    def __repr__(self):
        return f"<Product(name='{self.name}', platform='{self.channel}')>"

    def update_need_tracking(self):
        self.is_tracking_required = True

    def update_not_need_tracking(self):
        self.is_tracking_required = False

    def add_detail_from_naver_shopping(
        self,
        link: str,
        image_link: str,
        price: Decimal,
        mall_name: str,
        product_id: str,
        product_type: str,
        brand: str,
        maker: str,
        scraped_result: str,
    ) -> "ScrapedProductDetail":
        from app.entity import ScrapedProductDetail

        detail = ScrapedProductDetail(
            link=link,
            image_link=image_link,
            price=price,
            mall_name=mall_name,
            product_id=product_id,
            product_type=product_type,
            brand=brand,
            maker=maker,
            scraped_result=scraped_result,
        )
        self.details.append(detail)
        return detail
