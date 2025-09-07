from sqlalchemy import Column, Integer, Enum, String
from sqlalchemy_utc import UtcDateTime, utcnow

from app.config.database import Base
from app.enum.channel_enum import ChannelEnum


class SitemapSource(Base):
    __tablename__ = "sitemap_source"

    id = Column(Integer, primary_key=True)
    channel = Column(Enum(ChannelEnum), nullable=False)  # 새로운 채널 추가
    sitemap_url = Column(String(1024), nullable=False)
    filepath = Column(String(1024), nullable=False)
    created_at = Column(UtcDateTime(), default=utcnow(), nullable=True)
    last_synced_at = Column(UtcDateTime(), default=utcnow(), nullable=True)

    def __repr__(self):
        return f"SitemapSource(id={self.id}, channel={self.channel}, url={self.sitemap_url})"
