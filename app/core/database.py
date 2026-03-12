import logging
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from app.core.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


engine = create_engine(
    url=settings.database.dsn,
    pool_size=settings.database.pool_size,
    max_overflow=settings.database.max_overflow,
    pool_timeout=settings.database.pool_timeout,
    pool_recycle=settings.database.pool_recycle,
    pool_pre_ping=settings.database.pool_pre_ping,
    isolation_level=settings.database.isolation_level,
    echo=settings.debug,
    echo_pool=settings.debug,
)
session_factory = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI 의존성 주입 목적
    ⚠️ 자동으로 트랜잭션의 commit, rollback 처리
    """
    db = session_factory()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        logger.exception("[get_db] 데이터베이스 트랜잭션 중 예외 발생.")
        raise
    finally:
        db.close()


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """
    서비스 구현 로직 사용 목적
    ⚠️ 자동으로 트랜잭션의 commit, rollback 처리

    with get_db_session() as db:
        ...
    """
    db = session_factory()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        logger.exception("[get_db_session] 데이터베이스 트랜잭션 중 예외 발생.")
        raise
    finally:
        db.close()
