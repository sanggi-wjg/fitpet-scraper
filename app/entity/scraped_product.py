from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy_utc import UtcDateTime, utcnow

from app.config.database import Base
from app.enum.channel_enum import ChannelEnum


class ScrapedProduct(Base):
    __tablename__ = "scraped_product"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(1024), nullable=False, index=True)
    channel = Column(Enum(ChannelEnum), nullable=False, index=True)
    channel_product_id = Column(String(1024), nullable=False, index=True)
    created_at = Column(UtcDateTime(), default=utcnow(), nullable=False)
    is_tracking_required = Column(Boolean, nullable=False, default=False)

    # relationships
    keyword_id = Column(Integer, ForeignKey("keyword.id", ondelete="RESTRICT"), nullable=True, index=True)
    keyword = relationship("Keyword", back_populates="scraped_products")
    details = relationship("ScrapedProductDetail", back_populates="scraped_product")

    def __repr__(self):
        return f"<Product(name='{self.name}', channel='{self.channel}', channel_product_id='{self.channel_product_id}')>"

    def update_tracking_require(self):
        self.is_tracking_required = True

    def update_tracking_disable(self):
        self.is_tracking_required = False
