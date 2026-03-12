from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utc import UtcDateTime, utcnow

from app.core.database import Base

if TYPE_CHECKING:
    from app.entity.scraped_product import ScrapedProduct


class Keyword(Base):
    __tablename__ = "keyword"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    word: Mapped[str] = mapped_column(String(256), nullable=False, unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(UtcDateTime(), default=utcnow(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(UtcDateTime(), default=utcnow(), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(UtcDateTime(), default=None)

    # relationships
    scraped_products: Mapped[list["ScrapedProduct"]] = relationship("ScrapedProduct", back_populates="keyword")

    def __repr__(self):
        return f"<Keyword(name='{self.word}')>"
