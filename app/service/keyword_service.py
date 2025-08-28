from typing import List

from app.entity import Keyword
from app.repository.keyword_repository import KeywordRepository
from app.service.model.service_models import KeywordModel


class KeywordService:

    def __init__(self):
        self.keyword_repository = KeywordRepository(Keyword)

    def get_available_keywords(self) -> List[KeywordModel]:
        return [KeywordModel.model_validate(keyword) for keyword in self.keyword_repository.find_available_all()]
