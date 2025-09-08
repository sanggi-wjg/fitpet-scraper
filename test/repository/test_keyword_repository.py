from test.repository.test_repository_context import TestRepositoryContext


class TestKeywordRepository(TestRepositoryContext):

    def test_find_by_word(self, keyword_repository, keyword_entity_fixture, db_session):
        # given
        keyword = keyword_repository.save(keyword_entity_fixture)
        db_session.flush()
        # when
        result = keyword_repository.find_by_word(keyword.word)
        # then
        assert result == keyword
