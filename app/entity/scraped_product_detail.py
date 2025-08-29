from datetime import datetime

from sqlalchemy import Column, Integer, String, Numeric, Text, ForeignKey, func, DateTime
from sqlalchemy.orm import relationship

from app.config.database import Base
from app.util.util_datetime import DateTimeUtil


class ScrapedProductDetail(Base):
    __tablename__ = "scraped_product_detail"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    link = Column(String(1024))
    image_link = Column(String(1024))
    price = Column(Numeric(10, 0), nullable=False)
    mall_name = Column(String(128))
    product_type = Column(String(128))
    brand = Column(String(128))
    maker = Column(String(128))
    scraped_result = Column(Text)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)

    # relationships
    scraped_product_id = Column(
        Integer, ForeignKey("scraped_product.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    scraped_product = relationship("ScrapedProduct", back_populates="details")

    def __repr__(self):
        return f"<ScrapedProductDetail(mall_name='{self.mall_name}', price='{self.price}', link='{self.link}')>"

    @property
    def created_at_with_timezone(self) -> datetime:
        return DateTimeUtil.to_utc(self.created_at)
