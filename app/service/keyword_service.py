from typing import List

from app.config.database import transactional
from app.entity import Keyword
from app.repository.keyword_repository import KeywordRepository
from app.service.model.service_models import KeywordModel


class KeywordService:

    def __init__(self):
        self.keyword_repository = KeywordRepository(Keyword)

    @transactional()
    def get_available_keywords(self) -> List[KeywordModel]:
        return [KeywordModel.model_validate(item) for item in self.keyword_repository.find_available_all()]

    @transactional()
    def create_keyword(self, word: str):
        keyword = Keyword(word=word)
        self.keyword_repository.save(keyword)
