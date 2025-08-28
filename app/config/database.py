import functools
import logging
import threading
from contextlib import contextmanager
from typing import Generator, Callable

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from app.config.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

_local = threading.local()

engine = create_engine(
    settings.sqlite_database.path,
    connect_args={"check_same_thread": True},
)
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)
Base = declarative_base()


def create_tables():
    from app.entity import Keyword, ScrapedProduct, ScrapedProductDetail  # noqa: F401

    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_session() -> Session:
    return getattr(_local, "session", None)


def _set_current_session(session: Session):
    _local.session = session


def _clear_current_session():
    if hasattr(_local, "session"):
        delattr(_local, "session")


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        _set_current_session(session)
        yield session
    finally:
        _clear_current_session()
        session.close()


def transactional():
    def decorator(func: Callable):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_session = get_current_session()
            if current_session and current_session.in_transaction():
                return func(*args, **kwargs)

            session = current_session or SessionLocal()
            if not current_session:
                _set_current_session(session)

            try:
                result = func(*args, **kwargs)
                session.commit()
                return result

            except Exception as e:
                logger.error(f"Unexpected error during transaction for {func.__name__}: {e}")
                session.rollback()
                raise

            finally:
                _clear_current_session()
                session.close()

        return wrapper

    return decorator
