import logging

import httpx

from app.client.model.api_response_model import NaverShoppingApiResponse
from app.core.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class NaverShoppingClient:
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

    def search(self, query: str, strat: int, display: int, sort: str) -> NaverShoppingApiResponse:
        params: dict[str, str | int] = {
            "query": query,
            "start": strat,
            "display": display,
            "sort": sort,
        }

        with httpx.Client() as client:
            response = client.get(self.base_url, headers=self.headers, params=params)
            response.raise_for_status()
            return NaverShoppingApiResponse(**response.json())

    def search_with_all_pages(self, query: str) -> list[NaverShoppingApiResponse.Item]:
        all_items = []
        start = 1

        first_response: NaverShoppingApiResponse = self.search(query, start, self.default_display, self.default_sort)
        all_items.extend(first_response.items)
        # 네이버는 1000개까지만 지원
        max_total = min(first_response.total, 1000)

        while start + self.default_display <= max_total:
            start += self.default_display
            response: NaverShoppingApiResponse = self.search(query, start, self.default_display, self.default_sort)
            all_items.extend(response.items)

        return all_items
