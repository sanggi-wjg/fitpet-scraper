from app.api.naver_shopping_api import NaverShoppingApi
from app.config.database import transactional
from app.entity import ScrapedProduct
from app.enum.channel_enum import ChannelEnum
from app.repository.scraped_product_repository import ScrapedProductRepository


class ScrapeService:

    def __init__(self):
        self.scraped_product_repository = ScrapedProductRepository(ScrapedProduct)

    @transactional()
    def save_naver_shopping_result(self):
        # self.scraped_product_repository.find_by_channel_and_name(ChannelEnum.NAVER_SHOPPING, )
        pass

