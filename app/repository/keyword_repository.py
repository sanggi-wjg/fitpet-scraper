from app.entity import Keyword
from app.repository.base_repository import BaseRepository


class KeywordRepository(BaseRepository[Keyword]):

    def find_by_word(self, word: str) -> Keyword | None:
        return self.session.query(self.entity).filter(self.entity.word == word).first()

    def find_all_available(self) -> list[Keyword]:
        return (
            self.session.query(self.entity)
            .filter(
                self.entity.is_deleted.is_(False),
            )
            .all()
        )
