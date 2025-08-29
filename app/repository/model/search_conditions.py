from dataclasses import dataclass
from datetime import datetime

from app.enum.channel_enum import ChannelEnum


@dataclass(frozen=True, slots=True)
class ScrapedProductSearchCondition:
    created_at_before: datetime | None = None
    created_at_after: datetime | None = None
    name: str | None = None
    channel: ChannelEnum | None = None
