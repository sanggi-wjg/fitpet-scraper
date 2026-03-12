from functools import lru_cache
import httpx

from app.client.model.api_response_model import PetFriendsProductDetailApiResponse
from app.util.util_header import get_fake_headers


class PetFriendsClient:

    def __init__(self):
        self.base_url = "https://mobile.api.pet-friends.co.kr"
        self.headers = get_fake_headers()

    def get_product_detail(self, product_id: str) -> PetFriendsProductDetailApiResponse:
        url = f"{self.base_url}/product/detail_v2"
        payload = {"product_id": str(product_id)}

        with httpx.Client(headers=self.headers) as client:
            response = client.post(url, json=payload)
            response.raise_for_status()
            return PetFriendsProductDetailApiResponse(**response.json())


@lru_cache
def get_pet_friends_client():
    return PetFriendsClient()
