from typing import List

from app.api.model.api_response_model import NaverShoppingApiResponse
from app.config.database import transactional
from app.entity import ScrapedProduct, ScrapedProductDetail
from app.enum.channel_enum import ChannelEnum
from app.repository.scraped_product_detail_repository import ScrapedProductDetailRepository
from app.repository.scraped_product_repository import ScrapedProductRepository
from app.service.model.service_models import ScrapedProductModel


class ScrapedProductService:

    def __init__(self):
        self.scraped_product_repository = ScrapedProductRepository(ScrapedProduct)
        self.scraped_product_detail_repository = ScrapedProductDetailRepository(ScrapedProductDetail)

    @transactional()
    def get_tracking_required_products(self, channel: ChannelEnum) -> List[ScrapedProductModel]:
        return [
            ScrapedProductModel.model_validate(item)
            for item in self.scraped_product_repository.find_all_channel_and_tracking_required(channel)
        ]

    @transactional()
    def save_naver_shopping_search_result(
        self,
        searched_items: List[NaverShoppingApiResponse.Item],
        keyword_id: int,
        is_tracking_required: bool,
    ):
        for item in searched_items:
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
