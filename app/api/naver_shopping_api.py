import logging
from typing import List

import httpx

from app.api.model.api_response_model import NaverShoppingApiResponse
from app.config.settings import get_settings
from app.util.decorators import run_catching, Result

logger = logging.getLogger(__name__)
settings = get_settings()


class NaverShoppingApi:
    """
    https://developers.naver.com/docs/serviceapi/search/shopping/shopping.md#%EC%87%BC%ED%95%91
    """

    def __init__(self):
        self.client_id = settings.naver_shopping.client_id
        self.client_secret = settings.naver_shopping.client_secret
        self.base_url = "https://openapi.naver.com/v1/search/shop.json"
        self.headers = {
            "X-Naver-Client-Id": self.client_id,
            "X-Naver-Client-Secret": self.client_secret,
        }
        self.default_display = 100
        self.default_sort = "sim"

    @run_catching
    def search(self, query: str, strat: int, display: int, sort: str) -> NaverShoppingApiResponse:
        params = {"query": query, "start": strat, "display": display, "sort": sort}

        with httpx.Client() as client:
            response = client.get(self.base_url, headers=self.headers, params=params)
            response.raise_for_status()
            return NaverShoppingApiResponse(**response.json())

    def search_with_all_pages(self, query: str) -> List[NaverShoppingApiResponse.Item]:
        all_items = []
        start = 1

        first_result: Result[NaverShoppingApiResponse] = self.search(
            query, start, self.default_display, self.default_sort
        )
        if first_result.is_failure:
            logger.error(f"🔥 네이버 쇼핑 API 호출 실패, {first_result.exception}")
            raise first_result.exception

        first_response = first_result.get_or_raise()
        all_items.extend(first_response.items)
        # 네이버는 1000개까지만 지원
        max_total = min(first_response.total, 1000)

        while start + self.default_display <= max_total:
            start += self.default_display
            result: Result[NaverShoppingApiResponse] = self.search(
                query, start, self.default_display, self.default_sort
            )
            if result.is_success and result.get_or_raise().has_items():
                all_items.extend(result.get_or_raise().items)
            else:
                logger.warning(f"⚠️ 네이버 쇼핑 페이지 {start}에서 API 호출 실패, {result.exception}")

        return all_items
