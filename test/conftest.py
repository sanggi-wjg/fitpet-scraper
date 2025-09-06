import os
from typing import Generator

import pytest
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.config.database import Base, _set_current_session, _clear_current_session
from app.entity import Keyword, ScrapedProduct, ScrapedProductDetail
from app.repository.keyword_repository import KeywordRepository
from app.repository.scraped_product_detail_repository import ScrapedProductDetailRepository
from app.repository.scraped_product_repository import ScrapedProductRepository
from app.service.keyword_service import KeywordService
from app.service.scraped_product_service import ScrapedProductService


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
    try:
        yield session
    finally:
        _clear_current_session()
        session.close()


##################################################
# Repository
##################################################


@pytest.fixture
def keyword_repository(db_session) -> KeywordRepository:
    return KeywordRepository(Keyword)


@pytest.fixture
def scraped_product_repository(db_session) -> ScrapedProductRepository:
    return ScrapedProductRepository(ScrapedProduct)


@pytest.fixture
def scraped_product_detail_repository(db_session) -> ScrapedProductDetailRepository:
    return ScrapedProductDetailRepository(ScrapedProductDetail)


##################################################
# Service
##################################################


@pytest.fixture
def keyword_service(db_session, keyword_repository):
    return KeywordService(keyword_repository)


@pytest.fixture
def scraped_product_service(db_session, scraped_product_repository, scraped_product_detail_repository):
    return ScrapedProductService(scraped_product_repository, scraped_product_detail_repository)


##################################################
# Fixture
##################################################


@pytest.fixture
def keyword_entity_fixture() -> Keyword:
    return Keyword(word="잇츄")


@pytest.fixture
def scraped_product_entity_factory():
    from app.enum.channel_enum import ChannelEnum

    def create_scraped_product(
        name: str = "잇츄 100g",
        channel: ChannelEnum = ChannelEnum.NAVER_SHOPPING,
        channel_product_id: str = "test_product_123",
        is_tracking_required: bool = False,
        keyword: Keyword = None,
    ) -> ScrapedProduct:
        product = ScrapedProduct(
            name=name,
            channel=channel,
            channel_product_id=channel_product_id,
            is_tracking_required=is_tracking_required,
        )
        product.keyword = keyword
        return product

    return create_scraped_product
