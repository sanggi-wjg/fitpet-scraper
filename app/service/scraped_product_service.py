from functools import lru_cache

from app.client.model.api_response_model import NaverShoppingApiResponse
from app.config.database import transactional
from app.entity import ScrapedProduct, ScrapedProductDetail
from app.enum.channel_enum import ChannelEnum
from app.repository.model.search_conditions import ScrapedProductSearchCondition
from app.repository.scraped_product_detail_repository import ScrapedProductDetailRepository
from app.repository.scraped_product_repository import ScrapedProductRepository
from app.service.model.service_models import ScrapedProductModel, ScrapedProductWithRelatedModel
from app.util.util_datetime import UtilDatetime


class ScrapedProductService:

    def __init__(
        self,
        scraped_product_repository: ScrapedProductRepository = ScrapedProductRepository(ScrapedProduct),
        scraped_product_detail_repository: ScrapedProductDetailRepository = ScrapedProductDetailRepository(
            ScrapedProductDetail
        ),
    ):
        self.scraped_product_repository = scraped_product_repository
        self.scraped_product_detail_repository = scraped_product_detail_repository

    @transactional
    def get_tracking_required_products(self, channel: ChannelEnum) -> list[ScrapedProductModel]:
        return [
            ScrapedProductModel.model_validate(item)
            for item in self.scraped_product_repository.find_all_by_channel_and_tracking_required(channel)
        ]

    @transactional
    def get_all_products_with_related(
        self, search_condition: ScrapedProductSearchCondition
    ) -> list[ScrapedProductWithRelatedModel]:
        return [
            ScrapedProductWithRelatedModel.model_validate(item)
            for item in self.scraped_product_repository.find_all_with_related(search_condition)
        ]

    @transactional
    def save_naver_shopping_search_result(
        self,
        searched_items: list[NaverShoppingApiResponse.Item],
        keyword_id: int,
        keyword_word: str,
        is_tracking_required: bool,
    ):
        for item in searched_items:
            if keyword_word not in item.title:
                continue

            scraped_product = self.scraped_product_repository.find_by_channel_and_product_id(
                ChannelEnum.NAVER_SHOPPING, item.product_id
            )

            if not scraped_product:
                scraped_product = self.scraped_product_repository.save(
                    ScrapedProduct(
                        keyword_id=keyword_id,
                        name=item.title,
                        channel=ChannelEnum.NAVER_SHOPPING,
                        channel_product_id=item.product_id,
                        is_tracking_required=False,
                    )
                )
            if is_tracking_required and item.is_mall_name_naver:
                scraped_product.update_tracking_require()

            if not is_tracking_required and scraped_product.is_tracking_required:
                scraped_product.update_tracking_disable()

            # 3시간 이내 중복건은 제외처리
            exists_detail = None
            hours_ago = UtilDatetime.subtract_hours_from(3)

            for detail in scraped_product.details:
                if detail.created_at is None:
                    exists_detail = detail
                    break
                if detail.created_at >= hours_ago and detail.mall_name == item.mall_name and detail.link == item.link:
                    exists_detail = detail
                    break
            if exists_detail:
                continue

            scraped_product.details.append(
                ScrapedProductDetail(
                    scraped_product_id=scraped_product.id,
                    link=item.link,
                    image_link=item.image,
                    price=item.lprice,
                    mall_name=item.mall_name,
                    product_type=item.product_type,
                    brand=item.brand,
                    maker=item.maker,
                    scraped_result=item.model_dump_json(),
                )
            )


@lru_cache
def get_scraped_product_service() -> ScrapedProductService:
    return ScrapedProductService()
