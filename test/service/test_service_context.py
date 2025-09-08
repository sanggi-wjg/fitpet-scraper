import pytest

from app.config.database import Base


class TestServiceContext:

    @pytest.fixture(autouse=True)
    def setup_method(self, db_session):
        yield
        for table in reversed(Base.metadata.sorted_tables):
            db_session.execute(table.delete())
        db_session.commit()
