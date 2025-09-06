from decimal import Decimal

import pytest

from app.client.model.api_response_model import NaverShoppingApiResponse


@pytest.fixture
def naver_shopping_item_fixture() -> NaverShoppingApiResponse.Item:
    """네이버 쇼핑 검색 결과 Item fixture"""
    return NaverShoppingApiResponse.Item(
        title="잇츄",
        link="https://shopping.naver.com/catalog/12345",
        image="https://shopping-phinf.pstatic.net/test_image.jpg",
        lprice=Decimal("10000"),
        hprice=None,
        mallName="네이버",
        productId="12345",
        productType="1",
        brand="잇츄",
        maker="잇츄",
        category1="생활/건강",
        category2="반려동물용품",
        category3="강아지용품",
        category4="사료",
    )
