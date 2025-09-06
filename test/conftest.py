import os
from typing import Generator

import pytest
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.config.database import Base, _set_current_session
from app.entity import Keyword
from app.repository.keyword_repository import KeywordRepository
from app.service.keyword_service import KeywordService


@pytest.fixture(scope="session")
def test_engine() -> Engine:
    engine = create_engine(
        "sqlite:///:memory:",
        poolclass=StaticPool,
        connect_args={
            "check_same_thread": False,
        },
        echo=True if os.getenv("DEBUG", True) else False,
    )
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture(scope="session")
def test_session_factory(test_engine) -> sessionmaker[Session]:
    return sessionmaker(
        bind=test_engine,
        autocommit=False,
        autoflush=False,
    )


@pytest.fixture
def db_session(test_session_factory) -> Generator[Session, None, None]:
    session = test_session_factory()
    _set_current_session(session)
    yield session


@pytest.fixture
def keyword_repository(db_session) -> KeywordRepository:
    return KeywordRepository(Keyword)


@pytest.fixture
def keyword_service(db_session, keyword_repository):
    return KeywordService(keyword_repository)


@pytest.fixture
def keyword_single_fixture() -> Keyword:
    return Keyword(word="단어")
