from typing import List

from app.entity import Keyword
from app.repository.base_repository import BaseRepository


class KeywordRepository(BaseRepository[Keyword]):

    def find_available_all(self) -> List[Keyword]:
        return self.session.query(Keyword).filter(Keyword.is_deleted.is_(False)).all()
