from sqlalchemy.orm import Session

from app.entity import Keyword
from app.exception.exceptions import KeywordAlreadyExistsException
from app.repository.keyword_repository import KeywordRepository


class KeywordService:

    def __init__(self, session: Session):
        self.keyword_repository = KeywordRepository(session)

    def get_keywords(self) -> list[Keyword]:
        return self.keyword_repository.find_all_available()

    def create_keyword(self, word: str) -> Keyword:
        if self.keyword_repository.find_by_word(word):
            raise KeywordAlreadyExistsException(word)

        keyword = Keyword(word=word)
        return self.keyword_repository.save(keyword)
