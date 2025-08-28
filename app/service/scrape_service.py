from typing import List

from app.api.model.api_response_model import NaverShoppingApiResponse
from app.config.database import transactional
from app.entity import ScrapedProduct
from app.enum.channel_enum import ChannelEnum
from app.repository.scraped_product_repository import ScrapedProductRepository


class ScrapeService:

    def __init__(self):
        self.scraped_product_repository = ScrapedProductRepository(ScrapedProduct)

    @transactional()
    def save_naver_shopping_result(
        self,
        items: List[NaverShoppingApiResponse.Item],
        keyword_id: int,
        is_tracking_required: bool,
    ):
        for item in items:
            scraped_product = self.scraped_product_repository.find_by_channel_and_name(
                ChannelEnum.NAVER_SHOPPING, item.title
            )

            if not scraped_product:
                scraped_product = self.scraped_product_repository.save(
                    ScrapedProduct(
                        name=item.title,
                        channel=ChannelEnum.NAVER_SHOPPING,
                        keyword_id=keyword_id,
                        is_tracking_required=is_tracking_required,
                    )
                )

            scraped_product.add_detail_from_naver_shopping(
                link=item.link,
                image_link=item.image,
                price=item.lprice,
                mall_name=item.mall_name,
                product_id=item.product_id,
                product_type=item.product_type,
                brand=item.brand,
                maker=item.maker,
                scraped_result=item.scraped_result,
            )
