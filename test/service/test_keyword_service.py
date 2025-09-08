from app.entity import Keyword
from test.service.test_service_context import TestServiceContext


class TestKeywordService(TestServiceContext):

    def test_create_keyword(self, keyword_service, db_session):
        # give
        word = "단어"
        # when
        keyword_service.create_keyword(word)
        # then
        found_keyword = db_session.query(Keyword).filter_by(word=word).first()
        assert found_keyword is not None
        assert found_keyword.word == word
