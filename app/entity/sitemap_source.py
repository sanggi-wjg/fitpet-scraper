from datetime import datetime

from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utc import UtcDateTime, utcnow

from app.core.database import Base
from app.enum.channel_enum import ChannelEnum
from app.util.util_datetime import UtilDatetime


class SitemapSource(Base):
    __tablename__ = "sitemap_source"

    id: Mapped[int] = mapped_column(primary_key=True)
    channel: Mapped[ChannelEnum] = mapped_column(Enum(ChannelEnum), nullable=False)
    sitemap_url: Mapped[str] = mapped_column(String(256), nullable=False)
    filepath: Mapped[str | None] = mapped_column(String(256), nullable=True)
    created_at: Mapped[datetime] = mapped_column(UtcDateTime(), default=utcnow(), nullable=False)
    last_pulled_at: Mapped[datetime | None] = mapped_column(UtcDateTime(), nullable=True)

    def __repr__(self):
        return f"SitemapSource(id={self.id}, channel={self.channel}, url={self.sitemap_url})"

    def get_escaped_sitemap_url(self):
        return self.sitemap_url.replace("https://", "").replace("/", "_")

    def is_syncable(self):
        return self.last_pulled_at is not None and self.filepath is not None

    def pulled(self, filepath: str):
        self.filepath = filepath
        self.last_pulled_at = UtilDatetime.utc_now()
