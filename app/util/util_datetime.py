from datetime import datetime, timedelta

import pytz


class DatetimeUtil:

    @classmethod
    def utc_now(cls) -> datetime:
        return datetime.now(pytz.UTC)

    @classmethod
    def to_utc(cls, dt: datetime) -> datetime:
        if dt.tzinfo is None:
            return dt.replace(tzinfo=pytz.UTC)
        return dt.astimezone(pytz.UTC)

    @classmethod
    def subtract_hours_from(cls, hours: int, dt: datetime | None = None) -> datetime:
        if dt is None:
            return cls.utc_now() - timedelta(hours=hours)
        if dt.tzinfo is None:
            dt = cls.to_utc(dt)
        return dt - timedelta(hours=hours)
