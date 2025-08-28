from abc import ABC
from typing import TypeVar, Generic, Optional, Type, List

from sqlalchemy.orm import Session

from app.config.database import Base, get_current_session

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T], ABC):

    def __init__(self, entity: Type[T]):
        self.entity = entity

    @property
    def session(self):
        session: Session = get_current_session()
        if not session:
            raise RuntimeError("Session is not set. Use @transactional decorator.")
        return session

    def find_by_id(self, entity_id: int) -> Optional[T]:
        return self.session.query(self.entity).filter_by(id=entity_id).first()

    def find_all(self) -> List[T]:
        return self.session.query(self.entity).all()

    def find_all_by_ids(self, entity_ids: List[int]) -> List[T]:
        if not entity_ids:
            return []
        return self.session.query(self.entity).filter(self.entity.id.in_(entity_ids)).all()

    def save(self, entity: T) -> T:
        self.session.add(entity)
        # self.session.flush()
        return entity

    def save_all(self, entities: List[T]) -> List[T]:
        if not entities:
            return []
        self.session.add_all(entities)
        return entities

    def delete(self, entity: T) -> None:
        self.session.delete(entity)

    def delete_by_id(self, entity_id: int) -> bool:
        if found := self.find_by_id(entity_id):
            self.delete(found)
            return True
        return False
