from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entity import Keyword


class KeywordRepository:

    def __init__(self, session: Session):
        self.session = session

    def find_by_word(self, word: str) -> Keyword | None:
        stmt = select(Keyword).where(Keyword.word == word)
        return self.session.scalar(stmt)

    def find_all_available(self) -> list[Keyword]:
        stmt = select(Keyword).where(Keyword.is_deleted.is_(False)).order_by(Keyword.id)
        return list(self.session.scalars(stmt))

    def save(self, keyword: Keyword) -> Keyword:
        self.session.add(keyword)
        self.session.flush()
        return keyword
