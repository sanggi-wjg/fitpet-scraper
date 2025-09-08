from datetime import datetime

import pytz
from freezegun import freeze_time

from app.util.util_datetime import UtilDatetime


class TestUtilDatetime:

    @freeze_time("2025-09-05 11:37:46", tz_offset=0)
    def test_utc_now(self):
        expected = datetime(2025, 9, 5, 11, 37, 46, tzinfo=pytz.UTC)

        assert UtilDatetime.utc_now() == expected

    def test_to_utc(self):
        given = datetime(2025, 9, 5, 11, 37, 46)
        expected = datetime(2025, 9, 5, 11, 37, 46, tzinfo=pytz.UTC)

        assert UtilDatetime.to_utc(given) == expected

    def test_to_utc_with_kst(self):
        given = datetime(2025, 9, 5, 20, 37, 46, tzinfo=pytz.timezone("Asia/Seoul"))
        expected = datetime(2025, 9, 5, 12, 9, 46, tzinfo=pytz.UTC)

        assert UtilDatetime.to_utc(given) == expected

    def test_subtract_hours_from(self):
        given = datetime(2025, 9, 5, 11, 37, 46, tzinfo=pytz.UTC)
        expected = datetime(2025, 9, 5, 10, 37, 46, tzinfo=pytz.UTC)

        assert UtilDatetime.subtract_hours_from(1, given) == expected

    @freeze_time("2025-09-05 11:37:46", tz_offset=0)
    def test_subtract_hours_from_with_now(self):
        expected = datetime(2025, 9, 5, 10, 37, 46, tzinfo=pytz.UTC)

        assert UtilDatetime.subtract_hours_from(1) == expected
