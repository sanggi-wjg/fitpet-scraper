from datetime import datetime, timedelta

import pytz


class DateTimeUtil:

    @classmethod
    def utc_now(cls) -> datetime:
        return datetime.now(pytz.UTC)

    @classmethod
    def to_utc(cls, dt: datetime) -> datetime:
        if dt.tzinfo is None:
            return dt.replace(tzinfo=pytz.UTC)
        return dt.astimezone(pytz.UTC)

    @classmethod
    def subtract_hours_from(cls, hours: int, dt: datetime = None) -> datetime:
        if dt is None:
            return cls.utc_now() - timedelta(hours=hours)
        return dt - timedelta(hours=hours)
