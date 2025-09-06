from app.entity import ScrapedProduct
from app.enum.channel_enum import ChannelEnum
from app.service.model.service_models import ScrapedProductModel
from test.service.test_service_context import TestServiceContext


class TestScrapedProductService(TestServiceContext):

    def test_get_tracking_required_product(
        self,
        db_session,
        keyword_repository,
        scraped_product_repository,
        scraped_product_service,
        keyword_entity_fixture,
        scraped_product_entity_factory,
    ):
        # given
        keyword = keyword_repository.save(keyword_entity_fixture)
        scraped_product = scraped_product_repository.save(
            scraped_product_entity_factory(
                channel=ChannelEnum.NAVER_SHOPPING,
                is_tracking_required=True,
                keyword=keyword,
            ),
        )
        db_session.commit()

        expected = ScrapedProductModel.model_validate(scraped_product)

        # when
        result = scraped_product_service.get_tracking_required_products(ChannelEnum.NAVER_SHOPPING)

        # then
        assert len(result) == 1
        assert result[0] == expected

    def test_save_naver_shopping_search_result(
        self,
        db_session,
        keyword_repository,
        scraped_product_service,
        keyword_entity_fixture,
        naver_shopping_item_fixture,
    ):
        # given
        keyword = keyword_repository.save(keyword_entity_fixture)
        db_session.commit()

        # when
        scraped_product_service.save_naver_shopping_search_result(
            searched_items=[naver_shopping_item_fixture],
            keyword_id=keyword.id,
            keyword_word=keyword.word,
            is_tracking_required=True,
        )
        db_session.commit()

        # then
        result = db_session.query(ScrapedProduct).all()
        assert len(result) == 1
