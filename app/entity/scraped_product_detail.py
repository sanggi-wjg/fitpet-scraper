from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import String, Numeric, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utc import UtcDateTime, utcnow

from app.core.database import Base

if TYPE_CHECKING:
    from app.entity.scraped_product import ScrapedProduct


class ScrapedProductDetail(Base):
    __tablename__ = "scraped_product_detail"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    link: Mapped[str | None] = mapped_column(String(1024))
    image_link: Mapped[str | None] = mapped_column(String(1024))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 0), nullable=False)
    mall_name: Mapped[str | None] = mapped_column(String(128))
    product_type: Mapped[str | None] = mapped_column(String(128))
    brand: Mapped[str | None] = mapped_column(String(128))
    maker: Mapped[str | None] = mapped_column(String(128))
    scraped_result: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(UtcDateTime(), default=utcnow(), nullable=False)

    # relationships
    scraped_product_id: Mapped[int] = mapped_column(
        ForeignKey("scraped_product.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    scraped_product: Mapped["ScrapedProduct"] = relationship("ScrapedProduct", back_populates="details")

    def __repr__(self):
        return f"<ScrapedProductDetail(mall_name='{self.mall_name}', price='{self.price}', link='{self.link}')>"
