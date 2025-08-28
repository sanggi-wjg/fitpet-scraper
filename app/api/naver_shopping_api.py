import httpx

from app.api.model.response import NaverShoppingApiResponse
from app.config.settings import get_settings
from app.util.decorators import run_catching

settings = get_settings()


class NaverShoppingApi:

    def __init__(self):
        self.client_id = settings.naver_shopping.client_id
        self.client_secret = settings.naver_shopping.client_secret
        self.base_url = "https://openapi.naver.com/v1/search/shop.json"
        self.headers = {
            "X-Naver-Client-Id": self.client_id,
            "X-Naver-Client-Secret": self.client_secret,
        }

    @run_catching
    def search(self, query: str, strat: int = 1) -> NaverShoppingApiResponse:
        params = {
            "query": query,
            "display": 100,
            "start": strat,
            "sort": "sim",
        }

        with httpx.Client() as client:
            response = client.get(self.base_url, headers=self.headers, params=params)
            response.raise_for_status()
            return NaverShoppingApiResponse(**response.json())

    def search_all_pages(self):
        pass
