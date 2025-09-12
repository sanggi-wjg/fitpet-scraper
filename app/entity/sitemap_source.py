from sqlalchemy import Column, Integer, Enum, String
from sqlalchemy_utc import UtcDateTime, utcnow

from app.config.database import Base
from app.enum.channel_enum import ChannelEnum
from app.util.util_datetime import UtilDatetime


class SitemapSource(Base):
    __tablename__ = "sitemap_source"

    id = Column(Integer, primary_key=True)
    channel = Column(Enum(ChannelEnum), nullable=False)  # 새로운 채널 추가
    sitemap_url = Column(String(256), nullable=False)
    filepath = Column(String(256), nullable=True)
    created_at = Column(UtcDateTime(), default=utcnow(), nullable=False)
    last_pulled_at = Column(UtcDateTime(), nullable=True)

    def __repr__(self):
        return f"SitemapSource(id={self.id}, channel={self.channel}, url={self.sitemap_url})"

    def get_escaped_sitemap_url(self):
        return self.sitemap_url.replace("https://", "").replace("/", "_")

    def is_syncable(self):
        return self.last_pulled_at is not None and self.filepath is not None

    def pulled(self, filepath: str):
        self.filepath = filepath
        self.last_pulled_at = UtilDatetime.utc_now()
