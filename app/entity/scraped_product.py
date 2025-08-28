from sqlalchemy import Column, Integer, String, DateTime, Enum, func, ForeignKey
from sqlalchemy.orm import relationship

from app.config.database import Base
from app.enum.channel_enum import ChannelEnum


class ScrapedProduct(Base):
    __tablename__ = "scraped_product"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(1024), nullable=False, index=True)
    channel = Column(Enum(ChannelEnum), nullable=False, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    # relationships
    keyword_id = Column(Integer, ForeignKey("keyword.id", ondelete="RESTRICT"), nullable=True, index=True)
    keyword = relationship("Keyword", back_populates="scraped_products")
    details = relationship("ScrapedProductDetail", back_populates="scraped_product")

    def __repr__(self):
        return f"<Product(name='{self.name}', platform='{self.channel}')>"

    # def add_price(self, price: Decimal, discount: Optional[int]) -> "ScrapedProductDetail":
    #     from app.entity.scraped_product_detail import ScrapedProductDetail
    #     detail = ProductPrice(price=price, discount=discount)
    #     self.prices.append(new_price)
    #     return new_price
