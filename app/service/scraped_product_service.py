from sqlalchemy.orm import Session

from app.client.model.api_response_model import NaverShoppingApiResponse
from app.entity import ScrapedProduct, ScrapedProductDetail
from app.enum.channel_enum import ChannelEnum
from app.repository.model.search_conditions import ScrapedProductSearchCondition
from app.repository.scraped_product_detail_repository import ScrapedProductDetailRepository
from app.repository.scraped_product_repository import ScrapedProductRepository


class ScrapedProductService:

    def __init__(self, session: Session):
        self.scraped_product_repository = ScrapedProductRepository(session)
        self.scraped_product_detail_repository = ScrapedProductDetailRepository(session)

    def get_tracking_required_products(self, channel: ChannelEnum) -> list[ScrapedProduct]:
        return self.scraped_product_repository.find_all_by_channel_and_tracking_required(channel)

    def get_all_products_with_related(self, search_condition: ScrapedProductSearchCondition) -> list[ScrapedProduct]:
        return self.scraped_product_repository.find_all_with_related(search_condition)

    def get_all_products_with_latest_detail(
        self, search_condition: ScrapedProductSearchCondition
    ) -> list[ScrapedProduct]:
        return self.scraped_product_repository.find_all_with_latest_detail(search_condition)

    def delete_by_channel(self, channel: ChannelEnum):
        self.scraped_product_repository.delete_by_channel(channel)

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

            scraped_product = self.scraped_product_repository.save(
                ScrapedProduct(
                    keyword_id=keyword_id,
                    name=item.title,
                    channel=ChannelEnum.NAVER_SHOPPING,
                    channel_product_id=item.product_id,
                    is_tracking_required=False,
                    # last_scraped_at=UtilDatetime.utc_now(),
                )
            )

            if is_tracking_required and item.is_mall_name_naver:
                scraped_product.update_tracking_require()

            if not is_tracking_required and scraped_product.is_tracking_required:
                scraped_product.update_tracking_disable()

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
