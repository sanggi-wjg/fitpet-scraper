from functools import lru_cache

from app.config.database import transactional
from app.entity import Keyword
from app.exception.exceptions import KeywordAlreadyExistsException
from app.repository.keyword_repository import KeywordRepository
from app.service.model.service_models import KeywordModel


class KeywordService:

    def __init__(self, keyword_repository: KeywordRepository = KeywordRepository(Keyword)):
        self.keyword_repository = keyword_repository

    @transactional
    def get_available_keywords(self) -> list[KeywordModel]:
        return [KeywordModel.model_validate(item) for item in self.keyword_repository.find_all_available()]

    @transactional
    def create_keyword(self, word: str):
        if self.keyword_repository.find_by_word(word):
            raise KeywordAlreadyExistsException(word)

        keyword = Keyword(word=word)
        self.keyword_repository.save(keyword)


@lru_cache
def get_keyword_service() -> KeywordService:
    return KeywordService()
